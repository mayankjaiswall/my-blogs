from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render   

from .forms import LoginForm, RegistrationForm

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
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
        
    return render(request, 'register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, 'You are now logged in.')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'home')
    else:
        form = LoginForm(request)

    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'login.html', context)
