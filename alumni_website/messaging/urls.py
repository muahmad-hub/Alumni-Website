from django.urls import path
from . import views

urlpatterns = [
    # path('message_room/', views.message_room, name="message_room"),

    path("<str:group_name>/", views.chat_room, name="chat_room"),
    path("get_or_create_chat_room/<int:other_user_id>/", views.get_or_create_chat_room, name="get_or_create_chat_room"),
]