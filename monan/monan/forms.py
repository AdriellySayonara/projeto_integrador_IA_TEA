# monan/forms.py
# Arquivo responsável por definir formulários personalizados
# utilizados no sistema, especialmente relacionados à autenticação
# e criação de usuários.

from django import forms
# Importa o módulo base de formulários do Django.

from django.contrib.auth.forms import UserCreationForm
# Importa o formulário padrão de criação de usuários do Django,
# que já inclui validações de senha e confirmação.

from django.contrib.auth.models import User
# Importa o modelo padrão de usuário do Django,
# que será utilizado como base para o formulário.


# ============================================================
# Formulário personalizado de criação de usuário
# ============================================================
class CustomUserCreationForm(UserCreationForm):
    # Campo de e-mail obrigatório, com widget personalizado
    # para melhor integração visual (Bootstrap)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )

    # Campo de primeiro nome obrigatório
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome'
        })
    )

    # Campo de sobrenome obrigatório
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu sobrenome'
        })
    )
    
    # --------------------------------------------------------
    # Configuração do formulário
    # --------------------------------------------------------
    class Meta:
        # Define que o formulário está associado ao modelo User
        model = User

        # Define explicitamente os campos que aparecerão no formulário
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
    
    # --------------------------------------------------------
    # Inicialização personalizada do formulário
    # --------------------------------------------------------
    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe pai para manter
        # todo o comportamento padrão do UserCreationForm
        super().__init__(*args, **kwargs)

        # Itera sobre todos os campos do formulário
        # para aplicar classes e placeholders dinamicamente
        for field_name, field in self.fields.items():
            # Garante que todos os campos utilizem a classe do Bootstrap
            field.widget.attrs['class'] = 'form-control'

            # Placeholder específico para o campo de usuário
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Escolha um nome de usuário'

            # Placeholder específico para o campo de senha
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Crie uma senha segura'

            # Placeholder específico para a confirmação de senha
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Confirme sua senha'
