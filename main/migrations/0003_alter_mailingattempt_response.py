# Generated by Django 5.0.4 on 2024-04-05 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingattempt',
            name='response',
            field=models.TextField(blank=True, default='Ответ сервера', null=True, verbose_name='Ответ сервера'),
        ),
    ]
