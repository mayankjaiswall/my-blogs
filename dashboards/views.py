from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from blogs.models import Category, Blog
from .forms import CategoryForm, BlogForm

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    categories_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'categories_count': categories_count,
        'blogs_count': blogs_count,
    }
    
    return render(request, 'dashboards/dashboard.html', context)


@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    
    return render(request, 'dashboards/categories.html', context)


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been added.')
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'title': 'Add Category',
        'submit_label': 'Add Category',
    }
    return render(request, 'dashboards/category_form.html', context)


@login_required(login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been updated.')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'title': 'Edit Category',
        'submit_label': 'Update Category',
        'category': category,
    }
    return render(request, 'dashboards/category_form.html', context)


@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category has been deleted.')

    return redirect('categories')


def _unique_slug(title, exclude_id=None):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    queryset = Blog.objects.exclude(id=exclude_id) if exclude_id else Blog.objects.all()
    while queryset.filter(slug=slug).exists():
        counter += 1
        slug = f"{base_slug}-{counter}"
    return slug


@login_required(login_url='login')
def manage_posts(request):
    posts = Blog.objects.select_related('category').all().order_by('-created_at')
    context = {
        'posts': posts,
    }

    return render(request, 'dashboards/manage_posts.html', context)


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = _unique_slug(post.title)
            post.save()
            messages.success(request, 'Post has been created.')
            return redirect('manage_posts')
    else:
        form = BlogForm()

    context = {
        'form': form,
        'title': 'Create Post',
        'submit_label': 'Create Post',
    }
    return render(request, 'dashboards/post_form.html', context)


@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            if updated_post.title != post.title:
                updated_post.slug = _unique_slug(updated_post.title, exclude_id=post.id)
            updated_post.save()
            messages.success(request, 'Post has been updated.')
            return redirect('manage_posts')
    else:
        form = BlogForm(instance=post)

    context = {
        'form': form,
        'title': 'Edit Post',
        'submit_label': 'Update Post',
        'post': post,
    }
    return render(request, 'dashboards/post_form.html', context)


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been deleted.')

    return redirect('manage_posts')
