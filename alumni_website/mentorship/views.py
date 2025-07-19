from django.shortcuts import render
from .models import *
from profiles.models import Profile
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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
    if request.method == "POST":
        match = MentorMatch(mentor = Mentor.objects.get(user = Users.objects.get(id=mentor_id)), mentee = request.user, accept=None)
        match.save()

        return redirect('view_profile', id=mentor_id)

@login_required
def mentor_dashboard(request):
    requests_none = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=None)
    requests_true = MentorMatch.objects.filter(mentor=Mentor.objects.get(user=request.user), accept=True)
    return render(request, "mentorship/mentor_dashboard.html", {
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