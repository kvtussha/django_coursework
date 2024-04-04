import os

from django.core.mail import send_mail
from django.utils import timezone

from main.models import Mailing, MailingAttempt


def send_email_job():
    now = timezone.now()
    newsletters = Mailing.objects.filter(start_date__lte=now, end_date__gte=now)

    for newsletter in newsletters:
        clients = newsletter.clients.all()

        for client in clients:
            try:
                send_mail(
                    newsletter.message.subject,
                    'Текст рассылки',
                    os.getenv('EMAIL_HOST_USER'),
                    [client.email],
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                success = False

            # Сохранение статистики о попытке отправки
            MailingAttempt.objects.create(newsletter=newsletter, success=success)

    print("Successfully sent newsletters")
