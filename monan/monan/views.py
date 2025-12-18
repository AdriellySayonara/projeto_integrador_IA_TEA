from django.shortcuts import render, redirect, get_object_or_404
# Funções utilitárias do Django para renderizar templates,
# redirecionar requisições e obter objetos do banco com validação 404.

from django.contrib.auth.models import User
# Modelo de usuário padrão do Django.

from django.contrib import messages
# Sistema de mensagens do Django para feedback ao usuário.

from django.contrib.auth.decorators import login_required
# Decorator para restringir views apenas a usuários autenticados.

from django.db.models import Count
# Importa funções de agregação para contagem de objetos.

from datetime import datetime, timedelta
# Utilizado para manipulação de datas.

from django.contrib.auth import update_session_auth_hash
# Mantém a sessão ativa após alteração de senha.

from django.contrib.auth.forms import PasswordChangeForm
# Formulário padrão do Django para mudança de senha.

# Importa modelos personalizados e o formulário de criação de usuário
from core.models import EEGFile, Analysis, Profile, ReportConfig
from .forms import CustomUserCreationForm 





# ============================================================
# DASHBOARD DO USUÁRIO
# ============================================================
@login_required
def dashboard(request):
    user = request.user
    
    # Total de arquivos enviados
    total_uploads = EEGFile.objects.filter(user=user).count()
    
    # Total de laudos concluídos
    total_reports = Analysis.objects.filter(eeg_file__user=user).count()
    
    # Arquivos pendentes ou em processamento
    processing_files = EEGFile.objects.filter(user=user, status__in=['processing', 'pending']).count()
    
    # Arquivos com status 'completed'
    successful_files = EEGFile.objects.filter(user=user, status='completed').count()
    
    # Calcula taxa de sucesso
    success_rate = round((successful_files / total_uploads) * 100) if total_uploads > 0 else 0
    
    # Últimos uploads (para exibir no dashboard)
    recent_uploads = EEGFile.objects.filter(user=user).order_by('-uploaded_at')[:5]
    
    # Notificações para o usuário
    notifications = []
    if EEGFile.objects.filter(user=user, status='error').exists():
        notifications.append({
            'type': 'warning',
            'title': 'Arquivos com erro',
            'message': 'Alguns arquivos falharam no processamento.',
            'icon': 'exclamation-triangle-fill'
        })
    
    context = {
        'user': user,
        'total_uploads': total_uploads,
        'total_reports': total_reports,
        'processing_files': processing_files,
        'success_rate': success_rate,
        'recent_uploads': recent_uploads,
        'notifications': notifications,
    }
    
    return render(request, 'dashboard.html', context)


# ============================================================
# PERFIL DO USUÁRIO
# ============================================================
@login_required
def profile_view(request):
    """Exibe página do perfil do usuário"""
    # Garante que o Profile exista
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    return render(request, 'profile.html', {'user': request.user})


@login_required
def update_avatar(request):
    """Atualiza a foto de perfil do usuário"""
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        avatar = request.FILES['avatar']
        
        # Valida se é realmente uma imagem
        if not avatar.content_type.startswith('image/'):
            messages.error(request, 'Por favor, envie apenas imagens.')
            return redirect('profile')
            
        profile.avatar = avatar
        profile.save()
        messages.success(request, 'Foto atualizada!')
    
    return redirect('profile')


@login_required
def change_password(request):
    """Permite alteração de senha"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém usuário logado
            messages.success(request, 'Senha alterada com sucesso!')
        else:
            # Exibe mensagens de erro
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('profile')


# ============================================================
# UPLOAD DE ARQUIVOS
# ============================================================
@login_required
def upload_file(request):
    """Faz upload de arquivos EEG"""
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        EEGFile.objects.create(
            user=request.user,
            file=file,
            original_name=file.name,
            size_bytes=file.size,
            status='pending'  # Define status inicial
        )
        messages.success(request, 'Arquivo enviado! O processamento iniciará em breve.')
        return redirect('dashboard')
    
    return render(request, 'upload.html')


# ============================================================
# HISTÓRICO DE RELATÓRIOS
# ============================================================
@login_required
def report_history(request):
    """Exibe todos os arquivos enviados pelo usuário"""
    files = EEGFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'history.html', {'user_files': files})


# ============================================================
# CONFIGURAÇÕES DE RELATÓRIO
# ============================================================
@login_required
def report_settings(request):
    """Permite configurar formato e frequência dos relatórios"""
    config, created = ReportConfig.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        config.format = request.POST.get('format')
        config.frequency = request.POST.get('frequency')
        config.save()
        messages.success(request, 'Configurações salvas.')
    return render(request, 'report_settings.html', {'config': config})


# ============================================================
# SOLICITAÇÃO DE ANÁLISE
# ============================================================
@login_required
def request_analysis(request):
    """Exibe arquivos ainda não analisados"""
    files = EEGFile.objects.filter(user=request.user, analysis__isnull=True)
    return render(request, 'request_analysis.html', {'user_files': files})


# ============================================================
# INICIAR ANÁLISE (SIMULADA)
# ============================================================
@login_required
def analyze_file(request, file_id):
    """Simula o início de uma análise de EEG"""
    eeg_file = get_object_or_404(EEGFile, id=file_id, user=request.user)
    eeg_file.status = 'processing'
    eeg_file.save()
    messages.info(request, f'Análise iniciada para {eeg_file.original_name}')
    return redirect('dashboard')
