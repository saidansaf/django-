from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserUpdateForm, UserProfileUpdateForm,PostForm,CommentForm
from .models import CustomUser, Post,UserProfile,Comment,Like
from django.db.models import Q, Count

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

@login_required
def profile_edit_view(request):
    user_form = ProfileUpdateForm(instance=request.user)
    profile_form = UserProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':

        user_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        profile_form = UserProfileUpdateForm(
            request.POST,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(request, 'Profil muvaffaqiyatli yangilandi! ✅')
            return redirect('profile')

        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos tekshiring.')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile_edit.html', context)


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Akkaunt muvaffaqiyatli o'chirildi.")
        return redirect('register')

    return render(request, 'profile_delete_confirm.html')

def post_list_view(request):
    posts = Post.objects.prefetch_related('tags').select_related('author').all()
    return render(request,'post_list.html',{'posts': posts})    

def post_detail_view(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related('tags').select_related('author'), slug=slug)
    comments = post.comments.all()
    comment_form = CommentForm()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'likes_count': post.likes.count(),
        'comments_count': comments.count(),
    }
    return render(request, 'post_detail.html', context)

@login_required
def post_create_view(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)

    return render(request, 'post_create.html', {'form': form})

@login_required
def post_update_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)

    return render(request, 'post_update.html', {'form': form, 'post': post})


@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'post_delete.html', {'post': post})

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).distinct()

    context = {
        'posts': posts,
        'query': query,
        'posts_count': posts.count(),
    }
    return render(request, 'search_results.html', context)

@login_required
def like_toggle(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related('tags').select_related('author'), slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post_detail', slug=post.slug)

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related('tags').select_related('author'), slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('post_detail', slug=post.slug)

def popular_posts(request):
    posts = Post.objects.annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-total_likes', '-total_comments')

    return render(request, 'popular_posts.html', {'posts': posts})    