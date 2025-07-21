from django.shortcuts import render
from django.contrib import messages
from .models import *
from mentorship.models import MentorMatch

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # messages.success(request, "Welcome to the alumni site!")

    pending_requests = MentorMatch.objects.filter(mentee=request.user, accept=True)

    return render(request, "core/home.html", {
        "pending_requests": pending_requests,
    })  