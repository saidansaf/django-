from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def home_view(request):

    return render(request, 'home.html')

def register_view(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    return render(request,'register.html',{'form':form})

def login_view(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            email = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user = authenticate(
               request,
               email=email,
               password=password
            )

            if user is not None:

                login(request, user)

                return redirect('home')
            
    context = {
        'form':form
    }

    return render(
        request,
        'login.html',
        context
    )

def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def profile_view(request):

    context = {
        'user': request.user
    }

    return render(
        request,
        'profile.html',
        context
    )