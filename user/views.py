from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
import uuid

User=get_user_model()

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

# def login_view(request):

#     form = LoginForm()

#     if request.method == 'POST':

#         form = LoginForm(
#             request,
#             data=request.POST
#         )

#         if form.is_valid():

#             email = form.cleaned_data.get('username')

#             password = form.cleaned_data.get('password')

#             user = authenticate(
#                request,
#                email=email,
#                password=password
#             )

#             if user is not None:

#                 login(request, user)

#                 return redirect('home')
            
#     context = {
#         'form':form
#     }

#     return render(
#         request,
#         'login.html',
#         context
#     )

# def logout_view(request):

#     logout(request)

#     return redirect('login')

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

def delete_user(request, slug):
    user = User.objects.get(slug=slug)

    if request.POST:
        user.delete()
        return redirect('/')

    return render(request, 'delete_user.html', {'user': user})

def update_user(request, slug):
    user = User.objects.get(slug=slug)

    if request.POST:
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.FILES.get('picture'):
            user.picture = request.FILES.get('picture')

        user.save()
        return redirect('/')

    return render(request, 'update_user.html', {'user': user})

def create_user(request):
    if request.POST:
        name=request.POST.get('first_name')
        surename=request.POST.get('last_name')
        picture=request.FILES.get('picture')

        user=User.objects.create(
            first_name=name,
            last_name=surename,
            email=f"{name}{surename}{str(uuid.uuid4())[:3]}",
            picture=picture
        )
        return redirect('/')
    return render(request,'create_user.html')

def user_view(request,slug):
    one_user=User.objects.get(slug=slug)
    if request.method == "POST":
        one_user = request.user
        one_user.first_name = request.POST.get("first_name")
        one_user.last_name = request.POST.get("last_name")
        one_user.phone_number = request.POST.get("phone_number")
        one_user.email = request.POST.get("email")

    return render(request,'user_view.html',{'user':one_user})