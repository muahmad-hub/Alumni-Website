from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MessageGroup, GroupMessage

@login_required
def message_room(request):
    message_group = get_object_or_404(MessageGroup, group_name="Test")
    message_chat = message_group.group_messages.all().order_by('-sent_time')[:30]

    if request.method == "POST":
        message = request.POST.get("message")
        message_group = get_object_or_404(MessageGroup, group_name="Test")

        if message_group:
            new_message = GroupMessage(group = message_group, sender = request.user, message = message)
            new_message.save()

            return render(request, "messaging/partials/message.html", {
                "message_chat": new_message,
                "user": request.user
            })



    return render(request, "messaging/message.html", {
        "message_chat": message_chat
    })



        
