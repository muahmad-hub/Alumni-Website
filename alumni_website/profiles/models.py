from django.db import models
from core.models import Users

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    university_location = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    career = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    has_job = models.BooleanField(null=True)
    employer = models.CharField(max_length=255, null=True, blank=True)
    education_level = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.SlugField(unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'name: {self.name}, email: {self.user.email}'
    
class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills", null=True)
    skill = models.CharField(max_length=255)
    skill_category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.profile} has {self.skill} skill in category {self.skill_category}"
    
class Goal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="goals", null=True)
    goal = models.CharField(max_length=255, null=True, blank=True)
    goal_category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.profile} has {self.goal} goal in category {self.goal_category}"
    
class Connection(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="connection_initiated", null=True)
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="connection_received", null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} and {self.profile2}"
