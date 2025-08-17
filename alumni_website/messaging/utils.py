from .models import Groups, Members
from django.db.models import Count

# Creates message group for first time connection
# Adds both users to the group
def create_chat_room(user1, user2):
    groups = Groups.objects \
        .filter(is_private=True) \
        .filter(members__user__in=[user1, user2]) \
        .annotate(num_members=Count('members')) \
        .filter(num_members=2) \
        .distinct()

    for g in groups:
        users_in_group = set(g.members.values_list('user_id', flat=True))
        if user1.id in users_in_group and user2.id in users_in_group:
            return
        
    new_group = Groups.objects.create(is_private=True)
    Members.objects.create(group=new_group, user=user1)
    Members.objects.create(group=new_group, user=user2)