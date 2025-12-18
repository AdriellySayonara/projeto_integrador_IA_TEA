from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('analysis/request/', views.request_analysis, name='request_analysis'),
    path('analysis/run/<int:file_id>/', views.analyze_file, name='analyze_file'),
    path('analysis/result/<int:analysis_id>/', views.result_view, name='result_view'), # Adicionei esta rota usada no redirect
    path('reports/history/', views.report_history, name='report_history'),
    path('reports/settings/', views.report_settings, name='report_settings'),
    path('reports/preview/<int:analysis_id>/', views.report_preview, name='report_preview'),
    path('reports/pdf/<int:analysis_id>/', views.report_pdf, name='report_pdf'),
    path('profile/', views.dashboard, name='profile'), # Redireciona perfil para dashboard por enquanto
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('history/', views.report_history, name='report_history'),
    path('settings/', views.report_settings, name='report_settings'),
    path('analysis/request/', views.request_analysis, name='request_analysis'),
    path('analysis/run/<int:file_id>/', views.analyze_file, name='analyze_file'),
]