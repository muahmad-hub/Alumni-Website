from django.urls import path
from . import views

urlpatterns = [
    path("", views.directory, name="directory"),
    path("alumni_directory_recommend", views.alumni_directory_recommend, name="alumni_directory_recommend"),
    path("search_directory/", views.search_directory, name="search_directory"),
    path("mentor_directory/", views.mentor_directory, name="mentor_directory"),
    path("mentor_search_directory", views.mentor_search_directory, name="mentor_search_directory"),
    path("teacher_directory/", views.teacher_directory, name="teacher_directory"),
    path("teacher_search_directory", views.teacher_search_directory, name="teacher_search_directory"),
]