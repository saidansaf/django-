from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_view, name='user_list'),

    path('update/<slug:slug>/', views.update_user, name='update_user'),
    path('delete/<slug:slug>/', views.delete_user, name='delete_user'),
]