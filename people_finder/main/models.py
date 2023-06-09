from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


# Create your models here.
class ListofInterests(models.Model):
    interest = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.interest


class Profile(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, primary_key=True
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    display_picture = models.ImageField(
        upload_to="images/", default="images/default.png"
    )


class Interest(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=140, blank=True)


class Friend(models.Model):
    incoming = models.ForeignKey(User, related_name="incoming", on_delete=models.CASCADE)
    outgoing = models.ForeignKey(User, related_name="outgoing", on_delete=models.CASCADE)
    isFriend = models.BooleanField(default=False)
    
class ChatRoom(models.Model):
    id = models.OneToOneField(Friend, on_delete=models.CASCADE, primary_key=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1024) 

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1024) 
    link = models.TextField(max_length=1024) 
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)