from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from blogs.models import Blog, Category
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm


# ✅ Allow only staff / admin
def staff_required(user):
    return user.is_staff or user.is_superuser


# ---------------- DASHBOARD ----------------
@login_required(login_url='login')
@user_passes_test(staff_required)
def dashboard(request):
    category_count = Category.objects.count()
    blogs_count = Blog.objects.count()

    return render(request, 'dashboard/dashboard.html', {
        'category_count': category_count,
        'blogs_count': blogs_count,
    })


# ---------------- CATEGORIES ----------------
@login_required
@user_passes_test(staff_required)
def categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})


@login_required
@user_passes_test(staff_required)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/edit_category.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


# ---------------- POSTS ----------------
@login_required
@user_passes_test(staff_required)
def posts(request):
    posts = Blog.objects.all()
    return render(request, 'dashboard/posts.html', {'posts': posts})


@login_required
@user_passes_test(staff_required)
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.slug = f"{slugify(post.title)}-{post.id}"
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm()

    return render(request, 'dashboard/add_post.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.slug = f"{slugify(post.title)}-{post.id}"
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'dashboard/edit_post.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')


# ---------------- USERS ----------------
@login_required
@user_passes_test(staff_required)
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})


@login_required
@user_passes_test(staff_required)
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = AddUserForm()

    return render(request, 'dashboard/add_user.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'dashboard/edit_user.html', {'form': form})


@login_required
@user_passes_test(staff_required)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')
