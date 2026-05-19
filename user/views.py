from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import CustomUser

user = get_user_model()

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

# @login_required
# def profile_view(request):

#     context = {
#         'user': request.user
#     }

#     return render(
#         request,
#         'profile.html',
#         context
#     )

@login_required
def profile_view(request):
    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

@login_required
def user_list_view(request):
    users = CustomUser.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'users': users})


@login_required
def user_detail_view(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    return render(request, 'user_view.html', {'user_obj': user})


@login_required
def user_create_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    return render(request, 'create_user.html', {'form': form})


@login_required
def user_update_view(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-detail', slug=user.slug)
    return render(request, 'update_user.html', {'form': form, 'user_obj': user})


@login_required
def user_delete_view(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    return render(request, 'delete_user.html', {'user_obj': user})
