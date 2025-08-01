from django.shortcuts import render
from django.contrib import messages
from .models import *
from mentorship.models import MentorMatch
from profiles.models import Profile

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    # messages.success(request, "Welcome to the alumni site!")

    num_alumni = Users.objects.all().count
    num_countries = Profile.objects.exclude(location__isnull=True).exclude(location__exact='').values("location").count()
    num_careers = Profile.objects.exclude(major_uni__isnull=True).exclude(major_uni__exact='').values("major_uni").count()

    pending_requests = MentorMatch.objects.filter(mentee=request.user, accept=True)

    return render(request, "core/home.html", {
        "pending_requests": pending_requests,
        "num_alumni": num_alumni,
        "num_countries": num_countries,
        "num_careers": num_careers,
    })  