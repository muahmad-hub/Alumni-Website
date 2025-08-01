from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    # path("edit_profile", views.edit_profile, name="edit_profile"),
    path("view_profile/<int:id>", views.view_profile, name="view_profile"),
    # path("get_profile_info", views.get_profile_info, name="get_profile_info"),

    path("edit_personal_section", views.edit_personal_section, name="edit_personal_section"),
    path("edit_bio_section", views.edit_bio_section, name="edit_bio_section"),
    path("edit_education_section", views.edit_education_section, name="edit_education_section"),
    path("edit_skills_section", views.edit_skills_section, name="edit_skills_section"),
    path("edit_goals_section", views.edit_goals_section, name="edit_goals_section"),
    path("edit_career_section", views.edit_career_section, name="edit_career_section"),
    path("edit_employment_status", views.edit_employment_status, name="edit_employment_status"),
    path("connect", views.connect, name="connect"),
]