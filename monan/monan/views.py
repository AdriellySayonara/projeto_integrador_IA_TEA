from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Importar os modelos corretos e o formulário
from core.models import EEGFile, Analysis, Profile, ReportConfig
from .forms import CustomUserCreationForm 

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado! Faça login para continuar.')
            return redirect('registration_success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/registration_success.html')

@login_required
def dashboard(request):
    user = request.user
    
    # --- Lógica corrigida para usar EEGFile ---
    
    # Total de uploads
    total_uploads = EEGFile.objects.filter(user=user).count()
    
    # Total de laudos (Análises concluídas)
    total_reports = Analysis.objects.filter(eeg_file__user=user).count()
    
    # Arquivos em processamento ou pendentes
    processing_files = EEGFile.objects.filter(
        user=user,
        status__in=['processing', 'pending']
    ).count()
    
    # Arquivos com sucesso (status completed)
    successful_files = EEGFile.objects.filter(
        user=user,
        status='completed'
    ).count()
    
    # Taxa de sucesso
    success_rate = 0
    if total_uploads > 0:
        success_rate = round((successful_files / total_uploads) * 100)
    
    # Uploads recentes (últimos 7 dias)
    # Nota: No template, usa-se 'upload.original_name' e 'upload.uploaded_at'
    recent_uploads = EEGFile.objects.filter(
        user=user
    ).order_by('-uploaded_at')[:5]
    
    # Notificações
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

@login_required
def profile_view(request):
    """Exibir página do perfil"""
    # Garante que o profile existe
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_avatar(request):
    """Atualizar foto de perfil"""
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        avatar = request.FILES['avatar']
        
        if not avatar.content_type.startswith('image/'):
            messages.error(request, 'Por favor, envie apenas imagens.')
            return redirect('profile')
            
        profile.avatar = avatar
        profile.save()
        messages.success(request, 'Foto atualizada!')
    
    return redirect('profile')

@login_required
def change_password(request):
    """Alterar senha"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('profile')

# --- Views Faltantes que os templates pedem ---

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # Criar o registro no banco
        EEGFile.objects.create(
            user=request.user,
            file=file,
            original_name=file.name,
            size_bytes=file.size,
            status='pending' 
        )
        messages.success(request, 'Arquivo enviado! O processamento iniciará em breve.')
        return redirect('dashboard')
    return render(request, 'upload.html')

@login_required
def report_history(request):
    # Lista todos os arquivos e seus status
    files = EEGFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'history.html', {'user_files': files})

@login_required
def report_settings(request):
    config, created = ReportConfig.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        config.format = request.POST.get('format')
        config.frequency = request.POST.get('frequency')
        config.save()
        messages.success(request, 'Configurações salvas.')
    return render(request, 'report_settings.html', {'config': config})

@login_required
def request_analysis(request):
    # Mostra arquivos que ainda não têm análise
    files = EEGFile.objects.filter(user=request.user, analysis__isnull=True)
    return render(request, 'request_analysis.html', {'user_files': files})

@login_required
def analyze_file(request, file_id):
    # Simulação de gatilho de análise
    eeg_file = get_object_or_404(EEGFile, id=file_id, user=request.user)
    eeg_file.status = 'processing'
    eeg_file.save()
    messages.info(request, f'Análise iniciada para {eeg_file.original_name}')
    return redirect('dashboard')