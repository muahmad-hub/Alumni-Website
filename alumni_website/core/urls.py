from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health_check/", views.health_check, name="health_check"),
    path("db_health_check/", views.db_health_check, name="db_health_check")
]