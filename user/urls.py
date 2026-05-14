from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from .forms import LoginForm

urlpatterns = [
    path('',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    # path('login/',views.login_view,name='login'),
    # path('logout/',views.logout_view,name='logout'),
    path('login/',LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',views.profile_view,name='profile'),
]