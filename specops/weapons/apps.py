from tabnanny import verbose
from django.apps import AppConfig


class WeaponsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weapons'
    verbose_name = 'Оружие мира'