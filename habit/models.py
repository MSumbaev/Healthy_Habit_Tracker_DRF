from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    """Класс - Привычка"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель привычки', **NULLABLE)

    place = models.CharField(max_length=100, verbose_name='Место выполнения привычки')
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=150, verbose_name='Действие привычки')
    is_pleasant = models.BooleanField(verbose_name='Признак приятной привычки')
    linked = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    period = models.SmallIntegerField(verbose_name='Периодичность')
    reward = models.CharField(max_length=100, verbose_name='Вознаграждение', **NULLABLE)
    length = models.SmallIntegerField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(verbose_name='Признак публикации')

    def __str__(self):
        return f'{self.action}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
