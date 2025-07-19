from django.shortcuts import render
from django.contrib import messages
from .models import *
import datetime
import json
from django.templatetags.static import static
from django.forms.models import model_to_dict
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    messages.success(request, "Welcome to the alumni site!")

    pending_requests = MentorMatch.objects.filter(mentee=request.user, accept=True)

    return render(request, "alumni/home.html", {
        "pending_requests": pending_requests,
    })  

def login_view(request):
    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "alumni/login.html")
    else:
        return render(request, "alumni/login.html")

def sign_up(request):
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                messages.error(request, "Passwords must match")
                return render(request, "alumni/sign_up.html")

            try:
                user = Users.objects.create_user(email = email, username = email, password = password)
                user.save()
            except IntegrityError:
                messages.error(request, "Email is already registered")
                return render(request, "alumni/sign_up.html")
            
            profile = Profile.objects.create(
            user=user,
            name=None,
            graduation_year=None,
            university=None,
            about_me=None,
            career=None,
            location=None,
            profile_url=None,
            )

            login(request, user)
            return redirect('home')
        else:
            return render(request, "alumni/sign_up.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "alumni/login.html")

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
    return render(request, "alumni/profile.html", {
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

    return render(request, "alumni/edit_profile.html", {
        "profile": profile,
    })

@login_required
def directory(request):
    return render(request, "alumni/directory.html")

@login_required
def search_directory(request):
    query = request.GET.get("q", "").strip()

    if query:
        alumni = Profile.objects.filter(name__icontains=query)
    else:
        alumni = Profile.objects.all()

    results = []

    for alum in alumni:
        if all([alum.graduation_year, alum.career, alum.university]):
            result = {
                "id": alum.user.id,
                "name": alum.name,
                "profile_url": alum.profile_url if alum.profile_url else static("alumni/images/profile_image.jpg"),
                "graduation_year": alum.graduation_year,
                "career": alum.career,
                "university": alum.university,
            }
            results.append(result)
    

    return JsonResponse({
        "results": results,
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

    return render(request, "alumni/view_profile.html", {
        "profile": profile,
        "is_match": is_match,
    })

@login_required
def mentor_directory(request):
    years = Profile.objects.filter(graduation_year__isnull=False).values("graduation_year").distinct().order_by('-graduation_year')
    university = Profile.objects.filter(university__isnull=False).values("university").distinct()

    return render(request, "alumni/mentor_directory.html", {
        "years": years,
        "university": university,
    })

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
        
    alumni = Mentor.objects.filter(filter_conditions).distinct()

    results = []

    for alum in alumni:

        skills_list = []
        for skill in alum.user.mentor.skills.all():
            skills_list.append(skill.skill)

        if all([alum.user.profile.graduation_year, alum.user.profile.career, alum.user.profile.university]):
            result = {
                "id": alum.user.id,
                "name": alum.user.profile.name,
                "skills": skills_list,
                "profile_url": alum.user.profile.profile_url if alum.user.profile.profile_url else static("alumni/images/profile_image.jpg"),
                "graduation_year": alum.user.profile.graduation_year,
                "career": alum.user.profile.career,
                "university": alum.user.profile.university,
                "has_job": alum.user.profile.has_job,
                "employer": alum.user.profile.employer,
                "role": alum.user.profile.role,
            }
            results.append(result)
    

    return JsonResponse({
        "results": results,
    })

@login_required
def mentor_signup(request):
    if request.method == 'POST':
        industry = request.POST.get("industry")
        experience = request.POST.get("experience")
        skills = []
        skills.append(request.POST.get("skill1"))
        skills.append(request.POST.get("skill2"))
        skills.append(request.POST.get("skill3"))
        availability = request.POST.get("availability")

        mentor = Mentor(user = request.user, availability = availability, industry = industry, experience = experience, created_at = datetime.datetime.now(), updated_at = datetime.datetime.now())
        mentor.save()
        for i in range(3):
            skill = Skills(mentor = mentor, skill = skills[i])
            skill.save()

        return render(request, 'alumni/mentor_signup.html', {
            "message": "You are now a Mentor :)"
        })

    mentors = Mentor.objects.all()
    print(mentors)
    is_mentor = False
    for mentor in mentors:
        if request.user == mentor.user:
            print(mentor.user)
            is_mentor = True
            break

    skills = Skills.objects.distinct("skill")[:10]

    profile = Profile.objects.get(user = request.user)

    return render(request, "alumni/mentor_signup.html", {
        "skills": skills,
        "profile": profile,
        "is_mentor": is_mentor,
    })

@login_required
def mentor_match(request, mentor_id):
    if request.method == "POST":
        match = MentorMatch(mentor = Mentor.objects.get(user = Users.objects.get(id=mentor_id)), mentee = request.user, accept=None)
        match.save()

        return redirect('view_profile', id=mentor_id)

@login_required
def mentor_dashboard(request):
    requests_none = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=None)
    requests_true = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=True)
    return render(request, "alumni/mentor_dashboard.html", {
        "requests_none": requests_none,
        "requests_true": requests_true,
        "profile": Profile.objects.get(user = request.user),
    })

@login_required
def accept_mentor(request, match_id, mentor_id):
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = True
        match.save()

        return redirect("mentor_dashboard")
    
@login_required
def decline_mentor(request, match_id, mentor_id):
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = False
        match.save()

        return redirect("mentor_dashboard")