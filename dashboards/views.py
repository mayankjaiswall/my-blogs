from django.shortcuts import render

from blogs.models import Category, Blog

# Create your views here.


def dashboard(request):
    categories_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'categories_count': categories_count,
        'blogs_count': blogs_count,
    }
    
    return render(request, 'dashboards/dashboard.html', context)