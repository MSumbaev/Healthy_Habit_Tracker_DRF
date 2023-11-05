from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Класс Юзер"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    tg_username = models.CharField(max_length=150, verbose_name='Telegram username')
    tg_chat_id = models.IntegerField(unique=True, verbose_name='Telegram chat id', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
