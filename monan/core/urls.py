from django.urls import path
# Importa a função path, utilizada para mapear URLs para views no Django.

from django.contrib.auth import views as auth_views
# Importa as views prontas de autenticação do Django (login, logout, etc.).
# Neste arquivo específico, elas não estão sendo utilizadas diretamente,
# mas a importação foi mantida conforme o código original.

from . import views
# Importa o módulo de views da própria aplicação,
# onde estão definidas as funções que tratam cada rota.


# ============================================================
# Definição das rotas (URL patterns) da aplicação
# ============================================================
urlpatterns = [
    # Rota principal do sistema, exibindo o dashboard do usuário
    path('', views.dashboard, name='dashboard'),

    # Rota responsável pelo upload de arquivos EEG
    path('upload/', views.upload_file, name='upload_file'),

    # Rota para solicitar a análise de um arquivo enviado
    path('analysis/request/', views.request_analysis, name='request_analysis'),

    # Rota que executa a análise de um arquivo específico,
    # identificado pelo ID do arquivo
    path('analysis/run/<int:file_id>/', views.analyze_file, name='analyze_file'),

    # Rota para exibição do resultado de uma análise específica,
    # utilizada após o processamento
    path(
        'analysis/result/<int:analysis_id>/',
        views.result_view,
        name='result_view'
    ),  # Rota adicionada para uso em redirects após a análise

    # Rota para visualização do histórico de relatórios
    path('reports/history/', views.report_history, name='report_history'),

    # Rota para configuração das preferências de relatórios do usuário
    path('reports/settings/', views.report_settings, name='report_settings'),

    # Rota para pré-visualização de um relatório baseado em uma análise
    path(
        'reports/preview/<int:analysis_id>/',
        views.report_preview,
        name='report_preview'
    ),

    # Rota para geração/visualização do relatório em PDF
    path(
        'reports/pdf/<int:analysis_id>/',
        views.report_pdf,
        name='report_pdf'
    ),
]
