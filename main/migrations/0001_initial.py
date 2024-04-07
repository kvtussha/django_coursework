# Generated by Django 5.0.4 on 2024-04-05 05:33

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('email',),
                'permissions': [('can_view_client', 'Can view client'), ('can_block_client', 'Can block client')],
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Тема сообщения')),
                ('body', models.TextField(verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_time', models.TimeField(auto_now_add=True, verbose_name='Время рассылки')),
                ('status', models.CharField(choices=[('Создана', 'Создана'), ('Завершена', 'Завершена'), ('В процессе', 'В процессе')], default='Создана', max_length=50, verbose_name='Статус')),
                ('start_date', models.DateTimeField(default=datetime.date.today, verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(default=datetime.date.today, verbose_name='Дата окончания')),
                ('frequency', models.CharField(choices=[('Один раз', 'Один раз'), ('1 раз в день', '1 раз в день'), ('1 раз в неделю', '1 раз в неделю'), ('1 раз в месяц', '1 раз в месяц')], max_length=30, verbose_name='Периодичность')),
                ('is_active', models.BooleanField(default=False)),
                ('clients', models.ManyToManyField(related_name='mailing_messages', to='main.client', verbose_name='Клиенты')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'permissions': [('set_mailing_status', 'Can set mailing status'), ('can_mailing_disabling', 'Отключение рассылки')],
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Время рассылки')),
                ('status', models.CharField(choices=[('delivered', 'доставлено'), ('not_delivered', 'не доставлено')], verbose_name='Статус')),
                ('response', models.TextField(blank=True, null=True, verbose_name='Ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Статистика (попытка)',
                'verbose_name_plural': 'Статистики (попытки)',
            },
        ),
    ]
