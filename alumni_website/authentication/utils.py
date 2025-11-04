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

        logger.info("Starting activation email thread for %s", getattr(user, 'email', 'unknown'))
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


def _send_via_sendgrid_api(subject, text_message, html_message, recipient_email):
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
    except Exception as imp_e:
        print("sendgrid package import failed: %s", imp_e)
        raise

    sg_api_key = os.environ.get('API_KEY_SENDGRID')
    if not sg_api_key:
        raise RuntimeError('SendGrid API key missing: set API_KEY_SENDGRID in environment')

    mail = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=recipient_email,
        subject=subject,
        html_content=html_message or text_message,
    )

    sg = SendGridAPIClient(sg_api_key)
    response = sg.send(mail)
    print("SendGrid Web API send status=%s for %s", getattr(response, 'status_code', None), recipient_email)
    return response


def _send_email_thread(subject, message, html_message, recipient_email):
    try:
        logger.info("Attempting SendGrid Web API send to %s", recipient_email)
        resp = _send_via_sendgrid_api(subject, message, html_message, recipient_email)
        logger.info("SendGrid Web API send succeeded for %s (status=%s)", recipient_email, getattr(resp, 'status_code', None))
        return
    except Exception as api_exc:
        tb_api = traceback.format_exc()
        print("SendGrid Web API send failed for %s: %s\nTraceback:\n%s", recipient_email, api_exc, tb_api)

    try:
        print("Configuring SendGrid SMTP backend for recipient=%s host=%s port=%s timeout=%s",
                    recipient_email,
                    os.environ.get('SENDGRID_SMTP_HOST', 'smtp.sendgrid.net'),
                    os.environ.get('SENDGRID_SMTP_PORT', 587),
                    os.environ.get('SENDGRID_EMAIL_TIMEOUT', 180))

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
        print("Email sent successfully to %s via SMTP", recipient_email)
    except Exception as smtp_exc:
        tb_smtp = traceback.format_exc()
        print("SMTP send failed for %s: %s\nTraceback:\n%s", recipient_email, smtp_exc, tb_smtp)
        return
