from django.contrib import admin
from .models import ListofInterests, Profile, Interest

# Register your models here
def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]

class ListofInterestsAdmin(admin.ModelAdmin):
    fields = ["interest"]

class ProfileAdmin(admin.ModelAdmin):
    fields = get_model_fields(Profile)