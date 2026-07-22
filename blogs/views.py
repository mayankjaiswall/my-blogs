from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Blog, Category
# Create your views here.


def posts_by_category(request, category_id):
    #Fetch the blogs for the given category_id from the database
    blogs = Blog.objects.filter(category_id=category_id, status='Published').order_by('-created_at')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, '404.html', status=404)  # Return 404 page if category does not exist
    
    context = {
        'blogs': blogs,
        'category': category
    }
    
    return render(request, 'posts_by_category.html',context)


def blog_detail(request, slug):
    try:
        blog = Blog.objects.get(slug=slug, status='Published')
    except Blog.DoesNotExist:
        return render(request, '404.html', status=404)  # Return 404 page if blog does not exist

    context = {
        'blog': blog
    }

    return render(request, 'blog_detail.html', context)