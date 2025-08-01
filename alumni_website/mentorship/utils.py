from django.shortcuts import get_object_or_404
from .models import *


def get_mentor_match(user_id_1, mentor_user_id):

    mentor = get_object_or_404(Mentor, user = mentor_user_id)
    mentee = get_object_or_404(Users, id = user_id_1)

    mentor_match = MentorMatch.objects.filter(mentor = mentor, mentee = mentee)
    
    if mentor_match:
        return mentor_match
    else:
        return None
    

def is_mentor(user1, user2):
    try:
        mentor_obj = Mentor.objects.get(user=user1)
        match = MentorMatch.objects.filter(mentor=mentor_obj, mentee=user2, accept=True).first()
        if match:
            return {
                "is_mentor": True,
                "mentor": user1,
                "mentee": user2
            }

        mentor_obj = Mentor.objects.get(user=user2)
        match = MentorMatch.objects.filter(mentor=mentor_obj, mentee=user1, accept=True).first()
        if match:
            return {
                "is_mentor": True,
                "mentor": user2,
                "mentee": user1
            }

    except Mentor.DoesNotExist:
        pass

    return {
            "is_mentor": False,
            "mentor": None,
            "mentee": None
            }