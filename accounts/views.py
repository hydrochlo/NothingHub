from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import User

# def register(request):
#     return render(request, 'accounts/register.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 1. Check what credentials Django receives
            print(f"--- DEBUG: Attempting login for username: {username} ---")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 2. Authenticated successfully -> Log user in
                auth_login(request, user)
                print(f"--- DEBUG: Login SUCCESS for user: {user.username} ---")
                return redirect('home') # Replace 'home' with your default logged-in route
            else:
                # 3. Authentication failed
                print("--- DEBUG: Authentication FAILED! user is None ---")
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')