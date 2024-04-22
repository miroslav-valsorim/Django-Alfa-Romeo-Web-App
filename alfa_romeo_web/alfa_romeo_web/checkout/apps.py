from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alfa_romeo_web.checkout'

    # def ready(self):
    #     import alfa_romeo_web.checkout.signals
    #     result = super().ready()
    #     return result
