from django.db import models
from core.models import Users

class MessageGroup(models.Model):
    group_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'Group name: {self.group_name}'

class GroupMessage(models.Model):
    group = models.ForeignKey(MessageGroup, related_name="group_messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, related_name="chats_sent", on_delete=models.CASCADE)
    sent_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.message} from {self.sender}'