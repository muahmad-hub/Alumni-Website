from django.shortcuts import render
from django.contrib import messages
from core.models import Users
from profiles.models import Profile

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from .utils import send_activation_email_asynchronous

# Function used to get users IP address to log login attempts
def get_client_ip(request):
    # Gets IP from proxy server, else retrieves it manually
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Checks the number of attempts of the action (login/signup) to prevent Brute Force Attacks
# Attempts are stored in cache with the users IP address
def is_rate_limited(request, action='signup', limit=3, window=3600):
    ip = get_client_ip(request)
    cache_key = f"rate_limit_{action}_{ip}"
    
    attempts = cache.get(cache_key, 0)
    if attempts >= limit:
        return True
    
    cache.set(cache_key, attempts + 1, window)
    return False

def send_activation_email(user, request):
    try:
        # Random 32 string token is generated
        token = get_random_string(32)
        # Sets activation token as user's id and token
        # Cache only stores for 24 hours and so the link is also active only for 24 hours 
        cache.set(f"activation_{token}", user.id, 86400)
        
        # Token is embedded in the url
        activation_link = request.build_absolute_uri(
            reverse('activate_account', args=[token])
        )
        
        subject = "Activate Your Account"
        message = f"""
        Hi {user.email},
        
        Please click the link below to activate your account:
        {activation_link}
        
        This link will expire in 24 hours.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False

# Handles user's account activation
def activate_account(request, token):
    # Fetches corresponding user_id of the activation token
    user_id = cache.get(f"activation_{token}")
    
    # If it doesn't match, an error message is raised
    if not user_id:
        messages.error(request, "Invalid or expired activation link.")
        return redirect("login_view")
    
    # Else user's is_active status is set to True
    try:
        user = Users.objects.get(id=user_id)
        user.is_active = True
        user.save()
        
        # Cache deleted
        cache.delete(f"activation_{token}")
        
        messages.success(request, "Account activated successfully! You can now log in.")
        return redirect("login_view")
    except Users.DoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect("login_view")

# View for handling user login
def login_view(request):
    if request.method == "POST":
        # Login is limited to 5 attempts in 15 minutes
        if is_rate_limited(request, 'login', limit=5, window=900):
            messages.error(request, "Too many login attempts. Please try again later.")
            return render(request, "authentication/login.html")

        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user_obj = Users.objects.filter(email=email).first()
            user = authenticate(request, username=user_obj.username, password=password)
        except Users.DoesNotExist:
            user = None

        # If user didn't authenticate their email, they are asked to authenticate
        if user is not None:
            if not user.is_active:
                messages.success(
                    request,
                    "Please check your email to activate your account. "
                    "⚠️ Important: It may be in your SPAM/Junk folder."
                )
                return render(request, "authentication/login.html")
            
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials. Did you authenticate your email?")
            return render(request, "authentication/login.html")
    else:
        return render(request, "authentication/login.html")

# View for handling sign up process
def sign_up(request):
    if request.method == "POST":
        if is_rate_limited(request, 'signup', limit=2, window=3600):
            messages.error(request, "Too many signup attempts. Please try again later.")
            return render(request, "authentication/sign_up.html")

        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]

        is_teacher = request.POST.get("isTeacher", False)
        
        if is_teacher:
            subject = request.POST.get("subject", "")
            if not subject:
                messages.error(request, "Subject is required for teachers")
                return render(request, "authentication/sign_up.html")
            graduation_year = None
        else:
            graduation_year = request.POST.get("graduation-year", "")
            if not graduation_year:
                messages.error(request, "Graduation year is required for students")
                return render(request, "authentication/sign_up.html")
            subject = None
        
        if password != confirmation:
            messages.error(request, "Passwords must match")
            return render(request, "authentication/sign_up.html")

        try:
            user = Users.objects.get(email=email)
            user_exists = True
        except Users.DoesNotExist:
            user = None
            user_exists = False

        if user_exists and user.is_active == False:
            if send_activation_email_asynchronous(user, request):
                messages.success(
                    request,
                    "A new activation link has been sent to your email. "
                    "⚠️ Important: It may be in your SPAM/Junk folder."
                )
            else:
                messages.warning(
                    request, 
                    "Couldn't send activation email. Please contact oryxalumni@gmail.com for manual activation."
                )
            return render(request, "authentication/login.html")

        try:
            user = Users.objects.create_user(
                email=email, 
                username=email, 
                password=password,
                is_active=False,
                is_teacher=bool(is_teacher)
            )
            user.save()
            
            profile = Profile.objects.create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            
            if is_teacher:
                profile.subject = subject
            else:
                profile.graduation_year = graduation_year
                
            profile.save()

            if send_activation_email_asynchronous(user, request):
                messages.success(
                    request,
                    "Please check your email to activate your account. "
                    "⚠️ Important: It may be in your SPAM/Junk folder."
                )
            else:
                messages.warning(
                    request, 
                    "Account created but couldn't send activation email. Please contact oryxalumni@gmail.com for manual activation."
                )
            
            return render(request, "authentication/login.html")
            
        except IntegrityError:
            messages.error(request, "Email is already registered")
            return render(request, "authentication/sign_up.html")
        except Exception as e:
            messages.error(request, "An error occurred during signup. Please try again.")
            return render(request, "authentication/sign_up.html")
    else:
        return render(request, "authentication/sign_up.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "authentication/login.html")