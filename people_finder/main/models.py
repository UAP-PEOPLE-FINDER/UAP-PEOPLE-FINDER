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
    interests = [(str(i), str(i)) for i in ListofInterests.objects.all()]
    # interest_no = models.IntegerField(default=0, unique = False, null = False)
    #
    interest1 = models.CharField(
        max_length=20, blank=True, choices=interests, unique=False, null=True
    )
    link = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=140, blank=True)
