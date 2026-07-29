from django.contrib import messages
from django.shortcuts import redirect, render   

from .forms import RegistrationForm

from abouts.models import About
from blogs.models import Blog, Category

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-created_at')
    posts = Blog.objects.filter(status='Published').order_by('-created_at')[:2]  # Limit to the latest 2 posts


    try:
        about = About.objects.get()  # Assuming there's only one About instance
    except:
        about = None  # Handle the case where no About instance exists
    context = {
        'featured_posts': featured_posts,   
        'posts': posts,
        'about': about
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
        
    return render(request, 'register.html', context)
