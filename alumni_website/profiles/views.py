from django.shortcuts import render
from .models import *
from mentorship.models import MentorMatch, Mentor
import json
from django.forms.models import model_to_dict
from ai.classifier import predict_category_goal, predict_category_skill

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        profile = Profile.objects.get(user=request.user)

        ALLOWED_FIELDS = {"name", "graduation_year", "university", "about_me", "career", "location", "role", "employer", "university_location", "skills", "goals", "education_level"}

        if field in ALLOWED_FIELDS:
            if field == "graduation_year":
                try:
                    value = int(value)

                    if value < 2021 or value > 2040:
                        return JsonResponse({
                        "status": "error",
                        "message": "Graduation year must be 2021 or greater.",
                    }, status=400)
                except (ValueError, TypeError):
                    return JsonResponse({
                        "status": "error",
                        "message": "Graduation year must be a valid number.",
                    }, status=400)
            
            if field == "skills":
                if len(value) != 3:
                    return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
                for skill in value:
                    skill = Skill.objects.create(profile = profile, skill = skill, skill_category = predict_category_skill(skill)[0])

            if field == "goals":
                if len(value) != 3:
                    return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
                for goal in value:
                    goal = Goal.objects.create(profile = profile, goal = goal, goal_category = predict_category_goal(goal)[0])
                
            if field == "employer" or field == "job":
                setattr(profile, "has_job", "True")
                profile.save()

            if field != "skills" and field != "goals":
                setattr(profile, field, value)
                profile.save()    
            return JsonResponse({"status": "success", "message": f"{field} updated."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
        
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(profile = profile)
    goals = Goal.objects.filter(profile = profile)
    return render(request, "profiles/profile.html", {
        "profile": profile,
        "skills": skills,
        "goals": goals,
    })

@login_required
def get_profile_info(request):
    profile = Profile.objects.get(user = request.user)
    data = model_to_dict(profile)
    return JsonResponse(data)

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "profiles/edit_profile.html", {
        "profile": profile,
    })

@login_required
def view_profile(request, id):
    profile = Profile.objects.get(user = Users.objects.get(id = id))
    is_match = True
    try:
        match = MentorMatch.objects.get(mentor=Mentor.objects.get(user=Users.objects.get(id=id)), mentee=request.user)
        if match.accept == False:
            is_match = False
    except MentorMatch.DoesNotExist:
        is_match = False

    return render(request, "profiles/view_profile.html", {
        "profile": profile,
        "is_match": is_match,
    })
