from django.shortcuts import render
from .models import *
from profiles.models import Profile
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def mentor_signup(request):
    """
    Handles mentor signup process:
    - On POST: Collects mentor details from the form, creates a Mentor object, and saves up to 3 skills.
    - On GET: Checks if the user is already a mentor, fetches distinct skills, and renders the signup page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered mentor signup page or success message.
    """
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

        return render(request, 'mentorship/mentor_signup.html', {
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

    return render(request, "mentorship/mentor_signup.html", {
        "skills": skills,
        "profile": profile,
        "is_mentor": is_mentor,
    })

@login_required
def mentor_match(request, mentor_id):
    """
    Handles mentee's request to match with a mentor.
    Creates a MentorMatch object with accept=None (pending).

    Args:
        request (HttpRequest): The HTTP request object.
        mentor_id (int): The ID of the mentor to match with.

    Returns:
        HttpResponse: Redirects to the mentor's profile page after request.
    """
    if request.method == "POST":
        match = MentorMatch(mentor = Mentor.objects.get(user = Users.objects.get(id=mentor_id)), mentee = request.user, accept=None)
        match.save()

        return redirect('view_profile', id=mentor_id)

@login_required
def mentor_dashboard(request):
    """
    Displays the mentor dashboard with pending and accepted mentorship requests.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered mentor dashboard page.
    """
    requests_none = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=None)
    requests_true = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=True)
    return render(request, "mentorship/mentor_dashboard.html", {
        "requests_none": requests_none,
        "requests_true": requests_true,
        "profile": Profile.objects.get(user = request.user),
    })

@login_required
def accept_mentor(request, match_id, mentor_id):
    """
    Allows a mentor to accept a mentorship request.

    Args:
        request (HttpRequest): The HTTP request object.
        match_id (int): The ID of the MentorMatch object.
        mentor_id (int): The ID of the mentor (should match the logged-in user).

    Returns:
        HttpResponse: Redirects to the mentor dashboard after accepting.
    """
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = True
        match.save()

        return redirect("mentor_dashboard")
    
@login_required
def decline_mentor(request, match_id, mentor_id):
    """
    Allows a mentor to decline a mentorship request.

    Args:
        request (HttpRequest): The HTTP request object.
        match_id (int): The ID of the MentorMatch object.
        mentor_id (int): The ID of the mentor (should match the logged-in user).

    Returns:
        HttpResponse: Redirects to the mentor dashboard after declining.
    """
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = False
        match.save()

        return redirect("mentor_dashboard")