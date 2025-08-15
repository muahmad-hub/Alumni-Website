import threading
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.urls import reverse

def send_activation_email_asynchronous(user, request):
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
        
        # Send email in thread for asynchronous process
        email_thread = threading.Thread(
            target=_send_email_thread,
            args=(subject, message, user.email)
        )
        email_thread.daemon = True
        email_thread.start()
        
        return True
    except Exception as e:
        return False

def _send_email_thread(subject, message, recipient_email):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        pass