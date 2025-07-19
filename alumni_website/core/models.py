from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    is_teacher = models.BooleanField(default=False)