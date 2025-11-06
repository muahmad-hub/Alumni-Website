import threading
import traceback
import os

from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.urls import reverse
from django.template.loader import render_to_string


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

        print(f"Starting activation email thread for {getattr(user, 'email', 'unknown')}")
        email_thread = threading.Thread(
            target=_send_email_thread,
            args=(subject, text_message, html_message, user.email)
        )
        email_thread.daemon = True
        email_thread.start()

        return True
    except Exception as e:
        print(f"Error in send_activation_email_asynchronous for {getattr(user, 'email', 'unknown')}: {e}")
        return False


def _send_via_sendgrid_api(subject, text_message, html_message, recipient_email):
    raise RuntimeError("Direct sendgrid package usage disabled; use Django EMAIL_BACKEND")


def _send_email_thread(subject, message, html_message, recipient_email):
    try:
        print(f"Attempting to send email to {recipient_email} via Django EMAIL_BACKEND")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Email sent successfully to {recipient_email} via Django EMAIL_BACKEND")
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"Django email send failed for {recipient_email}: {exc}\nTraceback:\n{tb}")
        return
