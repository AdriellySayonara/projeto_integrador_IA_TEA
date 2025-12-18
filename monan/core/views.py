from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EEGFile, Analysis, ReportConfig
# Importe aqui suas bibliotecas de análise (ex: mne, numpy, weka wrappers)
import os

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Validação simples de extensão
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.gdf', '.dta']:
            messages.error(request, "Formato inválido. Use .gdf ou .dta")
            return redirect('upload_file')
            
        eeg = EEGFile.objects.create(
            user=request.user,
            file=uploaded_file,
            original_name=uploaded_file.name,
            size_bytes=uploaded_file.size
        )
        messages.success(request, "Arquivo enviado com sucesso!")
        return redirect('request_analysis')
    return render(request, 'upload.html')

@login_required
def request_analysis(request):
    # Lista arquivos que ainda NÃO foram analisados
    user_files = EEGFile.objects.filter(user=request.user, analysis__isnull=True).order_by('-uploaded_at')
    return render(request, 'request_analysis.html', {'user_files': user_files})

@login_required
def analyze_file(request, file_id):
    eeg_file = get_object_or_404(EEGFile, id=file_id, user=request.user)
    
    # --- AQUI ENTRARIA SUA LÓGICA DE IA/PYTHON/WEKA ---
    # Simulando um resultado para o sistema não quebrar:
    import random
    classification = random.choice([True, False]) 
    confidence = random.uniform(50, 99)
    # ---------------------------------------------------

    analysis = Analysis.objects.create(
        eeg_file=eeg_file,
        classification=classification,
        confidence=confidence
    )
    
    messages.success(request, "Análise concluída.")
    return redirect('result_view', analysis_id=analysis.id)

@login_required
def result_view(request, analysis_id):
    analysis = get_object_or_404(Analysis, eeg_file__user=request.user, id=analysis_id)
    return render(request, 'result.html', {'analysis': analysis})

@login_required
def report_history(request):
    analyses = Analysis.objects.filter(eeg_file__user=request.user).order_by('-analyzed_at')
    return render(request, 'history.html', {'analyses': analyses})

@login_required
def report_settings(request):
    config, created = ReportConfig.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        config.format = request.POST.get('format')
        config.frequency = request.POST.get('frequency')
        config.save()
        messages.success(request, "Configurações salvas.")
    return render(request, 'report_settings.html', {'config': config})

@login_required
def report_preview(request, analysis_id):
    # Renderiza a página que contém o iframe do PDF
    analysis = get_object_or_404(Analysis, eeg_file__user=request.user, id=analysis_id)
    return render(request, 'report_preview.html', {'analysis_id': analysis.id})

@login_required
def report_pdf(request, analysis_id):
    # Placeholder para geração do PDF real
    # Você precisaria usar WeasyPrint ou ReportLab aqui
    from django.http import HttpResponse
    return HttpResponse("PDF gerado (Mock)", content_type='application/pdf')

