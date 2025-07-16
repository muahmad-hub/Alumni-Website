from django.shortcuts import render
from django.contrib import messages
from .models import *
import json
from django.templatetags.static import static

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    messages.success(request, "Welcome to the alumni site!")
    return render(request, "alumni/home.html")  

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

def logout_view(request):
    logout(request)
    return render(request, "alumni/login.html")

def profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        profile = Profile.objects.get(user=request.user)

        ALLOWED_FIELDS = {"name", "graduation_year", "university", "about_me", "career", "location"}

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
            setattr(profile, field, value)
            profile.save()
            return JsonResponse({"status": "success", "message": f"{field} updated."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
        
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "alumni/profile.html", {
        "profile": profile,
    })

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "alumni/edit_profile.html", {
        "profile": profile,
    })

def directory(request):
    return render(request, "alumni/directory.html")

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

def view_profile(request, id):
    profile = Profile.objects.get(user = Users.objects.get(id = id))
    return render(request, "alumni/view_profile.html", {
        "profile": profile,
    })

