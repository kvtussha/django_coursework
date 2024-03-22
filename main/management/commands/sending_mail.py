from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Sending, MailingAttempt
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta


class Command(BaseCommand):
    help = 'Starts mailing scheduler'

    def handle(self, *args, **options):
        self.start()

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.send_mailing, 'interval', minutes=30)  # Запуск каждые 30 минут
        scheduler.start()

    def send_mailing(self):
        current_datetime = timezone.now()
        mailings = Sending.objects.filter(date__lte=current_datetime).filter(
            status__in=['CREATED', 'LAUNCHED'])  # Вы можете настроить статусы как в вашей модели
        for mailing in mailings:
            last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-date').first()
            if not last_attempt or current_datetime - last_attempt.date >= timedelta(days=1):
                try:
                    # Отправляем письмо
                    send_mail(
                        subject=mailing.subject,
                        message=mailing.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.clients.all()],
                        fail_silently=False
                    )
                    # Создаем запись о попытке рассылки
                    MailingAttempt.objects.create(mailing=mailing)
                except Exception as e:
                    # Обработка ошибок отправки
                    self.stdout.write(self.style.ERROR(f'Failed to send mailing: {e}'))
