from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Category, Blog
from .forms import CategoryForm

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
