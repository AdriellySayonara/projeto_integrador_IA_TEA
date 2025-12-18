# core/decorators.py
# Arquivo responsável por definir decorators de controle de acesso
# às views, com base no perfil (papel) do usuário autenticado.

from django.shortcuts import redirect
# Função utilitária do Django para redirecionar o usuário
# para outra rota/URL nomeada.

from django.contrib import messages
# Framework de mensagens do Django, usado para exibir feedback
# (erros, avisos, sucessos) ao usuário na interface.


def can_upload(view_func):
    """
    Decorator que restringe o acesso à view apenas para
    usuários com perfil de Médico ou Administrador.
    """
    def _wrapped_view(request, *args, **kwargs):
        # Obtém o perfil do usuário autenticado, se existir.
        # O uso de getattr evita erro caso o usuário não tenha perfil.
        profile = getattr(request.user, 'profile', None)

        # Verifica se existe perfil e se o usuário é médico ou admin.
        # O administrador tem acesso irrestrito.
        if profile and (profile.is_doctor or profile.is_admin):
            # Caso autorizado, executa a view original
            return view_func(request, *args, **kwargs)
        else:
            # Caso não autorizado, exibe mensagem de erro ao usuário
            messages.error(request, "Apenas médicos podem enviar arquivos.")

            # Redireciona o usuário para o dashboard
            return redirect('dashboard')

    # Retorna a função encapsulada, mantendo o comportamento da view
    return _wrapped_view


def can_audit(view_func):
    """
    Decorator que restringe o acesso à view apenas para
    usuários com perfil de Auditor ou Administrador.
    """
    def _wrapped_view(request, *args, **kwargs):
        # Obtém o perfil associado ao usuário autenticado
        profile = getattr(request.user, 'profile', None)

        # Verifica se existe perfil e se o usuário é auditor ou admin.
        # O administrador também possui acesso.
        if profile and (profile.is_auditor or profile.is_admin):
            # Caso autorizado, executa a view original
            return view_func(request, *args, **kwargs)
        else:
            # Caso não autorizado, exibe mensagem de erro
            messages.error(request, "Acesso restrito à auditoria.")

            # Redireciona o usuário para o dashboard
            return redirect('dashboard')

    # Retorna a função decorada
    return _wrapped_view
