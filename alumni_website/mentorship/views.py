from django.shortcuts import render, get_object_or_404
from .models import *
from profiles.models import Profile
import datetime
import json
from django.http import JsonResponse, Http404
from .utils import get_mentor_match
from messaging.utils import create_chat_room
from notifications.notifications import MentorAcceptedNotification, MentorActivationNotification, MentorRequestNotification, send_notification
from profiles.models import Skill
from ai.classifier import predict_category_skill

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Handles mentor sign up logic
# On post: collects mentor details from form and creates a mentor object 
# On get: Prepares the form for mentor sign up by prefilling data available
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

        # for i in range(3):
        #     skill = MentorSkills(mentor = mentor, skill = skills[i])
        #     skill.save()

        skill_objs = list(request.user.profile.skills.all())
        for i in range(3):
            skill_objs[0].skill = skills[i]
            skill_objs[0].category = list(predict_category_skill(skills[i]))[0]
            skill_objs[0].save()
            skill_objs.remove(skill_objs[0])

        notification = MentorActivationNotification(receiver=request.user)
        send_notification(notification)

        return render(request, 'mentorship/mentor_signup.html', {
            "message": "You are now a Mentor :)"
        })

    mentors = Mentor.objects.all()
    is_mentor = False
    for mentor in mentors:
        if request.user == mentor.user:
            print(mentor.user)
            is_mentor = True
            break

    mentor_obj = Mentor.objects.filter(user = request.user).exists()
    is_mentor = True if mentor_obj else False

    skills = Skill.objects.distinct("skill")[:10]

    user_skills = list(request.user.profile.skills.all())

    profile = Profile.objects.get(user = request.user)

    return render(request, "mentorship/mentor_signup.html", {
        "skills": skills,
        "profile": profile,
        "is_mentor": is_mentor,
        "user_skills": user_skills,
    })

# Handles mentee's request to match with mentor
# Creates MentorMatch object to intitiate the request
@login_required
def mentor_match(request):
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

            notification = MentorRequestNotification(receiver=match.mentor.user, sender=request.user)
            send_notification(notification)

            return JsonResponse({"status": "success", "message": "Connected", "accepted": accepted})
        
    else:
        return JsonResponse({"status": "error", "message": "Not post request"})
    
# Handles the Mentor dashboard view
# Retrieves request data: accepted requests, total requests, declined requests and the count for each
@login_required
def mentor_dashboard(request):
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

# Allows mentor to accept mentee's request
@login_required
def accept_mentor(request, match_id, mentor_id):
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = True
        match.save()
        create_chat_room(request.user, match.mentee)

        notification = MentorAcceptedNotification(receiver=match.mentee, sender=request.user)
        send_notification(notification)

        return redirect("mentor_dashboard")
    else:
        raise Http404
    
# Allows mentor to decline mentee's request
@login_required
def decline_mentor(request, match_id, mentor_id):
    if request.user.id == mentor_id:
        match = MentorMatch.objects.get(id = match_id)
        match.accept = False
        match.save()

        return redirect("mentor_dashboard")