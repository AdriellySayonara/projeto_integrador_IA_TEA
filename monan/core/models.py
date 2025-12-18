from django.db import models
# Importa o módulo base de models do Django, utilizado
# para definição das tabelas e campos do banco de dados.

from django.contrib.auth.models import User
# Importa o modelo padrão de usuário do Django,
# que será utilizado como base de autenticação.

from django.db.models.signals import post_save
# Signal disparado automaticamente após a execução de um save()
# em um modelo específico.

from django.dispatch import receiver
# Decorator utilizado para registrar funções como
# receptoras de sinais (signals) do Django.


# ============================================================
# Modelo responsável por armazenar arquivos de EEG enviados
# ============================================================
class EEGFile(models.Model):
    # Definição dos possíveis estados do processamento do arquivo
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('error', 'Erro'),
    ]

    # Usuário responsável pelo envio do arquivo
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Arquivo físico armazenado no sistema de arquivos
    file = models.FileField(upload_to='eeg_files/')

    # Nome original do arquivo no momento do upload
    original_name = models.CharField(max_length=255)

    # Tamanho do arquivo em bytes, útil para validações e exibição
    size_bytes = models.BigIntegerField()

    # Status atual do arquivo, baseado nos STATUS_CHOICES
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Data e hora do upload (definida automaticamente)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Representação em string do objeto (usada no Admin e shell)
    def __str__(self):
        return self.original_name
    
    # --------------------------------------------------------
    # Propriedade para exibir o tamanho do arquivo de forma
    # amigável (bytes, KB ou MB)
    # --------------------------------------------------------
    @property
    def size_formatted(self):
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 * 1024:
            return f"{self.size_bytes / 1024:.1f} KB"
        else:
            return f"{self.size_bytes / (1024 * 1024):.1f} MB"


# ============================================================
# Modelo responsável por armazenar a análise de um arquivo EEG
# ============================================================
class Analysis(models.Model):
    # Relação um-para-um com o arquivo de EEG
    # Cada arquivo possui no máximo uma análise
    eeg_file = models.OneToOneField(EEGFile, on_delete=models.CASCADE)

    # Data e hora em que a análise foi realizada
    analyzed_at = models.DateTimeField(auto_now_add=True)

    # Resultado da classificação
    # True  -> TEA
    # False -> Não TEA
    classification = models.BooleanField(default=False)

    # Grau de confiança do modelo (0.0 a 1.0)
    confidence = models.FloatField(default=0.0)
    
    # Representação textual do objeto
    def __str__(self):
        return f"Analysis of {self.eeg_file.original_name}"
    
    # --------------------------------------------------------
    # Propriedade para exibir o resultado de forma legível
    # --------------------------------------------------------
    @property
    def result_display(self):
        return "TEA Detectado" if self.classification else "Normal"
    
    # --------------------------------------------------------
    # Propriedade para exibir a confiança em formato percentual
    # --------------------------------------------------------
    @property
    def confidence_percent(self):
        return f"{self.confidence * 100:.1f}%"


# ============================================================
# Modelo de configuração de geração de relatórios por usuário
# ============================================================
class ReportConfig(models.Model):
    # Opções de frequência para geração de relatórios
    FREQUENCY_CHOICES = [
        ('on_demand', 'Sob demanda'),
        ('daily', 'Diária'),
        ('weekly', 'Semanal'),
    ]

    # Formatos disponíveis para o relatório
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('html', 'HTML'),
    ]
    
    # Usuário ao qual a configuração pertence
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Formato padrão do relatório
    format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default='pdf'
    )

    # Frequência de geração do relatório
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='on_demand'
    )
    
    # Representação textual da configuração
    def __str__(self):
        return f"Configuração de {self.user.username}"


# ============================================================
# Modelo de Perfil do Usuário (extensão do User padrão)
# ============================================================
class Profile(models.Model):
    # Papéis possíveis no sistema
    ROLE_CHOICES = [
        ('admin', 'Administrador do Sistema'),
        ('doctor', 'Médico'),
        ('auditor', 'Auditor'),
    ]
    
    # Relação um-para-um com o usuário
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Avatar opcional do usuário
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Papel/função do usuário no sistema
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='doctor'
    )
    
    # Representação textual do perfil
    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
    
    # --------------------------------------------------------
    # Propriedades auxiliares para verificação de permissões
    # --------------------------------------------------------
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_doctor(self):
        return self.role == 'doctor'
    
    @property
    def is_auditor(self):
        return self.role == 'auditor'
    
    # --------------------------------------------------------
    # Define a cor do badge de acordo com o papel do usuário
    # (útil para interfaces com Bootstrap, por exemplo)
    # --------------------------------------------------------
    @property
    def role_badge_color(self):
        colors = {
            'admin': 'danger',
            'doctor': 'primary',
            'auditor': 'warning'
        }
        return colors.get(self.role, 'secondary')


# ============================================================
# Signal para manter o Profile sincronizado com o User
# ============================================================
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Verifica se o usuário já possui um perfil associado.
    # Evita erro caso o perfil ainda não exista.
    if hasattr(instance, 'profile'):
        # Salva o perfil sempre que o usuário for salvo,
        # garantindo consistência dos dados.
        instance.profile.save()
