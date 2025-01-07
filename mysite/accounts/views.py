from django.shortcuts import render

from django.http import HttpResponse

# signup
def register_account(request):
    return HttpResponse("Register account")

# login
def login_account(request):
    return HttpResponse("Login account")

# logout
def logout_account(request):
    return HttpResponse("Logout account")

# profile
def profile_profile(request):
    return HttpResponse("Profile account")

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



