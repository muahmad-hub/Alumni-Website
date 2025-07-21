from django.urls import path
from . import views

urlpatterns = [
    path('message_room/', views.message_room, name="message_room"),
]