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
    path("view_profile/<int:id>", views.view_profile, name="view_profile")
]