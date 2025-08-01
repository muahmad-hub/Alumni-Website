from django.urls import path
from . import views

urlpatterns = [
    path("mentor_signup", views.mentor_signup, name="mentor_signup"),
    path("mentor_match/", views.mentor_match, name="mentor_match"),
    path("mentor_dashboard", views.mentor_dashboard, name="mentor_dashboard"),
    path("accept_mentor/<int:match_id>/<int:mentor_id>", views.accept_mentor, name="accept_mentor"),
    path("decline_mentor/<int:match_id>/<int:mentor_id>", views.decline_mentor, name="decline_mentor"),

]