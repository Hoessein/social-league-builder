from django.urls import path

from . import views

urlpatterns = [

    path('something/', views.something, name='something'),

]