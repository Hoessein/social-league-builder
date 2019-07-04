from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Profile

from . import forms

# def edit_profile(request):
    # if request.method == 'POST':
    #     form = EditProfileForm(request.POST, instance=request.user)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/profile')


# class ProfileUpdateView(UpdateView):
#     fields = ['bio', 'location', 'birth_date']
#     template_name = 'user_profile/profile_edit.html'
#     success_url = reverse_lazy('profile:my_profile')
#     form_classes = {'profile': forms.EditProfileForm,
#                  'user': forms.ProfileUpdateForm}
#
#
#     def get_object(self, queryset=None):
#         print(self.request.user, "hier ben ik")
#         return self.request.user.profile
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         print(form.instance.user, "dit is de form")
#         return super().form_valid(form)


def profile_edit(request):
    instance = request.user.profile

    if request.method == 'POST':
        profile_form = forms.EditProfileForm(request.POST, instance=instance)
        user_form = forms.EditUserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            return redirect('profile:my_profile')

    else:
        profile_form = forms.EditProfileForm(instance=instance)
        user_form = forms.EditUserForm(instance=request.user)

    return render(request,
                  'user_profile/profile_edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form}
                  )

class MyProfileView(DetailView):
    template_name = 'user_profile/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

