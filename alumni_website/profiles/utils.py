from .models import *
from django.shortcuts import render, get_object_or_404



def get_connection(profile_id_1, profile_id_2):
    current_profile = get_object_or_404(Profile, id=profile_id_1)
    target_profile = get_object_or_404(Profile, id=profile_id_2)

    connection = Connection.objects.filter(
            models.Q(profile1 = current_profile, profile2 = target_profile) |
            models.Q(profile1 = target_profile, profile2 = current_profile)
        ).first()
    
    if connection:
        return connection
    else:
        return None