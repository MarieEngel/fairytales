from django.apps import AppConfig


class FairytalesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fairytales"

    # def ready(self):
    #     import users.signals
