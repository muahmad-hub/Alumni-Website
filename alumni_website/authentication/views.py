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
import logging

logger = logging.getLogger(__name__)

# Function used to get users IP address to log login attempts
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
        token = get_random_string(32)
        cache.set(f"activation_{token}", user.id, 86400)
        
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
        logger.error(f"Failed to send activation email to {user.email}: {str(e)}")
        return False

def activate_account(request, token):
    user_id = cache.get(f"activation_{token}")
    
    if not user_id:
        messages.error(request, "Invalid or expired activation link.")
        return redirect("login_view")
    
    try:
        user = Users.objects.get(id=user_id)
        user.is_active = True
        user.save()
        
        cache.delete(f"activation_{token}")
        
        messages.success(request, "Account activated successfully! You can now log in.")
        return redirect("login_view")
    except Users.DoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect("login_view")


def login_view(request):
    if request.method == "POST":
        if is_rate_limited(request, 'login', limit=5, window=900):
            messages.error(request, "Too many login attempts. Please try again later.")
            return render(request, "authentication/login.html")

        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user_obj = Users.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except Users.DoesNotExist:
            user = None

        if user is not None:
            if not user.is_active:
                messages.error(request, "Please check your email to activate your account (Maybe in Spam)")
                return render(request, "authentication/login.html")
            
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "authentication/login.html")
    else:
        return render(request, "authentication/login.html")

def sign_up(request):
    if request.method == "POST":
        if is_rate_limited(request, 'signup', limit=2, window=3600):
            messages.error(request, "Too many signup attempts. Please try again later.")
            return render(request, "authentication/sign_up.html")

        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            messages.error(request, "Passwords must match")
            return render(request, "authentication/sign_up.html")

        try:
            user = Users.objects.create_user(
                email=email, 
                username=email, 
                password=password,
                is_active=False
            )
            user.save()
            
            profile = Profile.objects.create(user=user)
            profile.save()

            if send_activation_email(user, request):
                messages.success(request, "Account created! Please check your email to activate your account (Check spam too)")
            else:
                messages.warning(request, "Account created but couldn't send activation email. Please contact oryxalumni@gmail.com for manual activation.")
            
            return render(request, "authentication/login.html")
            
        except IntegrityError:
            messages.error(request, "Email is already registered")
            return render(request, "authentication/sign_up.html")
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            messages.error(request, "An error occurred during signup. Please try again.")
            return render(request, "authentication/sign_up.html")
    else:
        return render(request, "authentication/sign_up.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "authentication/login.html")