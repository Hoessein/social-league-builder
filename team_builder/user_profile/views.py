from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.signals import notify
from django.contrib.auth.models import User
from .models import Project, ProjectPosition, Applicant, ProfileSkill

from . import forms



def index(request):
    projects = Project.objects.filter()
    return render(request, 'index.html', {'projects': projects})


@login_required
def profile_edit(request):
    instance = request.user.profile
    skill_instance = ProfileSkill.objects.filter(profile__user_id=request.user.id)

    if request.method == 'POST':
        profile_form = forms.EditProfileForm(request.POST, instance=instance)
        user_form = forms.EditUserForm(request.POST, request.FILES, instance=request.user)
        # skill_form = forms.ProfileSkillForm(request.POST, instance=skill_instance)
        skill_formset = forms.SkillModelFormset(request.POST, queryset=skill_instance)

        if profile_form.is_valid() and user_form.is_valid() and skill_formset.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)

            for form in skill_formset:
                skill = form.save(commit=False)
                skill.profile = profile
                skill.save()
            return redirect('profile:my_profile')

    else:
        profile_form = forms.EditProfileForm(instance=instance)
        user_form = forms.EditUserForm(request.POST or None, instance=request.user,)
        skill_formset = forms.SkillModelFormset(request.POST or None, queryset=skill_instance)

    return render(request,
                  'user_profile/profile_edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form,
                   'skill_formset': skill_formset,
                   }
                  )


class MyProfileView(LoginRequiredMixin, DetailView):
    template_name = 'user_profile/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = ProfileSkill.objects.filter(profile__user=self.request.user)
        context['project'] = Project.objects.filter(owner=self.request.user)
        return context


class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'user_profile/project.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = ProjectPosition.objects.filter(project__id=self.kwargs.get('pk'))
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context


class ApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter()
        return context


class NewApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'user_profile/new_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_applicants'] = Applicant.objects.filter(status='p')
        return context


class AcceptedApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'user_profile/accepted_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_applicants'] = Applicant.objects.filter(status='a')
        return context


class RejectedApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'user_profile/rejected_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rejected_applicants'] = Applicant.objects.filter(status='r')
        return context


@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = forms.CreateProjectForm(request.POST, prefix='project')
        position_formset = forms.PositionModelFormset(request.POST, prefix='position')

        if project_form.is_valid() and position_formset.is_valid():

            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()

            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.save()
            return redirect('profile:my_profile')

    else:
        position_formset = forms.PositionModelFormset(queryset=ProjectPosition.objects.none(), prefix='position')
        project_form = forms.CreateProjectForm(prefix='project')

    return render(request, 'user_profile/project_new.html',
                  {'project_form': project_form,
                   'position_formset': position_formset}
                  )


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    position = ProjectPosition.objects.filter(project__id=pk)

    if request.method == 'POST':
        position_formset = forms.PositionModelFormset(request.POST, queryset=position, prefix='position')
        project_form = forms.CreateProjectForm(request.POST, instance=project, prefix='project')

        if project_form.is_valid() and position_formset.is_valid():

            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()

            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.save()
            return redirect('profile:project', pk=pk)

    else:
        project_form = forms.CreateProjectForm(instance=project, prefix='project')
        position_formset = forms.PositionModelFormset(queryset=position, prefix='position')

    return render(request,
                  'user_profile/project_edit.html',
                  {'project_form': project_form,
                   'position_formset': position_formset,
                   }
                  )


@login_required
def apply_position(request, project_pk, position_pk):
    project = get_object_or_404(Project, pk=project_pk)
    positions = ProjectPosition.objects.filter(project__id=project.pk,)

    for position in positions:
        if position.pk == position_pk:
            pending_status = position.applicant_set.create(status='p', name=request.user)
            pending_status.save()
        return redirect('profile:project', pk=project.pk)


@login_required
def reject_application(request, applicant_pk):
    applicant = get_object_or_404(Applicant, pk=applicant_pk)
    applicant.status = 'r'
    applicant.save()

    notify.send(
        applicant.name,
        recipient=applicant.name,
        verb=f'Unfortunately, you have been reject as a'
        f' {str(applicant.position.title)} in the project:'
        f' {str(applicant.position.project.title)}!')

    return redirect('profile:applications')


@login_required
def accept_application(request, applicant_pk):
    applicant = get_object_or_404(Applicant, pk=applicant_pk)
    applicant.status = 'a'
    applicant.position.filled = True
    applicant.save()
    notify.send(
        applicant.name,
        recipient=applicant.name,
        verb=f'Congratulations, you have been accepted as a'
        f' {str(applicant.position.title)} in the project:'
        f' {str(applicant.position.project.title)}!')
    return redirect('profile:applications')


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'user_profile/search_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |(
                Q(description__icontains=query)
                ))
        return qs


class NotificationsView(LoginRequiredMixin, ListView):
    template_name = "user_profile/notifications.html"
    model = User
