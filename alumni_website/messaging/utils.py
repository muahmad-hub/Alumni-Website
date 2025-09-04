from .models import Groups, Members
from django.db.models import Count

# Creates message group for first time connection
# Adds both users to the group
def create_chat_room(user1, user2):
    groups_with_user1 = Groups.objects.filter(
        is_private=True,
        members__user=user1
    ).values_list('id', flat=True)

    groups_with_user2 = Groups.objects.filter(
        is_private=True,
        members__user=user2
    ).values_list('id', flat=True)

    common_group_ids = set(groups_with_user1) & set(groups_with_user2)
        
    for group_id in common_group_ids:
        group = Groups.objects.get(id=group_id)
        if group.members.count() == 2:
            return 

    new_group = Groups.objects.create(is_private=True)
    Members.objects.create(group=new_group, user=user1)
    Members.objects.create(group=new_group, user=user2)