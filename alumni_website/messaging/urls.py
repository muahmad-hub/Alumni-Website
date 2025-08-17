from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages, name="messages"),
    path("open_chats/", views.open_chats, name="open_chats"),
    path("<str:group_name>/", views.chat_room, name="chat_room"),
]
