import re
from django import forms
from django.contrib.auth.models import User

#  signup form
class RegisterForm(forms.ModelForm):
    username= forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username is required')
        if len(username) < 6:
            raise forms.ValidationError('Username must be at least 6 characters')
        if len(username) > 20:
            raise forms.ValidationError('Username must be less than 20 characters')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean_password1(self):
        password1= self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError('Password is required')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        
        # validation check for password
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least one digit')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter')
        if not any(char in "!@#$%^&*()-_+=~`[]{}|:;'<>,.?/" for char in password1):
            raise forms.ValidationError('Password must contain at least one special character')
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError('Password confirmation is required')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('First name is required')
        if len(first_name) < 2:
            raise forms.ValidationError('First name must be at least 2 characters')
        if len(first_name) > 4:
            raise forms.ValidationError('First name must be less than 4 characters')
        return first_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        if len(email) > 50:
            raise forms.ValidationError('Email must be less than 50 characters')
        if not re.match(r'^[a-zA-Z0-9+_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Email is invalid')
        return email

# login form
class LoginForm(forms.Form):
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    class Meta:
         model = User
         fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username is required')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password is required')
        return password

# profile update form
class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('First name is required')
        if len(first_name) < 2:
            raise forms.ValidationError('First name must be at least 2 characters')
        if len(first_name) > 4:
            raise forms.ValidationError('First name must be less than 4 characters')
        return first_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required')
        print(self.instance.id)
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email already exists')
        if len(email) > 50:
            raise forms.ValidationError('Email must be less than 50 characters')
        if not re.match(r'^[a-zA-Z0-9+_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Email is invalid')
        return email