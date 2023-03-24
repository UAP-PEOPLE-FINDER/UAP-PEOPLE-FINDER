from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ListofInterests, Interest

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


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    display_picture = forms.ImageField()
    interest_1 = forms.ModelChoiceField(
        queryset=ListofInterests.objects.all(), required=False
    )
    interest_1_bio = forms.CharField(max_length=140, required=False)
    interest_1_link = forms.CharField(max_length=100, required=False)

    interest_2 = forms.ModelChoiceField(
        queryset=ListofInterests.objects.all(), required=False
    )
    interest_2_bio = forms.CharField(max_length=140, required=False)
    interest_2_link = forms.CharField(max_length=100, required=False)

    interest_3 = forms.ModelChoiceField(
        queryset=ListofInterests.objects.all(), required=False
    )
    interest_3_bio = forms.CharField(max_length=140, required=False)
    interest_3_link = forms.CharField(max_length=100, required=False)

    # interest1 = forms.


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=30, required=False)