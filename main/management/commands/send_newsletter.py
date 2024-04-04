import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Mailing, MailingAttempt
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send newsletters to clients'

    def handle(self, *args, **options):
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

        self.stdout.write(self.style.SUCCESS('Successfully sent newsletters'))
