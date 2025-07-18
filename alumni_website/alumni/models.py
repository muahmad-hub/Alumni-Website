from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    is_teacher = models.BooleanField(default=False)

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

class Mentor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="mentor") 
    availability = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

class Skills(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="skills")
    skill = models.TextField(null=True, blank=True)

class Languages(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="languages")
    language = models.CharField(max_length=255, null=True, blank=True)

class MentorMatch(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_matches')
    mentee = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='mentee_matches')
    accept = models.BooleanField(null=True, default=None)