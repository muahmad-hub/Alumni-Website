from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("view_profile/<int:id>", views.view_profile, name="view_profile"),
    path("get_profile_info", views.get_profile_info, name="get_profile_info"),
]