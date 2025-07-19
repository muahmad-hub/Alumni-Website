from django.shortcuts import render
from .models import *
from mentorship.models import MentorMatch, Mentor
import json
from django.forms.models import model_to_dict

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

        ALLOWED_FIELDS = {"name", "graduation_year", "university", "about_me", "career", "location", "role", "employer"}

        if field in ALLOWED_FIELDS and hasattr(profile, field):
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
                
            if field == "employer" or field == "job":
                setattr(profile, "has_job", "True")
                profile.save()

            setattr(profile, field, value)
            profile.save()
            return JsonResponse({"status": "success", "message": f"{field} updated."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
        
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "profiles/profile.html", {
        "profile": profile,
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
