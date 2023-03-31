from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ListofInterests, Interest
import django_tables2 as tables
from django.utils.safestring import mark_safe


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
    first_name = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;height:40px;font-size:115%;'}), max_length=30, required=True)
    last_name = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;height:40px;font-size:115%;'}), max_length=30, required=True)
    display_picture = forms.ImageField(widget=forms.FileInput())
    interest = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;height:40px;font-size:115%;'}), max_length=200, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;vertical-align: top;height:120px;font-size:115%;'}), max_length=140, required=True)
    link = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;height:40px;font-size:115%;'}), max_length=100, required=False)


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=30, required=False)


class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe(
            '<img src="%s" alt="Display Picture" style="float:right;width:100px;height:100px;padding:20px 20px 20px 20px; z-index: 7;" />'
            % value
        )


class SearchTable(tables.Table):
    class Meta:
        model = Profile
        template_name = "django_tables2/bootstrap-responsive.html"

    display_picture = ImageColumn()
