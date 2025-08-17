from django.shortcuts import render
from .models import *
from profiles.models import Profile, UserAlumniRecommendation
from mentorship.models import Mentor
from django.templatetags.static import static
from django.db.models import Q
from .utils import get_directory_filters
from django.utils import timezone
from datetime import timedelta
from ai.recommender import optimised_recommend, populate_cache, simple_recommend
from django.core.cache import cache
from core.models import RecommendationSystem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# View to handle alumni directory
# 'view_type' in context is set to alumni so that Connect buttons are shown when profiles are visited instead of Mentor Connect buttons 
@login_required
def directory(request):
    context = get_directory_filters()
    context["view_type"] = "alumni"

    return render(request, "directory/directory.html", context)

# View to handle recommendation 
# Checks switch in database to see which recommendation algorithm to use
# Checks from database the last time user was recommended to ensure users are only recommended once a week so that the feature doesn't become annoying
# Populates cache if not populated or if expired with data used by recommendation system 
@login_required
def alumni_directory_recommend(request):

    context = {}

    instance = RecommendationSystem.objects.all().first()
    if instance and instance.recommendation_system:
        system_choice = instance.recommendation_system
    else:
        context["show_modal"] = False
        return JsonResponse(context)


    profile = request.user.profile
    session_key = "last_seen_recommendation_id"

    try:
        user_recommendation = UserAlumniRecommendation.objects.get(profile=profile)
    except UserAlumniRecommendation.DoesNotExist:
        return JsonResponse({"show_modal": False})

    time_difference = timezone.now() - user_recommendation.timestamp

    if time_difference > timedelta(days=7) or not user_recommendation.recommended_profile:
        if not cache.get("all_profile_data"):
            populate_cache()

        if system_choice == "OptimisedAlgorithm":
            recommend_data = optimised_recommend(request.user.profile.id)
        elif system_choice == "SimpleAlgorithm":
            recommend_data = simple_recommend(request.user.profile.id)

        print(f"Request profile id: {request.user.profile.id}")
        print(f"Recommended data: {recommend_data}")
        if recommend_data:
            recommended_profile = Profile.objects.get(id = recommend_data["user"])
            print("Got recommendation profile")
            print(recommended_profile)

            user_recommendation.recommended_profile = recommended_profile
            user_recommendation.compatibility_score = recommend_data["f_n_score"]
            user_recommendation.timestamp = timezone.now()
            user_recommendation.save()

            percentage = recommend_data["f_n_score"] * 100

            print("Compatibility Score")
            print(percentage)

            context["first_name"] = recommended_profile.first_name
            context["last_name"] = recommended_profile.last_name
            context["id"] = recommended_profile.user.id
            context["percentage"] = percentage
        

            if request.session.get(session_key) != recommended_profile.id:
                context["show_modal"] = True
                print("Show modal is true")
                request.session[session_key] = recommended_profile.id
            else:
                context["show_modal"] = False
                print("ERROR: Show modal is false, not in session key")
        else:
            context["first_name"] = None
            context["last_name"] = None
            context["id"] = None
            print("ERROR: Show modal is false, no recommended data")
            context["show_modal"] = False

    else:
        recommended_profile = user_recommendation.recommended_profile
        context["first_name"] = recommended_profile.first_name
        context["last_name"] = recommended_profile.last_name
        context["id"] = recommended_profile.user.id
        context["percentage"] = user_recommendation.compatibility_score * 100

        if request.session.get(session_key) != recommended_profile.id:
            context["show_modal"] = True
            request.session[session_key] = recommended_profile.id
        else:
            context["show_modal"] = False

    return JsonResponse(context)
    
# Returns alumni based on the search queries in the directory
# Only alumni with First name added on profile are shown in results
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
            "education_level": alum.education_level,
        }
        results.append(result)
    
    return JsonResponse({
        "results": results,
    })

# View to handle mentor directory
# 'view_type' in context is set to mentor so that Mentor Connect buttons are shown when profiles are visited instead of Connect buttons 
@login_required
def mentor_directory(request):
    context = get_directory_filters()
    context["view_type"] = "mentor"

    return render(request, "directory/mentor_directory.html", context)

# Returns mentor based on the search queries in the directory
# Filters mentors whose profile's main information is complete
@login_required
def mentor_search_directory(request):

    query = request.GET.get("q", "").lower().strip()
    batch_year = request.GET.get("batch_year", "")
    university = request.GET.get("uni", "")

    filter_conditions = Q()

    if query:
        filter_conditions &= Q(user__profile__skills__skill__icontains=query)

    if batch_year and batch_year != "Batch Year":
        filter_conditions &= Q(user__profile__graduation_year=batch_year)

    if university and university != "University":
        filter_conditions &= Q(user__profile__university__icontains=university)
        
    alumni = Mentor.objects.filter(filter_conditions).exclude(user__profile__skills__isnull=True).distinct()

    results = []

    for alum in alumni:

        skills_list = []
        for skill in alum.user.profile.skills.all():
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
