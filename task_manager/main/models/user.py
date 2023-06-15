from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager.services.storage_backends import public_storage


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        MANAGER = "manager"
        DEVELOPER = "developer"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar_picture = models.ImageField(null=True, storage=public_storage)
