import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import Mailing, MailingAttempt
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send newsletters to clients'

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(start_date__lte=now, end_date__gte=now)

        for mailing in mailings:
            clients = mailing.clients.all()
            mailing.is_active = True

            for client in clients:
                success = send_mail(
                    mailing.message.subject,
                    'Текст рассылки',
                    os.getenv('EMAIL_HOST_USER'),
                    [client.email],
                    fail_silently=False,
                )

                # Сохранение статистики о попытке отправки
                MailingAttempt.objects.create(mailing=mailing, sent_at=now, status='COMPLETED',
                                              response=success)

        self.stdout.write(self.style.SUCCESS('Successfully sent newsletters'))
