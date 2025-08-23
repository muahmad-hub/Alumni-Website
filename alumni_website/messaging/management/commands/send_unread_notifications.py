from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from messaging.models import Members, Messages
import random
import time

# Command to send weeky message digest
# Only sends to users who have atleast 3 unread message and have allowed the weekly digest in their preferences
class Command(BaseCommand):
    help = 'Send weekly unread message notifications'

    def handle(self, *args, **options):
        users_with_unread_and_email = []
        for member in Members.objects.select_related('user', 'group').all():
            unread_count = 0
            if member.last_read_message_id and member.user.profile.send_digest_email == True:
                unread_count = Messages.objects.filter(
                    group=member.group,
                    id__gt=member.last_read_message_id
                ).exclude(sender=member.user).count()
            else:
                unread_count = Messages.objects.filter(
                    group=member.group
                ).exclude(sender=member.user).count()

            if unread_count >= 3:
                users_with_unread_and_email.append({
                    'user': member.user,
                    'unread_count': unread_count
                })

        for data in users_with_unread_and_email:
            try:
                self.send_notification_email(data['user'], data['unread_count'])
                self.stdout.write(f"Sent email to {data['user'].email}")

                # I'm adding a random delay so that their isn't too much pressure on the machine
                time.sleep(random.uniform(1, 5))
            except Exception as e:
                self.stdout.write(f"Failed to send email to {data['user'].email}: {e}")

    def send_notification_email(self, user, unread_count):
        subject = f"You have {unread_count} unread messages - Oryx Alumni"
        
        context = {
            "first_name": user.profile.first_name,
            "unread_count": unread_count,
            "site_url": "www.oryxalumni.com/messaging/"
        }
        
        html_content = render_to_string("notifications/unread_message.html", context)
        
        text_content = f"""Hi {context['first_name']},

You have {unread_count} unread messages on Oryx Alumni.

Visit: {context['site_url']}/messaging/

Best regards,
Oryx Alumni Team
"""

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()