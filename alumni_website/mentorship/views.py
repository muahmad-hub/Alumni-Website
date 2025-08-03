from django.shortcuts import render, get_object_or_404
from .models import *
from profiles.models import Profile
import datetime
import json
from django.http import JsonResponse, Http404
from .utils import get_mentor_match
from messaging.utils import create_chat_room



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
            skill = MentorSkills(mentor = mentor, skill = skills[i])
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

    skills = MentorSkills.objects.distinct("skill")[:10]

    profile = Profile.objects.get(user = request.user)

    return render(request, "mentorship/mentor_signup.html", {
        "skills": skills,
        "profile": profile,
        "is_mentor": is_mentor,
    })

@login_required
def mentor_match(request):
    """
    Handles mentee's request to match with a mentor.
    Creates a MentorMatch object with accept=None (pending).

    Args:
        request (HttpRequest): The HTTP request object.
        mentor_id (int): The User ID of the mentor to match with.

    Returns:
        HttpResponse: Redirects to the mentor's profile page after request.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")

        if not id:
            return JsonResponse({"status": "error", "message": "User ID is required"})
        
        mentor_match = get_mentor_match(request.user.id, id)

        if mentor_match is not None:
            mentor_match.delete()
            return JsonResponse({"status": "success", "message": "Deleted"})
        else: 
            match = MentorMatch(mentor = Mentor.objects.get(user = Users.objects.get(id=id)), mentee = request.user)
            match.save()
            accepted = match.accept
            return JsonResponse({"status": "success", "message": "Connected", "accepted": accepted})
        
    else:
        return JsonResponse({"status": "error", "message": "Not post request"})
    
@login_required
def mentor_dashboard(request):
    """
    Displays the mentor dashboard with pending and accepted mentorship requests.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered mentor dashboard page.
    """
    mentor = get_object_or_404(Mentor, user = request.user)

    all_requests = MentorMatch.objects.filter(mentor = mentor).all()
    accepted_requests = all_requests.filter(accept = True)
    declined_requests = all_requests.filter(accept = False)

    all_requests_count = all_requests.count()
    accepted_requests_count = accepted_requests.count()
    declined_requests_count = declined_requests.count()

    return render(request, "mentorship/mentor_dashboard.html", {
        "all_requests": all_requests,
        "accepted_requests": accepted_requests,
        "declined_requests": declined_requests,

        "all_requests_count": all_requests_count,
        "accepted_requests_count": accepted_requests_count,
        "declined_requests_count": declined_requests_count,
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
        create_chat_room(request.user, match.mentee)
        return redirect("mentor_dashboard")
    else:
        raise Http404
    
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