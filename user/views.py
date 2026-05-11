from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

from . import models

User=get_user_model()


def run(request):
    users = User.objects.all()
    return render(request,'index.html',{'users': users})


def users_view(request):
    users=User.objects.all()
    return render(request,'user_view.html',{'users': users})


def create_user(request):

    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        picture=request.FILES.get('picture')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            picture=picture,
        )

        return redirect('/')

    return render(request,'create_user.html')


def update_user(request, slug):
    user=get_object_or_404(models.CustomUser, slug=slug)

    if request.method=="POST":
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        if request.FILES.get('picture'):
            user.picture=request.FILES.get('picture')
        user.save()

        return redirect('/')

    return render(request,'update_user.html',{'user': user})


def delete_user(request, slug):

    user=get_object_or_404(models.CustomUser, slug=slug)

    if request.method=="POST":
        user.delete()
        return redirect('/')

    return render(request,'delete_user.html',{'user': user})
