from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    
    def ready(self):
        """Initialise les signaux d'audit logging"""
        import users.signals  # noqa
