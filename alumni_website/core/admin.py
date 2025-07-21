from django.contrib import admin

from core.models import *
from authentication.models import *
from messaging.models import *
from directory.models import *
from mentorship.models import *
from profiles.models import *

admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(MentorMatch)
admin.site.register(Mentor)
admin.site.register(Skills)
admin.site.register(Languages)
admin.site.register(Messages)
admin.site.register(Groups)
admin.site.register(Members)