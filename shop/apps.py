from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = "1. Управления товарами"

    def ready(self):
        from . import signals
        signals.request_finished.connect(signals.my_callback)
