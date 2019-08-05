from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput

from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import Profile, Project, ProjectPosition, ProfileSkill, ProjectSkill


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'bio',
        )





class EditUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "avatar")


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", 'description', 'timeline', 'project_skill')
        label = {'title': 'Project Title'}

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'projectname here'}),
        'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
        'timeline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'timeline'}),
        'project_skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'skill'}),

    }


PositionModelFormset = modelformset_factory(
    ProjectPosition,
    fields=('title', 'information',),
    extra=1,
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title!'}),
        'information': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'information!'}),

    }
)

SkillModelFormset = modelformset_factory(
    ProfileSkill,
    fields=('name',),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name!'}),

    }
)

class ProfileSkillForm(forms.ModelForm):
    class Meta:
        model = ProfileSkill
        fields = ('name',)