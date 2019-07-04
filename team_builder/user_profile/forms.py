from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'bio',
            'location',
            'birth_date',
        )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
