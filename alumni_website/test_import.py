import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_website.settings')
django.setup()

import alumni_website.asgi
print(alumni_website.asgi.application)
