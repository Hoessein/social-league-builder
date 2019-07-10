from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('', views.MyProfileView.as_view(), name='my_profile'),
    path('edit/', views.profile_edit, name='profile-update'),
    path('create_project', views.create_project, name='create_project'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
