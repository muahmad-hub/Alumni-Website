from django.shortcuts import render
from .models import *
from profiles.models import Profile
from mentorship.models import Mentor
from django.templatetags.static import static
from django.db.models import Q
from .utils import get_directory_filters

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def directory(request):
    context = get_directory_filters()
    context["view_type"] = "alumni"

    return render(request, "directory/directory.html", context)
    
@login_required
def search_directory(request):
    query = request.GET.get("q", "").lower().strip()
    batch_year = request.GET.get("batch_year", "")
    university = request.GET.get("uni", "")

    filter_conditions = Q()

    if query:
        filter_conditions &= Q(first_name__icontains=query) | Q(last_name__icontains=query)

    if batch_year and batch_year != "Batch Year" and batch_year.isdigit():
        filter_conditions &= Q(graduation_year=int(batch_year))

    if university and university != "University":
        filter_conditions &= Q(university__icontains=university)
        
    alumni = Profile.objects.filter(filter_conditions).exclude(first_name__isnull=True).distinct()

    results = []

    for alum in alumni:
        if all([alum.graduation_year, alum.major_uni, alum.university]):
            result = {
                "id": alum.user.id,
                "first_name": alum.first_name,
                "last_name": alum.last_name,
                "profile_url": alum.profile_url if alum.profile_url else static("images/profile_image.jpg"),
                "graduation_year": alum.graduation_year,
                "major_uni": alum.major_uni,
                "university": alum.university,
                "has_job": alum.has_job,
                "employer": alum.employer,
                "role": alum.role,
            }
            results.append(result)
    
    return JsonResponse({
        "results": results,
    })

@login_required
def mentor_directory(request):
    context = get_directory_filters()
    context["view_type"] = "mentor"

    return render(request, "directory/mentor_directory.html", context)

@login_required
def mentor_search_directory(request):

    query = request.GET.get("q", "").lower().strip()
    batch_year = request.GET.get("batch_year", "")
    university = request.GET.get("uni", "")

    filter_conditions = Q()

    if query:
        filter_conditions &= Q(skills__skill__icontains=query)

    if batch_year and batch_year != "Batch Year":
        filter_conditions &= Q(user__profile__graduation_year=batch_year)

    if university and university != "University":
        filter_conditions &= Q(user__profile__university__icontains=university)
        
    alumni = Mentor.objects.filter(filter_conditions).exclude(skills__isnull=True).distinct()

    results = []

    for alum in alumni:

        skills_list = []
        for skill in alum.user.mentor.skills.all():
            skills_list.append(skill.skill)

        if all([alum.user.profile.graduation_year, alum.user.profile.major_uni, alum.user.profile.university]):
            result = {
                "id": alum.user.id,
                "first_name": alum.user.profile.first_name,
                "last_name": alum.user.profile.last_name,
                "skills": skills_list,
                "profile_url": alum.user.profile.profile_url if alum.user.profile.profile_url else static("/images/profile_image.jpg"),
                "graduation_year": alum.user.profile.graduation_year,
                "major_uni": alum.user.profile.major_uni,
                "university": alum.user.profile.university,
                "has_job": alum.user.profile.has_job,
                "employer": alum.user.profile.employer,
                "role": alum.user.profile.role,
            }
            results.append(result)
    

    return JsonResponse({
        "results": results,
    })
