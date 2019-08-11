from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout


from . import forms
from . import models


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("profile:my_profile")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        profile_pk = self.request.user.pk
        return reverse_lazy('profile:my_profile', kwargs={'pk': profile_pk})


class LogOutView(generic.RedirectView):
    url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

