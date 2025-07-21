from django.db import models
from core.models import Users

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    career = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    has_job = models.BooleanField(null=True)
    employer = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f'name: {self.name}, email: {self.user.email}'