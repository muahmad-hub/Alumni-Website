import base64
import json
from typing import List
from email.utils import parseaddr

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.conf import settings


class SendGridAPIBackend(BaseEmailBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = getattr(settings, 'SENDGRID_API_KEY', None) or None
        self.api_url = getattr(settings, 'SENDGRID_API_URL', 'https://api.sendgrid.com/v3/mail/send')
        self.timeout = getattr(settings, 'SENDGRID_API_TIMEOUT', 30)

    def send_messages(self, email_messages: List[EmailMessage]):
        if not email_messages:
            return 0

        try:
            import requests
        except Exception as e:
            print(f"SendGrid backend requires requests package: {e}")
            return 0

        if not self.api_key:
            print("SendGrid API key not configured (SENDGRID_API_KEY). Emails not sent.")
            return 0

        sent_count = 0

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        for message in email_messages:
            try:
                payload = self._build_payload(message)
                resp = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=self.timeout)
                if 200 <= resp.status_code < 300:
                    sent_count += 1
                else:
                    print(f"SendGrid API returned {resp.status_code} for recipients {message.to}: {resp.text}")
            except Exception as exc:
                print(f"Exception sending email via SendGrid API to {message.to}: {exc}")

        return sent_count

    def _build_payload(self, message: EmailMessage):
        content = []
        if getattr(message, 'content_subtype', '') == 'html':
            content.append({'type': 'text/html', 'value': message.body or ''})
            content.append({'type': 'text/plain', 'value': getattr(message, 'alternatives_plain', '') or ''})
        else:
            content.append({'type': 'text/plain', 'value': message.body or ''})

        personalizations = [
            {
                'to': [{'email': r} for r in (message.to or [])],
                'subject': message.subject or ''
            }
        ]

        raw_from = getattr(settings, 'SENDGRID_FROM_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None) or ''
        name, email_address = parseaddr(raw_from)

        from_field = {'email': email_address}
        if name:
            from_field['name'] = name

        payload = {
            'personalizations': personalizations,
            'from': from_field,
            'content': content,
        }

        if getattr(message, 'attachments', None):
            sg_attachments = []
            for att in message.attachments:
                try:
                    filename, content_bytes, mimetype = att
                except Exception:
                    continue
                encoded = base64.b64encode(content_bytes).decode('ascii')
                sg_attachments.append({
                    'content': encoded,
                    'type': mimetype or 'application/octet-stream',
                    'filename': filename
                })
            if sg_attachments:
                payload['attachments'] = sg_attachments

        return payload
