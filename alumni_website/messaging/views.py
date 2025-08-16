from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import Http404, JsonResponse
from django.db.models import Q
from mentorship.utils import is_mentor

@login_required
def chat_room(request, group_name):
    group = get_object_or_404(Groups, group_name=group_name)

    other_user = Members.objects.filter(
        group=group 
    ).exclude(user=request.user).first()

    other_is_mentor = is_mentor(other_user.user, request.user)
    current_is_mentor = is_mentor(request.user, other_user.user)

    has_mentor = False
    mentor_type = None

    if other_is_mentor["is_mentor"]:
        has_mentor = True
        mentor_type = "other"
    elif current_is_mentor["is_mentor"]:
        has_mentor = True 
        mentor_type = "current"

    if Members.objects.filter(group=group, user=request.user).exists():
        messages = Messages.objects.filter(group=group).order_by('-sent_time')[:50]
        online_count = Members.objects.filter(group=group, is_online=True).exclude(user=request.user).count()

        current_member = Members.objects.get(group=group, user=request.user)
        latest_message = messages.first()
        if latest_message:
            current_member.last_read_message_id = latest_message.id
            current_member.save()


        return render(request, "messaging/messages.html", {
        "messages": messages,
        "user": request.user,
        "group_name": group_name,
        "online_count": online_count,
        "other_user": other_user,
        "has_mentor": has_mentor,
        "current_chat": True,
        "mentor_type": mentor_type,
    })


    # has_mentor = False
    # if mentor["is_mentor"]:
    #     has_mentor = True


    # if Members.objects.filter(group=group, user=request.user).exists():
    #     messages = Messages.objects.filter(group=group).order_by('-sent_time')[:50]
    #     online_count = Members.objects.filter(group=group, is_online=True).exclude(user=request.user).count()
    #     return render(request, "messaging/messages.html", {
    #             "messages": messages,
    #             "user": request.user,
    #             "group_name": group_name,
    #             "online_count": online_count,
    #             "other_user": other_user,
    #             "has_mentor": has_mentor,
    #             "current_chat": True,
    #         })
    
    raise Http404
    
# @login_required
# def get_or_create_chat_room(request, other_user_id):
#     other_user = get_object_or_404(Users, id=other_user_id)
#     groups = Groups.objects \
#         .filter(is_private=True) \
#         .filter(members__user__in=[request.user, other_user]) \
#         .annotate(num_members=Count('members')) \
#         .filter(num_members=2) \
#         .distinct()

#     for g in groups:
#         users_in_group = set(g.members.values_list('user_id', flat=True))
#         if request.user.id in users_in_group and other_user.id in users_in_group:
#             group = g
#             break
#     else:
#         group = None

    
#     if group:
#         return redirect('chat_room', group_name = group.group_name)
#     else:
#         new_group = Groups.objects.create(is_private = True)
#         Members.objects.create(group = new_group, user = request.user)
#         Members.objects.create(group = new_group, user = other_user)
#         return redirect('chat_room', group_name = new_group.group_name)
    

@login_required
def messages(request):
    return render(request, "messaging/messages.html", {
        "current_chat": False,
    })

@login_required
def open_chats(request):
    query = request.GET.get("q", "").strip()
    user_groups = Groups.objects.filter(members__user=request.user)

    members = Members.objects.filter(
        group__in=user_groups
    ).exclude(user=request.user)

    if query:
        members = members.filter(
            Q(user__profile__first_name__icontains=query) | Q(user__profile__last_name__icontains=query)
        )

    results = []

    current_user_member = Members.objects.filter(group__in=user_groups, user=request.user)


    for member in members.select_related("user__profile", "group").distinct():
        profile = member.user.profile

        other_is_mentor = is_mentor(member.user, request.user)
        is_user_mentor = other_is_mentor["is_mentor"]
        
        current_member = current_user_member.filter(group=member.group).first()
        unread_count = 0
        if current_member and current_member.last_read_message_id:
            unread_count = Messages.objects.filter(
                group=member.group,
                id__gt=current_member.last_read_message_id
            ).exclude(sender=request.user).count()
        else:
            unread_count = Messages.objects.filter(
                group=member.group
            ).exclude(sender=request.user).count()


        results.append({
            "name": f"{profile.first_name or ''} {profile.last_name or ''}".strip(),
            "profile_url": profile.profile_url or "/static/images/profile_image.jpg",
            "group_name": member.group.group_name,
            "is_mentor": is_user_mentor,
            "unread_count": unread_count, 
        })

    return JsonResponse({"results": results})
