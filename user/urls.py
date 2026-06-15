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
    path('users/', views.user_list_view, name='user-list'),
    path('users/create/', views.user_create_view, name='user-create'),
    path('users/<slug:slug>/', views.user_detail_view, name='user-detail'),
    path('users/<slug:slug>/update/', views.user_update_view, name='user-update'),
    path('users/<slug:slug>/delete/', views.user_delete_view, name='user-delete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('posts/',views.post_list_view,name='post_list'),
    path('posts/create/', views.post_create_view, name='post_create'),
    path('posts/<slug:slug>/update/', views.post_update_view, name='post_update'),
    path('posts/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('search/', views.search_posts, name='search_posts'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_toggle, name='like_toggle'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('popular/', views.popular_posts, name='popular_posts'),
    ]