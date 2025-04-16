from django.apps import AppConfig

class StaffpanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staffpanel'
    ##
    def ready(self):
        import staffpanel.signals


