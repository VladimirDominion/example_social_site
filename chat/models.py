from django.db import models


class ChatGroup(models.Model):
    name = models.CharField(max_length=200, default='')
    member = models.ManyToManyField("users.User", blank=True)


class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message = models.TextField(default="")
