from django.db import models
from core.models import Users
import shortuuid

class Groups(models.Model):
    group_name = models.CharField(max_length=255, default = shortuuid.uuid, unique=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f'Group: {self.group_name}, Private: ${self.is_private}'
    

class Members(models.Model):
    group = models.ForeignKey(Groups, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name="group_memberships", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} in {self.group}'

class Messages(models.Model):
    group = models.ForeignKey(Groups, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, related_name="messages_sent", on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message} from {self.sender}'