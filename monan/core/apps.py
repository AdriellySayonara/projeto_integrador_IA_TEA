from django.apps import AppConfig
# Importa a classe base AppConfig, utilizada para configurar
# o comportamento e os metadados de uma aplicação Django.


class CoreConfig(AppConfig):
    # Define o tipo de campo que será usado automaticamente
    # para chaves primárias (id) dos modelos da aplicação,
    # quando não especificado explicitamente.
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome da aplicação conforme registrado no projeto Django.
    # Esse valor deve corresponder ao nome do app criado.
    name = 'core'
