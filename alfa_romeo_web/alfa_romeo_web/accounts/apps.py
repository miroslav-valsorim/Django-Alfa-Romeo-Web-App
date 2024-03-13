from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alfa_romeo_web.accounts'

    def ready(self):
        import alfa_romeo_web.accounts.signals
