from django import forms
from .models import Posts

#  update form
class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = Posts
        fields = ['title', 'content', 'username', 'password']

    # validation check for title
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError('Title is required')
        if len(title) < 2:
            raise forms.ValidationError('Title must be at least 2 characters')
        if len(title) > 100:
            raise forms.ValidationError('Title must be less than 100 characters')
        return title
    
    # validation check for content
    def clean_content(self):
        content = self.cleaned_data['content']
        if not content:
            raise forms.ValidationError('Content is required')
        return content
    
    # validation check for username
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('Username is required')
        if len(username) < 2:
            raise forms.ValidationError('Username must be at least 2 characters')
        if len(username) > 10:
            raise forms.ValidationError('Username must be less than 100 characters')
        return username
    
    # validation check for password
    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError('Password is required')
        if len(password) < 4:
            raise forms.ValidationError('Password must be at least 4 characters')
        if len(password) > 20:
            raise forms.ValidationError('Password must be less than 20 characters')
        return password