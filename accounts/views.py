from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import User

# def register(request):
#     return render(request, 'accounts/register.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Use your custom manager method to save the user
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            # Optional: set phone number or active status before saving
            user.phone_number = form.cleaned_data['phone_number']
            user.is_active = True  # Activate account immediately
            user.save()

            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})