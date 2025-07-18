from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login_view", views.login_view, name="login_view"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("logout", views.logout_view, name="logout_view"),
    path("profile", views.profile, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("directory", views.directory, name="directory"),
    path("search_directory", views.search_directory, name="search_directory"),
    path("view_profile/<int:id>", views.view_profile, name="view_profile"),


    path("mentor_directory", views.mentor_directory, name="mentor_directory"),
    path("mentor_search_directory", views.mentor_search_directory, name="mentor_search_directory"),
    path("mentor_signup", views.mentor_signup, name="mentor_signup"),
    path("mentor_match/<int:mentor_id>", views.mentor_match, name="mentor_match"),
    path("mentor_dashboard", views.mentor_dashboard, name="mentor_dashboard"),
    path("accept_mentor/<int:match_id>/<int:mentor_id>", views.accept_mentor, name="accept_mentor"),
    path("decline_mentor/<int:match_id>/<int:mentor_id>", views.decline_mentor, name="decline_mentor"),
    path("get_profile_info", views.get_profile_info, name="get_profile_info"),
]