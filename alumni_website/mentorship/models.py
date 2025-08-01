from django.db import models
from core.models import Users

class Mentor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="mentor") 
    availability = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f'name: str({self.user})'
    

class MentorSkills(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="skills")
    skill = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.mentor.user}"

class Languages(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="languages")
    language = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.mentor.user}"

class MentorMatch(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_matches')
    mentee = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='mentee_matches')
    accept = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f"{self.mentor.user}"