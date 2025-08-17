from django.shortcuts import render
from .models import *
import json
from ai.classifier import predict_category_goal, predict_category_skill
from django.urls import reverse
from urllib.parse import urlencode
from mentorship.utils import get_mentor_match
from mentorship.models import Mentor
from .utils import get_connection, num_connections
from messaging.utils import create_chat_room
from notifications.notifications import ConnectRequestNotification, ConnectAcceptedNotification, send_notification

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Countries list: used in forms where users enter location
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See",
    "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan",
    "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway",
    "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka",
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States of America",
    "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe"
]

# Opens user's own profile page
# Allows edit to profile information
# Stores new profile data when users update it on the webpage
@login_required
def profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        profile = Profile.objects.get(user=request.user)

        # Validation check to ensure users don't manipulate and try to write to a new field
        ALLOWED_FIELDS = {"name", "graduation_year", "university", "about_me", "major_uni", "location", "role", "employer", "university_location", "skills", "goals", "education_level"}

        if field in ALLOWED_FIELDS:
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
            
            if field == "skills":
                if len(value) != 3:
                    return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
                for skill in value:
                    skill = Skill.objects.create(profile = profile, skill = skill, skill_category = predict_category_skill(skill)[0])

            if field == "goals":
                if len(value) != 3:
                    return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
                for goal in value:
                    goal = Goal.objects.create(profile = profile, goal = goal, goal_category = predict_category_goal(goal)[0])
                
            if field == "employer" or field == "job":
                setattr(profile, "has_job", "True")
                profile.save()

            if field != "skills" and field != "goals":
                setattr(profile, field, value)
                profile.save()    
            return JsonResponse({"status": "success", "message": f"{field} updated."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid field."}, status=400)
        
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(profile = profile)
    goals = Goal.objects.filter(profile = profile)
    connection_requests = Connection.objects.filter(profile2 = profile, accepted=None)
    num_of_connections = num_connections(profile)

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "skills": skills,
        "goals": goals,
        "connection_requests": connection_requests,
        "num_of_connections": num_of_connections,
        "countries": countries,
    })

def redirect_to_profile_with_message(message):
    query_params = urlencode({"message": message})
    profile_url = reverse("profile")
    return redirect(f"{profile_url}?{query_params}")

# Opens user profile when other users want to view it
@login_required
def view_profile(request, id):
    view_type = request.GET.get('view')

    profile = Profile.objects.get(user = Users.objects.get(id = id))
    skills = Skill.objects.filter(profile = profile)

    connection = get_connection(request.user.profile.id, profile.id)
    num_of_connections = num_connections(profile)
    
    try:
        mentors = Mentor.objects.get(user=profile.user)
        mentor_exists = True
        mentor_match = get_mentor_match(request.user.id, profile.user.id)
    except Mentor.DoesNotExist:
        mentors = None
        mentor_exists = False
        mentor_match = None


    return render(request, "profiles/view_profile.html", {
        "profile": profile,
        "skills": skills,
        "connection": connection,
        "mentor_match": mentor_match,
        "mentor_exists": mentor_exists,
        "view_type": view_type,
        "num_of_connections": num_of_connections
    })


# Handle user profile edits
# One view for each modal (Each profile section has a modal, for example, Personal section, bio, education)
@login_required
def edit_personal_section(request):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "location": request.POST.get("location"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        if not data["first_name"] or not data["last_name"] or not data["email"] or not data["date_of_birth"] or not data["location"]:
            return redirect_to_profile_with_message("All fields are required")
        
        for field, value in data.items():
            if field == "date_of_birth":
                try:
                    setattr(profile, field, value)
                except:
                    return redirect_to_profile_with_message("Date of Birth must be in the format YYYY-MM-DD")
            elif field == "email":
                setattr(profile.user, field, value)
            else:
                setattr(profile, field, value)

        profile.user.save()
        profile.save()

    return redirect("profile")

@login_required
def edit_bio_section(request):
    if request.method == "POST":
        data = {
            "about_me": request.POST.get("about_me"),
        }
        profile = get_object_or_404(Profile, user = request.user)

        if not data["about_me"]:
            return redirect_to_profile_with_message("About Me section cannot be empty")
        setattr(profile, "about_me", data["about_me"])

        profile.save()
    return redirect("profile")

@login_required
def edit_education_section(request):
    if request.method == "POST":
        data = {
            "graduation_year": request.POST.get("graduation_year"),
            "education_level": request.POST.get("education_level"),
            "university": request.POST.get("university"),
            "university_location": request.POST.get("university_location"),
            "major_uni": request.POST.get("major_uni"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        try:
            graduation_year = int(data["graduation_year"])
            data["graduation_year"] = graduation_year
        except (ValueError, TypeError):
            return redirect_to_profile_with_message("Graduation year must be a valid number")
        if not 2021 <= data["graduation_year"] < 2040:
            return redirect_to_profile_with_message("Gradutaion year must be a valid year")
        # if data["education_level"] == "Still in School":
        #     pass
        # elif not data["graduation_year"] or not data["education_level"] or not data["university"] or not data["university_location"] or not data["major_uni"]:
        #     return redirect_to_profile_with_message("All fields are required")
        
        for field, value in data.items():
            setattr(profile, field, value)

        profile.save()
    return redirect("profile")

@login_required
def edit_skills_section(request):
    if request.method == "POST":
        data = {
            "skills": request.POST.getlist("skills")
        }

        profile = get_object_or_404(Profile, user = request.user)

        if len(data["skills"]) != 3:
            return redirect_to_profile_with_message("You must add 3 skills")
        
        skills = Skill.objects.filter(profile=profile)[:3]

        for value, field in zip(data["skills"], skills):
            field.skill = value
            field.skill_category = predict_category_skill(value)[0]
            field.save()

    return redirect("profile")

@login_required
def edit_goals_section(request):
    if request.method == "POST":
        data = {
            "goals": request.POST.getlist("goals")
        }

        profile = get_object_or_404(Profile, user = request.user)

        if len(data["goals"]) != 3:
            return redirect_to_profile_with_message("You must add 3 goals")
        
        goals = Goal.objects.filter(profile=profile)[:3]

        for value, field in zip(data["goals"], goals):
            field.goal = value
            field.goal_category = predict_category_goal(value)[0]
            field.save()

    return redirect("profile")

@login_required
def edit_career_section(request):
    if request.method == "POST":
        data = {
            "role": request.POST.get("role"),
            "employer": request.POST.get("employer"),
        }

        profile = get_object_or_404(Profile, user = request.user)

        if not data["role"].strip() or not data["employer"].strip():
            return redirect_to_profile_with_message("All fields are required")

        for field, value in data.items():
            setattr(profile, field, value)
        setattr(profile, "has_job", True)

        profile.save()

    return redirect("profile")

@login_required
def edit_employment_status(request):
    if request.method =="POST":
        data = json.loads(request.body)
        has_job = data.get("has_job")

        profile = get_object_or_404(Profile, user = request.user)

        if has_job in ["True", "False"]:
            profile.has_job = has_job
            profile.save()
            return JsonResponse({"status": "success", "message": "Employment status updated."})
    return redirect("profile")

# Handles user's request to connect or disconnect with other user
# Creates a connection object if users are not connected
# Deletes connection object if users are connected
@login_required
def connect(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile_id = data.get("profile_id")
        profile = get_object_or_404(Profile, id=profile_id)

        if not profile_id:
            return JsonResponse({"status": "error", "message": "Profile ID is required"})
        
        connection = get_connection(request.user.profile.id, profile_id)

        if connection is not None:
            connection.delete()
            return JsonResponse({"status": "success", "message": "Disconnected"})
        else:
            new_connection = Connection.objects.create(profile1=request.user.profile, profile2=profile)
            accepted = new_connection.accepted
            if accepted is None:
                accepted_str = "Pending"
            elif accepted is True:
                accepted_str = "True"
            else:
                accepted_str = "False"

            notification = ConnectRequestNotification(receiver=profile.user, sender=request.user)
            send_notification(notification)

            return JsonResponse({"status": "success", "message": "Connected", "accepted": accepted_str})
    return JsonResponse({"status": "error", "message": "Method is not POST"})

@login_required
def accept_connection(request, user_id, action):
    if request.method == "POST":
        try:
            profile2 = get_object_or_404(Profile, user = request.user)
            user1 = get_object_or_404(Users, id = user_id)
            profile1 = get_object_or_404(Profile, user = user1)

            connection = get_object_or_404(Connection, profile1=profile1, profile2=profile2)

            if action == "accept":
                connection.accepted = True
                connection.save()
                print(connection)

                create_chat_room(request.user, user1)
                print("chat room created")

                notification = ConnectAcceptedNotification(receiver=user1, sender=request.user)
                send_notification(notification)

                return JsonResponse({'status': 'success', 'message': 'Connection accepted.'})
            else:
                connection.accepted = False
                connection.save()
                return JsonResponse({'status': 'success', 'message': 'Connection declined.'})

        except Exception:
            return JsonResponse({'status': 'error', 'message': str(Exception)})

# Handle weekly digest email preferences
@login_required
def yes_digest_email(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
            profile.send_digest_email = True
            profile.save()

            return JsonResponse({"status": "success", "message": "Email preference updated."})
        except:
            return JsonResponse({"status": "error", "message": "An error occured when trying to update"})
    return JsonResponse({"status": "error", "message": "Invalid request. Only POST accepted"})

@login_required
def no_digest_email(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
            profile.send_digest_email = False
            profile.save()

            return JsonResponse({"status": "success", "message": "Email preference updated."})
        except:
            return JsonResponse({"status": "error", "message": "An error occured when trying to update"})
    return JsonResponse({"status": "error", "message": "Invalid request. Only POST accepted"})
