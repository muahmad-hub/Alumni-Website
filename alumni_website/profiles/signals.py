from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Goal, Skill, UserAlumniRecommendation

@receiver(post_save, sender=Profile)
def create_default_goals_skills(sender, instance, created, **kwargs):
    if created:

        for i in range(3):
            Goal.objects.create(profile=instance, goal="", goal_category="")
        for j in range(3):
            Skill.objects.create(profile=instance, skill="", skill_category="")
        
        UserAlumniRecommendation.objects.create(profile=instance)