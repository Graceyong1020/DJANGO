from django.shortcuts import render

from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import AccountDeleteForm, RegisterForm, LoginForm, ProfileUpdateForm, PasswordUpdateForm, UsernameFindForm, PasswordResetForm

import random
import string

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
""" def get_profile(request):
    return HttpResponse("Profile account") """

@login_required(login_url='auth:login')
def get_profile(request):
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

# profile update
""" def update_profile(request):
    return HttpResponse("Update account") """

@login_required(login_url='auth:login')
def update_profile(request):
    form = ProfileUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request. user)
            messages.success(request, 'Profile updated successfully')
            return redirect('auth:profile')
        else:
            messages.error(request, 'Profile update failed')
        
    return render(request, 'accounts/update_profile.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# password change
""" def update_password(request):
    return HttpResponse("Change password") """

@login_required(login_url='auth:login')
def update_password(request):
    form = PasswordUpdateForm()

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']

            user = authenticate(request, username=request.user.username, password=password)
            if user is None:
                messages.error(request, 'Invalid password')
                return redirect('auth:update_password')
           
            user = request.user
            user.set_password(password1)
            user.save()

            logout(request)
            messages.success(request, 'Password updated successfully')
            return redirect('auth:login')
        else:
            messages.error(request, 'Password update failed')

    return render(request, 'accounts/update_password.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# find id
def find_username(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = UsernameFindForm()

    if request.method == 'POST':
        form = UsernameFindForm(request.POST) 
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            user = User.objects.filter(first_name=first_name, email=email).first()
            if user:
                messages.success(request, f'Your username is {user.username}')
                return redirect('auth:login')
            else:
                messages.error(request, 'User not found')
        else: 
            messages.error(request, 'Invalid input')
    return render(request, 'accounts/find_username.html', {'form': form, 'message_class': 'col-4 mx-auto'})

# reset password
def reset_password(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            user = User.objects.filter(first_name=first_name, username=username, email=email).first()
            if user:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                user.set_password(password)
                user.save()

                messages.success(request, f'Your new password is {password}')
                return redirect('auth:login')
            else:
                messages.error(request, 'User not found')

    return render(request, 'accounts/reset_password.html', {'form': form, 'message_class': 'col-4 mx-auto'})

# delete account
""" def delete_account(request):
    return HttpResponse("Delete account") """

@login_required(login_url='auth:login')
def delete_account(request):
    form = AccountDeleteForm()

    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(first_name=first_name, username=username, email=email).first()
            authenticated = authenticate(request, username=username, password=password)
            if user and authenticated is not None:
                user.delete()
                logout(request)
                messages.success(request, 'Account deleted successfully')
                return redirect('auth:login')
            else:
                messages.error(request, 'User not found or password is incorrect')

    return render(request, 'accounts/delete_account.html', {'form': form, 'message_class': 'col-4 mx-auto'})



