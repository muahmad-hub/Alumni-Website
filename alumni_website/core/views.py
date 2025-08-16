from django.shortcuts import render
from .models import *
from profiles.models import Profile
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render

def home(request):
    # messages.success(request, "Welcome to the alumni site!")

    num_alumni = Users.objects.all().count
    num_countries = Profile.objects.exclude(location__isnull=True).exclude(location__exact='').values("location").count()
    num_careers = Profile.objects.exclude(major_uni__isnull=True).exclude(major_uni__exact='').values("major_uni").count()

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if not profile.about_me or not profile.education_level or not profile.skills:
            profile_url = reverse("profile")
            messages.success(request, f"Hi there! Your profile seems incomplete. Please check your profile in 'Your Space'")

    return render(request, "core/home.html", {
        "num_alumni": num_alumni,
        "num_countries": num_countries,
        "num_careers": num_careers,
    })  