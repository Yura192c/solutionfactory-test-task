from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from src.newsletter.models import Dispatch, Client, Message


@shared_task
def send_statistics_email():
    # Получение статистики обработанных рассылок
    current_date = datetime.now().date()
    dispatches_today = Dispatch.objects.filter(start_time__date=current_date)
    messages = Message.objects.filter(dispatch__in=dispatches_today)
    failed_messages = messages.filter(status='F')
    sent_messages = messages.filter(status='S')
    pending_messages = messages.filter(status='P')

    # Отправка статистики по email
    subject = 'Статистика обработанных рассылок'
    message = f'Обработано рассылок: {dispatches_today.count()}\n' \
              f'Отправлено сообщений: {messages.count()}\n' \
              f'Успешно: {sent_messages.count()}\n' \
              f'Неудачно: {failed_messages.count()}\n' \
              f'В ожидании: {pending_messages.count()}\n'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = settings.STATISTICS_EMAIL_RECIPIENTS
    send_mail(subject, message, from_email, recipient_list)
