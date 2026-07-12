from django.shortcuts import render   

from blogs.models import Blog, Category

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-created_at')
    posts = Blog.objects.filter(status='Published').order_by('-created_at')[:2]  # Limit to the latest 2 posts


    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'posts': posts,
    }

    return render(request, 'home.html', context)