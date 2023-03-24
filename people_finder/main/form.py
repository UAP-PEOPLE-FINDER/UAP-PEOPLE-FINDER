from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
