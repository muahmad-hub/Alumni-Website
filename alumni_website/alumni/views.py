from django.shortcuts import render
from django.contrib import messages
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
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
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "alumni/profile.html", {
        "profile": profile,
    })


