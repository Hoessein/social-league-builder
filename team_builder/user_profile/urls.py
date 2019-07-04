from django.urls import path, include


from . import views

urlpatterns = [

    path('', views.MyProfileView.as_view(), name='my_profile'),
    path('edit/', views.profile_edit, name='profile-update'),

]