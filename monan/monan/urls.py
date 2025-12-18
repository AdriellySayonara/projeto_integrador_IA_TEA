from django.contrib import admin
# Importa a interface administrativa do Django.

from django.urls import path, include
# Importa funções para definir URLs e incluir arquivos de urls de apps.

from django.contrib.auth import views as auth_views
# Importa views de autenticação prontas do Django (login, logout, reset de senha, etc.)

from django.views.generic import TemplateView
# Importa views genéricas (não utilizadas diretamente aqui, mas podem ser usadas para páginas estáticas).

from . import views
# Importa views personalizadas do projeto.

from django.conf import settings
from django.conf.urls.static import static
# Importações para servir arquivos de mídia (uploads) em ambiente de desenvolvimento.


# ============================================================
# Definição das rotas principais do projeto
# ============================================================
urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # Inclui todas as URLs do app 'core'
    path('', include('core.urls')),

    # URLs de autenticação do Django (login, logout, reset de senha)
    path('accounts/', include('django.contrib.auth.urls')),

    # Login customizado com template específico
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    # Logout customizado, redireciona para login
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # Reset de senha com template personalizado
    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),

    # Registro de usuário (comentado por enquanto)
    # path('accounts/register/', views.register_view, name='register'),
    # path('accounts/register/success/', views.registration_success, name='registration_success'),

    # Perfil do usuário
    path('profile/', views.profile_view, name='profile'),

    # Atualização de avatar
    path('profile/update-avatar/', views.update_avatar, name='update_avatar'),

    # Alteração de senha personalizada
    path('profile/change-password/', views.change_password, name='change_password')
]

# ============================================================
# Servir arquivos de mídia em desenvolvimento
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Durante o desenvolvimento, o Django servirá arquivos
    # de mídia (como avatares) diretamente.
