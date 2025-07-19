from django.urls import path
from . import views

urlpatterns = [
    path("", views.directory, name="directory"),
    path("search_directory/", views.search_directory, name="search_directory"),
    path("mentor_directory/", views.mentor_directory, name="mentor_directory"),
    path("mentor_search_directory", views.mentor_search_directory, name="mentor_search_directory"),

]