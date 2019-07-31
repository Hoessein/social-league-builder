from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns =\
    [
        path('', views.MyProfileView.as_view(), name='my_profile'),
        path('edit/', views.profile_edit, name='profile-update'),

        path('project/<int:pk>/', views.ProjectView.as_view(), name='project'),
        path('project/<int:pk>/update/', views.edit_project, name='project-update'),
        path('project/<int:pk>/apply/', views.apply_position, name='apply_position'),
        path('applications/applicant/<int:applicant_pk>/reject', views.reject_application,
             name='reject_application'),

        path('applications/applicant/<int:applicant_pk>/accept', views.accept_application,
             name='accept_application'),

        path('create_project/', views.create_project, name='create_project'),
        path('search_project/', views.ProjectListView.as_view(), name='search_project'),

        # path('applications/', views.CreateProject.as_view(), name='create_project'),
        path('notifications', views.NotificationsView.as_view(), name="notifications"),

        path('applications/', views.ApplicationsView.as_view(), name='applications'),
        path('new-applications/', views.NewApplicationsView.as_view(), name='new_applications'),
        path('rejected-applications/', views.RejectedApplicationsView.as_view(), name='rejected_applications'),
        path('accepted-applications/', views.AcceptedApplicationsView.as_view(), name='accepted_applications'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
