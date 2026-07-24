from django.shortcuts import render, redirect, get_object_or_404
from .models import Feature, Post
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


# Handle the index page view
def index(request):

    # Retrieve all features from the database
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})


# Handle the registration form submission
def register(request):

    # Check if the request method is POST
    if request.method == 'POST':
        data = request.POST

        # Extract the form data
        username = data['username']
        email = data['email']
        password = data['password']
        password_repeat = data['password_repeat']

        # Check if the passwords match
        if password == password_repeat:

            # Check if the username/email already exists
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:

                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


# Handle the login form submission
def login(request):

    # Check if the request method is POST
    if request.method == 'POST':
        # Extract the form data
        data = request.POST
        username = data['username']
        password = data['password']

        # Authenticate the User
        user = auth.authenticate(username=username, password=password)

        # Check if the user is authenticated
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


# Handle the logout action
def logout(request):
    auth.logout(request)
    return redirect('/')


# Handle the post view
def posts(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            # Retrieve all posts by the logged-in user
            posts = request.user.blog_posts.all()
            return render(request, 'posts.html', {'posts': posts})
        else:
            messages.info(request, 'You need to be logged in to view your posts')
            return redirect('login')
    else:
        return redirect('/')

def post(request, slug):
    if request.method == 'GET':
        if request.user.is_authenticated:
            post = get_object_or_404(request.user.blog_posts, slug=slug)
            if post:
                return render(request, 'post.html', {'post': post})
            else:
                messages.info(request, 'Post not found')
                return redirect('posts')
        else:
            messages.info(request, 'You need to be logged in to view this post')
            return redirect('login')
    else:
        return redirect('posts')