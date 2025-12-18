# core/admin.py
# Arquivo responsável por configurar como os modelos da aplicação
# serão exibidos e administrados no Django Admin.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Importação dos modelos da aplicação
from .models import Profile, EEGFile, Analysis
from .models import Profile  # (Importação repetida, mas mantida conforme solicitado)

# ============================================================
# 1. Configurar o Perfil para aparecer dentro do Usuário
# ============================================================
# Essa classe permite que o modelo Profile seja exibido
# embutido (inline) dentro da tela de edição do User no Admin.
class ProfileInline(admin.StackedInline):
    # Define qual modelo será exibido como inline
    model = Profile

    # Impede a exclusão do perfil diretamente pelo admin,
    # garantindo integridade entre User e Profile
    can_delete = False

    # Nome exibido no painel administrativo
    verbose_name_plural = 'Definição de Papel (Médico/Auditor)'

    # Define qual campo faz a ligação com o User
    fk_name = 'user'

# ============================================================
# 2. Personalizar a tela de Usuários do Admin
# ============================================================
# Esta classe estende o UserAdmin padrão do Django
# para incluir o Profile e personalizar a listagem.
class CustomUserAdmin(BaseUserAdmin):
    # Adiciona o ProfileInline à tela de edição do usuário
    inlines = (ProfileInline,)
    
    # Define quais colunas aparecem na lista de usuários
    list_display = ('username', 'email', 'first_name', 'get_role', 'is_active')

    # Otimiza consultas ao banco usando JOIN com o Profile
    list_select_related = ('profile',)

    # Método personalizado para exibir o papel/função do usuário
    # diretamente na tabela do admin
    def get_role(self, instance):
        # Verifica se o usuário possui um perfil associado
        if hasattr(instance, 'profile'):
            # Retorna o valor legível do campo role (choices)
            return instance.profile.get_role_display()
        # Caso não exista perfil vinculado
        return "Sem perfil"

    # Nome da coluna exibida no Django Admin
    get_role.short_description = 'Função'

# ============================================================
# 3. Registrar as alterações no Admin
# ============================================================
# Remove o registro padrão do modelo User
admin.site.unregister(User)

# Registra o User novamente utilizando a configuração personalizada
admin.site.register(User, CustomUserAdmin)

# ============================================================
# Registro dos demais modelos no Django Admin
# ============================================================

# Configuração do admin para arquivos de EEG
@admin.register(EEGFile)
class EEGFileAdmin(admin.ModelAdmin):
    # Campos exibidos na listagem
    list_display = ('original_name', 'user', 'status', 'uploaded_at')

    # Filtros disponíveis na lateral do admin
    list_filter = ('status', 'uploaded_at')

# Configuração do admin para análises de EEG
@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    # Campos exibidos na listagem de análises
    list_display = ('eeg_file', 'classification', 'confidence', 'analyzed_at')
