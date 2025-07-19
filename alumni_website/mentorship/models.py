from django.db import models
from core.models import Users

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