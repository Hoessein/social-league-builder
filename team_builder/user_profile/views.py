from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import EditProfileForm

from .models import Profile


# def edit_profile(request):
    # if request.method == 'POST':
    #     form = EditProfileForm(request.POST, instance=request.user)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/profile')


class ProfileUpdateView(UpdateView):
    fields = ['bio', 'location', 'birth_date']
    template_name = 'user_profile/profile_edit.html'
    success_url = reverse_lazy('profile:my_profile')
    model = Profile

    def get_object(self, queryset=None):
        print(self.request.user, "hier ben ik")
        return self.request.user.profile

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form.instance.user, "dit is de form")
        return super().form_valid(form)


class MyProfileView(DetailView):
    template_name = 'user_profile/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

