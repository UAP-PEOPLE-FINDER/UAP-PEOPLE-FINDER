from email.policy import default
from django.db import models
from django.contrib.auth.models import User


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
    incoming = models.OneToOneField(User, related_name="incoming", on_delete=models.CASCADE)
    outgoing = models.OneToOneField(User, related_name="outgoing", on_delete=models.CASCADE)
    isFriend = models.BooleanField(default=False)
    