from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'IqtinaaAPI'

    def ready(self):
        import IqtinaaAPI.signals
  
