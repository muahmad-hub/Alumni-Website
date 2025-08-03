from django.shortcuts import render
from .models import *
import json
from django.forms.models import model_to_dict
from ai.classifier import predict_category_goal, predict_category_skill
from django.urls import reverse
from urllib.parse import urlencode
from mentorship.utils import get_mentor_match
from mentorship.models import Mentor
from .utils import get_connection

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        profile = Profile.objects.get(user=request.user)

        ALLOWED_FIELDS = {"name", "graduation_year", "university", "about_me", "major_uni", "location", "role", "employer", "university_location", "skills", "goals", "education_level"}

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

def redirect_to_profile_with_message(message):
    query_params = urlencode({"message": message})
    profile_url = reverse("profile")
    return redirect(f"{profile_url}?{query_params}")

@login_required
def view_profile(request, id):
    view_type = request.GET.get('view')

    profile = Profile.objects.get(user = Users.objects.get(id = id))
    skills = Skill.objects.filter(profile = profile)

    connection = get_connection(request.user.profile.id, profile.id)
    mentor_match = get_mentor_match(request.user.id, profile.user.id)

    mentors = Mentor.objects.filter(user = Users.objects.get(id = profile.user.id))

    if mentors:
        mentor_match = get_mentor_match(request.user.id, profile.user.id)
        mentor_exists = True
    else:
        mentor_exists = False


    return render(request, "profiles/view_profile.html", {
        "profile": profile,
        "skills": skills,
        "connection": connection,
        "mentor_match": mentor_match,
        "mentor_exists": mentor_exists,
        "view_type": view_type
    })

@login_required
def edit_personal_section(request):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "location": request.POST.get("location"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        if not data["first_name"] or not data["last_name"] or not data["email"] or not data["date_of_birth"] or not data["location"]:
            return redirect_to_profile_with_message("All fields are required")
        
        for field, value in data.items():
            if field == "date_of_birth":
                try:
                    setattr(profile, field, value)
                except:
                    return redirect_to_profile_with_message("Date of Birth must be in the format YYYY-MM-DD")
            elif field == "email":
                setattr(profile.user, field, value)
            else:
                setattr(profile, field, value)

        profile.user.save()
        profile.save()

    return redirect("profile")

@login_required
def edit_bio_section(request):
    if request.method == "POST":
        data = {
            "about_me": request.POST.get("about_me"),
        }
        profile = get_object_or_404(Profile, user = request.user)

        if not data["about_me"]:
            return redirect_to_profile_with_message("About Me section cannot be empty")
        setattr(profile, "about_me", data["about_me"])

        profile.save()
    return redirect("profile")

@login_required
def edit_education_section(request):
    if request.method == "POST":
        data = {
            "graduation_year": request.POST.get("graduation_year"),
            "education_level": request.POST.get("education_level"),
            "university": request.POST.get("university"),
            "university_location": request.POST.get("university_location"),
            "major_uni": request.POST.get("major_uni"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        try:
            graduation_year = int(data["graduation_year"])
            data["graduation_year"] = graduation_year
        except (ValueError, TypeError):
            return redirect_to_profile_with_message("Graduation year must be a valid number")
        if not 2021 < data["graduation_year"] < 2040:
            return redirect_to_profile_with_message("Gradutaion year must be a valid year")
        if not data["graduation_year"] or not data["education_level"] or not data["university"] or not data["university_location"] or not data["major_uni"]:
            return redirect_to_profile_with_message("All fields are required")
        
        for field, value in data.items():
            setattr(profile, field, value)

        profile.save()
    return redirect("profile")

@login_required
def edit_skills_section(request):
    if request.method == "POST":
        data = {
            "skills": request.POST.getlist("skills")
        }

        profile = get_object_or_404(Profile, user = request.user)

        if len(data["skills"]) != 3:
            return redirect_to_profile_with_message("You must add 3 skills")
        
        skills = Skill.objects.filter(profile=profile)[:3]

        for value, field in zip(data["skills"], skills):
            field.skill = value
            field.skill_category = predict_category_skill(value)[0]
            field.save()

    return redirect("profile")

@login_required
def edit_goals_section(request):
    if request.method == "POST":
        data = {
            "goals": request.POST.getlist("goals")
        }

        profile = get_object_or_404(Profile, user = request.user)

        if len(data["goals"]) != 3:
            return redirect_to_profile_with_message("You must add 3 goals")
        
        goals = Goal.objects.filter(profile=profile)[:3]

        for value, field in zip(data["goals"], goals):
            field.goal = value
            field.goal_category = predict_category_goal(value)[0]
            field.save()

    return redirect("profile")

@login_required
def edit_career_section(request):
    if request.method == "POST":
        data = {
            "role": request.POST.get("role"),
            "employer": request.POST.get("employer"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        if not data["role"].strip() or not data["employer"].strip():
            return redirect_to_profile_with_message("All fields are required")

        for field, value in data.items():
            setattr(profile, field, value)
        setattr(profile, "has_job", True)

        profile.save()

    return redirect("profile")

@login_required
def edit_employment_status(request):
    if request.method =="POST":
        data = json.loads(request.body)
        has_job = data.get("has_job")

        profile = get_object_or_404(Profile, user = request.user)

        if has_job in ["True", "False"]:
            profile.has_job = has_job
            profile.save()
            return JsonResponse({"status": "success", "message": "Employment status updated."})
    return redirect("profile")

@login_required
def connect(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile_id = data.get("profile_id")
        profile = get_object_or_404(Profile, id=profile_id)
        if not profile_id:
            return JsonResponse({"status": "error", "message": "Profile ID is required"})
        
        connection = get_connection(request.user.profile.id, profile_id)

        if connection is not None:
            connection.delete()
            return JsonResponse({"status": "success", "message": "Disconnected"})
        else:
            new_connection = Connection.objects.create(profile1=request.user.profile, profile2=profile)
            accepted = new_connection.accepted
            return JsonResponse({"status": "success", "message": "Connected", "accepted": str(accepted)})
