from django.contrib import admin
from .models import *

admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(Mentor)
admin.site.register(Skills)
admin.site.register(Languages)
admin.site.register(MentorMatch)