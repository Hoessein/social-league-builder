from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from .models import Profile


class EditProfileForm(UserChangeForm):

    class Meta:
        models = Profile
        fields = (
            'bio',
            'location',
            'birth_date'
        )


