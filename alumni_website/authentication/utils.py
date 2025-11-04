import threading
import traceback
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.urls import reverse
from django.template.loader import render_to_string
import os


def send_activation_email_asynchronous(user, request):
    try:
        token = get_random_string(32)
        cache.set(f"activation_{token}", user.id, 86400)
        
        activation_link = request.build_absolute_uri(
            reverse('activate_account', args=[token])
        )
            
        subject = "Activate Your Account"
        
        html_message = render_to_string('notifications/activation_email.html', {
            'user_email': user.email,
            'activation_link': activation_link,
            'site_name': 'OryxAlumni'
        })
        
        text_message = f"Hi {user.email}, please activate your account: {activation_link}"
        
        print("Starting activation email thread for %s", getattr(user, 'email', 'unknown'))
        email_thread = threading.Thread(
            target=_send_email_thread,
            args=(subject, text_message, html_message, user.email)
        )
        email_thread.daemon = True
        email_thread.start()
        
        return True
    except Exception as e:
        print("Error in send_activation_email_asynchronous for %s: %s", getattr(user, 'email', 'unknown'), e)
        return False
    
def _send_email_thread(subject, message, html_message, recipient_email):
    try:
        print("Configuring SendGrid SMTP backend for recipient=%s host=%s port=%s timeout=%s",
                    recipient_email, os.environ.get('SENDGRID_SMTP_HOST', 'smtp.sendgrid.net'),
                    os.environ.get('SENDGRID_SMTP_PORT', 587), os.environ.get('SENDGRID_EMAIL_TIMEOUT', 180))

        sendgrid_backend = EmailBackend(
            host=os.environ.get('SENDGRID_SMTP_HOST', 'smtp.sendgrid.net'),
            port=int(os.environ.get('SENDGRID_SMTP_PORT', 587)),
            username=os.environ.get('SENDGRID_SMTP_USER', 'apikey'),
            password=os.environ.get('API_KEY_SENDGRID'),
            use_tls=True,
            timeout=int(os.environ.get('SENDGRID_EMAIL_TIMEOUT', 180))
        )

        print("Attempting to send activation email to %s via SendGrid SMTP", recipient_email)
        send_mail(
            subject,
            message,
            settings.SENDGRID_FROM_EMAIL,
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
            connection=sendgrid_backend,
        )
        print("Email sent successfully to %s", recipient_email)
    except Exception as e:
        tb = traceback.format_exc()
        print("Error sending email to %s: %s\nTraceback:\n%s", recipient_email, e, tb)
