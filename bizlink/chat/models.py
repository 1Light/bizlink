from django.db import models
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class ChatGroup(models.Model):
    chatGroupId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="chatGroup", alphabet="ABCDEF0123456789")
    users_online = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="online_in_groups", blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['-created_at']

class ReadReceipt(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now=True)  # Timestamp of when the message was read

    class Meta:
        unique_together = ('message', 'user')