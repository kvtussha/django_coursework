from datetime import date

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    surname = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    def __str__(self):
        return f'{self.email} ({self.name} {self.surname})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email',)
        permissions = [
            (
                'can_view_client',
                'Can view client'
            ),
            (
                'can_block_client',
                'Can block client'
            ),
        ]


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст сообщения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Sending(models.Model):
    ONCE = 'Один раз'
    DAILY = '1 раз в день'
    WEEKLY = '1 раз в неделю'
    MONTHLY = '1 раз в месяц'

    FREQUENCY_CHOICES = [
        (ONCE, 'Один раз'),
        (DAILY, '1 раз в день'),
        (WEEKLY, '1 раз в неделю'),
        (MONTHLY, '1 раз в месяц'),
    ]

    CREATED = 'Создана'
    COMPLETED = 'Завершена'
    LAUNCHED = 'В процессе'

    SELECT_STATUS = [
        (CREATED, 'Создана'),
        (COMPLETED, 'Завершена'),
        (LAUNCHED, 'В процессе'),
    ]

    scheduled_time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    status = models.CharField(max_length=50, default='Создана', choices=SELECT_STATUS, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    start_date = models.DateField(default=date.today, verbose_name='Дата начала')
    end_date = models.DateField(default=date.today, verbose_name='Дата окончания')
    frequency = models.CharField(max_length=30, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')

    def __str__(self):
        return f'id: {self.id}, время рассылки: {self.scheduled_time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'set_sending_status',
                'Can set sending status'
            ),
            (
                'can_view_sending',
                'Can view sending'
            ),
        ]


class MailingAttempt(models.Model):
    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'

    STATUS = (
        (DELIVERED, 'доставлено'),
        (NOT_DELIVERED, 'не доставлено'),
    )

    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='Рассылка')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Время рассылки')
    status = models.CharField(choices=STATUS, verbose_name='Статус')
    response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f"{self.sending.message.subject} - {self.sent_at}"

    class Meta:
        verbose_name = 'Статистика (попытка)'
        verbose_name_plural = 'Статистики (попытки)'
