from django.contrib import admin
from .models import ListofInterests, Profile, Interest, Friend

# Register your models here
def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]

class ListofInterestsAdmin(admin.ModelAdmin):
    fields = ["interest"]

class ProfileAdmin(admin.ModelAdmin):
    fields = get_model_fields(Profile)

class InterestAdmin(admin.ModelAdmin):
    fields = ["username", "interest1", "link", "bio"]

class FriendAdmin(admin.ModelAdmin):
    fields = get_model_fields(Friend).remove('id')

admin.site.register(ListofInterests, ListofInterestsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Friend, FriendAdmin)