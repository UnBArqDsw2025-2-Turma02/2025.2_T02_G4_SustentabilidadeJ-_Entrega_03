from django.apps import AppConfig

class AbstractFactoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "App.abstract_factory"
    label = "abstract_factory"
    verbose_name = "Abstract Factory"
