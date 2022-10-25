from django.apps import AppConfig


class SmartlombardapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartlombardAPI'
    verbose_name = "2. Товары требующие модерации"

    def ready(self):
        from . import signals
        signals.request_finished.connect(signals.my_callback)
