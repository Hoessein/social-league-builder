from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.signals import notify
from django.contrib.auth.models import User
from .models import Project, ProjectPosition, Applicant, ProfileSkill, Profile

from . import forms


def index(request,):
    """homepage"""
    projects = Project.objects.filter()
    return render(request, 'index.html', {'projects': projects})


@login_required
def profile_edit(request, pk):
    """allows user to edit their personal profile"""
    instance = get_object_or_404(Profile, pk=pk)
    skill_instance = ProfileSkill.objects.filter(profile__user_id=instance.id)

    if request.user.pk == instance.user.pk:

        if request.method == 'POST':
            profile_form = forms.EditProfileForm(request.POST, instance=instance)
            user_form = forms.EditUserForm(request.POST, request.FILES, instance=instance.user)
            skill_formset = forms.SkillModelFormset(request.POST, queryset=skill_instance)

            if profile_form.is_valid() and user_form.is_valid() and skill_formset.is_valid():
                user_form.save()
                profile = profile_form.save(commit=False)

                # more than one skill can be added in the profile.
                for form in skill_formset:
                    skill = form.save(commit=False)
                    skill.profile = profile
                    skill.save()
                return redirect('profile:my_profile', pk=request.user.pk)

        else:
            profile_form = forms.EditProfileForm(instance=instance)
            user_form = forms.EditUserForm(request.POST or None, instance=instance.user)
            skill_formset = forms.SkillModelFormset(request.POST or None, queryset=skill_instance)

        return render(request,
                      'user_profile/profile_edit.html',
                      {'profile_form': profile_form,
                       'user_form': user_form,
                       'skill_formset': skill_formset,
                       }
                      )


class MyProfileView(LoginRequiredMixin, DetailView):
    """Shows the profile page for logged in user"""
    template_name = 'user_profile/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = ProfileSkill.objects.filter(profile__user_id=self.kwargs.get('pk'))
        context['projects'] = Project.objects.filter(owner_id=self.kwargs.get('pk'))
        context['applicants'] = Applicant.objects.filter(Q(name_id=self.kwargs.get('pk')) &
                                                                  (Q(status='a')))
        return context


class ProjectView(LoginRequiredMixin, DetailView):
    """shows the project the user requested to view"""
    template_name = 'user_profile/project.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = ProjectPosition.objects.filter(project__id=self.kwargs.get('pk'))
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context


class ApplicationsView(LoginRequiredMixin, ListView):
    """shows all applicants for projects the logged in user created"""
    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter(position__project__owner_id=self.request.user.id)
        context['projects'] = Project.objects.filter(owner=self.request.user)
        return context


class NewApplicationsView(LoginRequiredMixin, ListView):
    """shows all applicants that haven't been accepted or rejected for projects the logged in user created"""
    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter(Q(position__project__owner_id=self.request.user.id) &
                                                             (Q(status='p')))
        context['projects'] = Project.objects.filter(owner=self.request.user)

        return context


class AcceptedApplicationsView(LoginRequiredMixin, ListView):
    """shows all applicants that have been accepted for projects the logged in user created"""

    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter(Q(position__project__owner_id=self.request.user.id) &
                                                                  (Q(status='a')))
        context['projects'] = Project.objects.filter(owner=self.request.user)

        return context


class RejectedApplicationsView(LoginRequiredMixin, ListView):
    """shows all applicants that have been rejected for projects the logged in user created"""

    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter(Q(position__project__owner_id=self.request.user.id) &
                                                                  (Q(status='r')))

        context['projects'] = Project.objects.filter(owner=self.request.user)

        return context


@login_required
def create_project(request):
    """allows users to create a project"""
    if request.method == 'POST':
        project_form = forms.CreateProjectForm(request.POST, prefix='project')
        position_formset = forms.PositionModelFormset(request.POST, prefix='position')

        if project_form.is_valid() and position_formset.is_valid():

            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()

            # more than one position can be added to the project.
            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.save()
            return redirect('profile:my_profile', pk=request.user.pk)

    else:
        position_formset = forms.PositionModelFormset(queryset=ProjectPosition.objects.none(), prefix='position')
        project_form = forms.CreateProjectForm(prefix='project')

    return render(request, 'user_profile/project_new.html',
                  {'project_form': project_form,
                   'position_formset': position_formset}
                  )


@login_required
def edit_project(request, pk):
    """allows user to edit a project"""
    project = get_object_or_404(Project, pk=pk)
    position = ProjectPosition.objects.filter(project__id=pk)

    if request.user == project.owner:

        if request.method == 'POST':
            position_formset = forms.PositionModelFormset(request.POST, queryset=position, prefix='position')
            project_form = forms.CreateProjectForm(request.POST, instance=project, prefix='project')

            if project_form.is_valid() and position_formset.is_valid():

                project = project_form.save(commit=False)
                project.owner = request.user
                project.save()

                # more than one position can be added to the project.
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
def delete_project(request, pk):
    """allows user to delete a project"""
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.owner:
        project.delete()
        return redirect('profile:my_profile', pk=request.user.pk)


@login_required
def apply_position(request, project_pk, position_pk):
    """allows user to apply for a position in a project"""
    project = get_object_or_404(Project, pk=project_pk)
    positions = ProjectPosition.objects.filter(project__id=project.pk,)

    for position in positions:
        if position.pk == position_pk:
            pending_status = position.applicant_set.create(status='p', name=request.user)
            pending_status.save()
        return redirect('profile:project', pk=project.pk)


@login_required
def reject_application(request, applicant_pk):
    """allows the project owner to reject an application"""
    applicant = get_object_or_404(Applicant, pk=applicant_pk)
    applicant.status = 'r'
    applicant.save()

    notify.send(
        applicant.name,
        recipient=applicant.name,
        verb=f'Unfortunately, you have been reject as a'
        f' {str(applicant.position.title)} in the project:'
        f' {str(applicant.position.project.title)}!')

    return redirect('profile:all_applications')


@login_required
def accept_application(request, applicant_pk):
    """allows the project owner to accept an application"""
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
    return redirect('profile:all_applications')


class ProjectListView(LoginRequiredMixin, ListView):
    """displays search results as a list"""
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
    """creates notifications for user"""
    template_name = "user_profile/notifications.html"
    model = User


class FilterProjectsView(LoginRequiredMixin, ListView):
    """Filters projects by positions"""
    model = ProjectPosition
    template_name = 'user_profile/filter_projects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(projectposition__title=self.kwargs.get('position'))
        return context
