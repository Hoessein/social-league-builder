from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Profile, Skill

from . import forms


def profile_edit(request):
    instance = request.user.profile

    if request.method == 'POST':
        profile_form = forms.EditProfileForm(request.POST, instance=instance)
        user_form = forms.EditUserForm(request.POST, request.FILES, instance=request.user)
        skill_form = forms.SkillProfileForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid() and skill_form.is_valid():
            user_form.save()
            profile_form.save()
            skilll = skill_form.save(commit=False)
            skilll.user = request.user
            skilll.save()
            return redirect('profile:my_profile')

    else:
        profile_form = forms.EditProfileForm(instance=instance)
        user_form = forms.EditUserForm(instance=request.user)
        skill_form = forms.SkillProfileForm(instance=request.user)

    return render(request,
                  'user_profile/profile_edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form,
                   'skill_form': skill_form,
                   }
                  )


class MyProfileView(DetailView):
    template_name = 'user_profile/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill'] = Skill.objects.all().filter(user_id=self.request.user)
        return context






