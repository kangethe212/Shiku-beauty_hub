"""
App configuration for beautyhub
"""
from django.apps import AppConfig


class BeautyhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beautyhub'
    verbose_name = 'Shiku Beauty Hub'
    
    def ready(self):
        """Import signals when app is ready"""
        import beautyhub.signals

