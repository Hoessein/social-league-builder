from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    # path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogOutView.as_view(), name='signout')

]