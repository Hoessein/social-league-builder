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


class ProfileSkillForm(forms.ModelForm):
    class Meta:
        model = ProfileSkill
        fields = ('name',)


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
# class CreateProjectPositionForm(forms.ModelForm):
#     class Meta:
#         model = ProjectPosition
#         fields = ('information', 'title')


PositionModelFormset = modelformset_factory(
    ProjectPosition,
    fields=('title', 'information',),
    extra=1,
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title!'}),
        'information': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'information!'}),

    }
)

# class somethingForm(forms.ModelForm):
#     class Meta:
#         model = ProjectPosition
#         fields = ('position', 'project')


# max_num = 1,
# fields = (
#              'title', 'description', 'positions', 'timeline'),
# widgets = {
#               'name': TextInput(attrs={'placeholder': 'Position Title',
#                                        'class': 'circle--input--h3'}
#                                 ),
#               'description': Textarea(attrs={'cols': 40,
#                                              'rows': 10,
#                                              'placeholder': 'Position description...'}
#                                       ),
#           },
# help_texts = {
#     'time_involvement': 'In minutes',
# }
# )



# #factory that makes model formsets
# PositionFormset = modelformset_factory(ProjectPosition, fields=('title', 'description'),
#                                        form=CreateProjectForm,
#                                        extra=1,
#