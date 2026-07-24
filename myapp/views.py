from django.shortcuts import render, redirect
from .models import Feature
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def index(request):

    # Retrieve all features from the database
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})


def register(request):

    # Handle the registration form submission
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