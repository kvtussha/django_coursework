from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Отправитель рассылок
    """

    class User(AbstractUser):
        email = models.EmailField(unique=True)
        is_verified = models.BooleanField(default=False)
        verification_code = models.CharField(max_length=100, blank=True, null=True)

        def __str__(self):
            return self.username
