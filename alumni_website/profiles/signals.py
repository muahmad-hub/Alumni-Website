from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Goal, Skill, UserAlumniRecommendation
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=Profile)
def create_default_goals_skills(sender, instance, created, **kwargs):
    if created:

        for i in range(3):
            Goal.objects.create(profile=instance, goal="", goal_category="")
        for j in range(3):
            Skill.objects.create(profile=instance, skill="", skill_category="")
        
        UserAlumniRecommendation.objects.create(profile=instance)

@receiver([post_save], sender=Profile)
def clear_profile_cache(sender, **kwargs):
    from django.core.cache import cache
    cache.delete("all_profile_data")
    cache.delete("connections_graph")
    cache.delete("simple_algo_profiles")
