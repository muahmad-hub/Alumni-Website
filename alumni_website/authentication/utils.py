import threading
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
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
        
        # Sending email in thread for asynchronous process
        email_thread = threading.Thread(
            target=_send_email_thread,
            args=(subject, message, user.email)
        )
        email_thread.daemon = True
        email_thread.start()
        
        return True
    except Exception as e:
        print(f"Error in send_activation_email_asynchronous: {e}") 
        return False

def _send_email_thread(subject, message, recipient_email):
    try:
        sendgrid_backend = EmailBackend(
            host=settings.SENDGRID_SMTP_HOST,
            port=settings.SENDGRID_SMTP_PORT,
            username=settings.SENDGRID_SMTP_USER,
            password=settings.SENDGRID_SMTP_PASSWORD,
            use_tls=True,
            timeout=settings.SENDGRID_EMAIL_TIMEOUT
        )
        
        send_mail(
            subject,
            message,
            settings.SENDGRID_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
            connection=sendgrid_backend,
        )
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}") 