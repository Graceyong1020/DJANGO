from django.shortcuts import render

from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ProfileUpdateForm

# signup
""" def register_account(request):
    return HttpResponse("Register account")
 """
def register_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email']
            )
            user.save()
            messages.success(request, 'Account created successfully')
        else:
            messages.error(request, 'Account creation failed')
    
    return render(request, 'accounts/register.html', {'form': form, 'message_class': 'col-4 mx-auto'})


# login
""" def login_account(request):
    return HttpResponse("Login account") """
def login_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # if login is failed
            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('auth:login')
            # if login is successful
            login(request, user)
            return redirect('auth:profile')
        else:
            messages.error(request, 'Enter a valid username and password')
    
    return render(request, 'accounts/login.html', {'form': form, 'message_class': 'col-4 mx-auto'})



# logout
""" def logout_account(request):
    return HttpResponse("Logout account") """
def logout_account(request):
    logout(request)
    return redirect('auth:login')

# profile
""" def profile_profile(request):
    return HttpResponse("Profile account") """

@login_required(login_url='auth:login')
def profile_profile(request):
    form = ProfileUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Profile updated successfully')
            return redirect('auth:profile')
        else:
            messages.error(request, 'Profile update failed')
            
    return render(request, 'accounts/profile.html', {'message_class': 'col-4 mx-auto'})

# update
def update_profile(request):
    return HttpResponse("Update account")

# password change
def update_password(request):
    return HttpResponse("Change password")

# find id
def find_username(request):
    return HttpResponse("Find username")

# reset password
def reset_password(request):
    return HttpResponse("Reset password")

# delete account
def delete_account(request):
    return HttpResponse("Delete account")



