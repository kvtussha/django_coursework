# Generated by Django 5.0.4 on 2024-04-05 05:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailingmessage', verbose_name='Сообщение'),
        ),
    ]
