from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Count
from django.http import Http404

@login_required
def chat_room(request, group_name):
    group = get_object_or_404(Groups, group_name=group_name)

    if Members.objects.filter(group=group, user=request.user).exists():
        messages = Messages.objects.filter(group=group).order_by('-sent_time')[:30]
        online_count = Members.objects.filter(group=group, is_online=True).exclude(user=request.user).count()
        return render(request, "messaging/message.html", {
                "messages": messages,
                "user": request.user,
                "group_name": group_name,
                "online_count": online_count,
            })
    
    raise Http404
    
@login_required
def get_or_create_chat_room(request, other_user_id):
    other_user = get_object_or_404(Users, id=other_user_id)
    groups = Groups.objects \
        .filter(is_private=True) \
        .filter(members__user__in=[request.user, other_user]) \
        .annotate(num_members=Count('members')) \
        .filter(num_members=2) \
        .distinct()

    for g in groups:
        users_in_group = set(g.members.values_list('user_id', flat=True))
        if request.user.id in users_in_group and other_user.id in users_in_group:
            group = g
            break
    else:
        group = None

    
    if group:
        return redirect('chat_room', group_name = group.group_name)
    else:
        new_group = Groups.objects.create(is_private = True)
        Members.objects.create(group = new_group, user = request.user)
        Members.objects.create(group = new_group, user = other_user)
        return redirect('chat_room', group_name = new_group.group_name)
