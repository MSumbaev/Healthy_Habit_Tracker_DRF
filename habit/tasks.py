from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from habit.models import Habit
from habit.services import checking_users_for_chat_id, send_message
from users.models import User


@shared_task
def send_notification_tg():
    """Проверка времени для отправки уведомлений и отправление в telegram"""
    token = settings.TG_BOT_TOKEN

    habits = Habit.objects.all()
    users = User.objects.all()

    checking_users_for_chat_id(token, users)

    now = timezone.now()

    for habit in habits:

        if habit.last_dispatch_time:
            if habit.last_dispatch_time <= now - timedelta(days=habit.period):
                send_message(token, habit)
                habit.last_dispatch_time = now
                habit.save()
        else:
            if habit.time <= now.time():
                send_message(token, habit)
                habit.last_dispatch_time = now
                habit.save()
