from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import UpdateView
from django.db import transaction
from django.forms.models import inlineformset_factory, modelformset_factory
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.db.models import Exists, OuterRef




from notifications.signals import notify



from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Profile, Project, ProjectPosition, Applicant, ProjectSkill, ProfileSkill

from . import forms


def index(request):

    projects = Project.objects.filter()

    return render(request, 'index.html', {'projects': projects})


def profile_edit(request):
    instance = request.user.profile
    skill_instance = ProfileSkill.objects.filter(profile__user_id=request.user.id).first()

    if request.method == 'POST':
        profile_form = forms.EditProfileForm(request.POST, instance=instance)
        user_form = forms.EditUserForm(request.POST, request.FILES, instance=request.user)
        skill_form = forms.ProfileSkillForm(request.POST, instance=skill_instance)

        if profile_form.is_valid() and user_form.is_valid() and skill_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            skill = skill_form.save(commit=False)
            skill.profile = profile
            skill.save()
            return redirect('profile:my_profile')

    else:
        profile_form = forms.EditProfileForm(instance=instance)
        user_form = forms.EditUserForm(request.POST or None, instance=request.user,)
        skill_form = forms.ProfileSkillForm(instance=skill_instance)

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
        context['skills'] = ProfileSkill.objects.filter(profile__user=self.request.user)
        context['project'] = Project.objects.filter(owner=self.request.user)
        return context


# def create_project(request):
#     if request.method == 'POST':
#         create_project_form = forms.CreateProjectForm(request.POST,)
#         create_project_position_form = forms.CreateProjectPositionForm(request.POST,)
#
#         if create_project_form.is_valid() and create_project_position_form.is_valid():
#             create_project_position_form.save()
#             create = create_project_form.save(commit=False)
#             create.owner = request.user
#             create.save()
#             return redirect('profile:my_profile')
#
#     else:
#         create_project_form = forms.CreateProjectForm()
#         create_project_position_form =forms.CreateProjectPositionForm()
#
#     return render(request,
#                   'user_profile/project_new.html',
#                   {'create_project_form': create_project_form,
#                    'create_project_position_form': create_project_position_form
#                   project }
#                   )


class ProjectView(DetailView):
    template_name = 'user_profile/project.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.all().get(pk=self.kwargs.get('pk'))

        # you have already applied
        # maak een lijst met gebruikers
        # kijk of inlgelogde gebruiker in die lijst zit
        context['positions'] = ProjectPosition.objects.filter(project__id=self.kwargs.get('pk'))

        # applicants = position.applicant_set.all()
        # lista = []
        #
        # for x in hey:
        #     lista.append(x.name.pk)
        #     print(lista)
        #
        # context['popo'] = lista
        user_list = 'hhhhh'

        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        context['user_list'] = user_list


        return context


class ApplicationsView(ListView):
    template_name = 'user_profile/applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = Applicant.objects.filter()
        return context


class NewApplicationsView(ListView):
    template_name = 'user_profile/new_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_applicants'] = Applicant.objects.filter(status='p')
        return context


class AcceptedApplicationsView(ListView):
    template_name = 'user_profile/accepted_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_applicants'] = Applicant.objects.filter(status='a')
        return context


class RejectedApplicationsView(ListView):
    template_name = 'user_profile/rejected_applications.html'
    model = Applicant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rejected_applicants'] = Applicant.objects.filter(status='r')
        return context


def create_project(request):
    # something = forms.CreateProjectForm(request.POST, )

    # formset = inlineformset_factory(Project, ProjectPosition, extra=1, max_num=3, form=forms.CreateProjectForm)
    # dick = inlineformset_factory(Project, ProjectPosition, form=forms.CreateProjectForm)
    # form = forms.ProjectFormSet(request.POST, instance=None)

    if request.method == 'POST':
        project_form = forms.CreateProjectForm(request.POST, prefix='project')
        position_formset = forms.PositionModelFormset(request.POST, prefix='position')

        if project_form.is_valid() and position_formset.is_valid():

            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            print(project, 'DIT IS PROJECTTTTTTTTTTTTTT')

            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.save()
                print(position, 'DIT IS POSITIONNNNNNNNNNNN')

            return redirect('profile:my_profile')

    else:
        position_formset = forms.PositionModelFormset(queryset=ProjectPosition.objects.none(), prefix='position')
        project_form = forms.CreateProjectForm(prefix='project')

    return render(request, 'user_profile/project_new.html',
                  {'project_form': project_form,
                   'position_formset': position_formset}

    )



def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    position = ProjectPosition.objects.filter(project__id=pk)

    if request.method == 'POST':
        position_formset = forms.PositionModelFormset(request.POST, queryset=position, prefix='position')
        project_form = forms.CreateProjectForm(request.POST, instance=project, prefix='project')

        # # print('i can make it past here')
        # print('TEST', position_form.data)
        # print('TEST', project_form.data)

        if project_form.is_valid() and position_formset.is_valid():

            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            print(project, 'DI IS PROJECTTTTTTTTTTTTTT')

            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.save()
                print(position, 'DIT IS POSITIONNNNNNNNNNNN')
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


#     project = get_object_or_404(Project, pk=pk)
#
#     if request.method == 'POST':
#         # formset = PositionFormset(queryset=ProjectPosition.objects.filter(project__id=project.id))
#         formset = PositionFormset(request.POST, instance=project)
#
#         if formset.is_valid():
#             #the language is supposed to have a programmer.
#             #the associated programmer is not done yet.
#             formset.save()
#             # for instance in instances:
#             #     instance.project_id=project.id
#             #     instance.save()
#             return redirect('profile:project', pk=project.pk)
#
#     formset = PositionFormset(instance=project)
#
#     # formset = PositionFormset(queryset=ProjectPosition.objects.filter(project__id=project.id))
#
#     return render(request,
#                   'user_profile/project_edit.html',
#                   {'formset': formset,
#                    }
#                   )
#
def apply_position(request, project_pk, position_pk):
    project = get_object_or_404(Project, pk=project_pk)
    positions = ProjectPosition.objects.filter(project__id=project.pk,)
    print(position_pk, 'OALKJDFLKAJDSFLKAJSDLFKJ')
    kk = ProjectPosition.objects.get(id=position_pk)
    print(kk.applicant_set.all(), 'hopi')

    for position in positions:
        if position.pk == position_pk:
            pending_status = position.applicant_set.create(status='p', name=request.user)
            pending_status.save()
            print("STATUS AANGEPAST!", pending_status)

        # for applicant in position.applicant_set.all().values('name'):

        return redirect('profile:project', pk=project.pk)

def reject_application(request, applicant_pk):
    # project = get_object_or_404(Project, pk=project_pk)
    # position = ProjectPosition.objects.get(project__id=project.pk)

    applicant = get_object_or_404(Applicant, pk=applicant_pk)

    # reject_status = position.applicant_set.create(status='r',)
    # reject_status.save()

    applicant.status = 'r'

    applicant.save()


    notify.send(
        applicant.name, recipient=applicant.name, verb=f'Unfortunately, you have been reject as a {str(applicant.position.title)} in the project: {str(applicant.position.project.title)}...')

    return redirect('profile:applications')


def accept_application(request, applicant_pk):
    # project = get_object_or_404(Project, pk=project_pk)
    applicant = get_object_or_404(Applicant, pk=applicant_pk)

    # position = ProjectPosition.objects.get(project__id=project.pk)
    applicant.status = 'a'
    # accept_status = position.applicant_set.create(status='a',)

    applicant.position.filled = True

    applicant.save()

    notify.send(
        applicant.name, recipient=applicant.name, verb=f'Congratulations, you have been accepted as a {str(applicant.position.title)} in the project: {str(applicant.position.project.title)}...')

    return redirect('profile:applications')

# def search_project(request):
#     query = request.GET.get('q')
#     project = Project.objects.filter(title__icontains=query)
#     return render(request, 'user_profile/search_list.html', {'project': project})


class ProjectListView(ListView):
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

# apply knop:
# als ingelogde gebruiker heeft applied dan knop niet tonen
    # melding je hebt applied

# als status accepted is voor position dan knop niet tonen
    # dan positie is ingevuld tonen

# als status rejected is knop tonen

class NotificationsView(ListView):
    template_name = "user_profile/notifications.html"
    model = User
