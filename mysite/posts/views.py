from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts

from django.contrib import messages
from .form import PostCreateForm
from .form2 import PostUpdateForm

# Create your views here.

# register
""" def create_post(request):
    return HttpResponse("Create post") """
def create_post(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
           post = form.save(commit=False)
           post.save()
           messages.success(request, 'Post created successfully')
           return redirect('posts:read', post_id=post.id)
        else:
            messages.error(request, 'Post creation failed')
    return render(request, 'posts/create.html', {'form': form})

# Read
""" def get_post(request, post_id):
    return HttpResponse('Get post')
 """
def get_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    return render(request, 'posts/read.html', {'post': post})

# Update
""" def update_post(request, post_id):
    return HttpResponse('Update post') """
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    form = PostUpdateForm(instance=post)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['password'] == post.password:
                post = form.save(commit=False)
                post.save()
                messages.success(request, 'Post updated successfully')
                return redirect('posts:read', post_id=post.id)
            else:
                messages.error(request, 'Password is incorrect')
        else:
            messages.error(request, 'Post update failed')
    return render(request, 'posts/update.html', {'form': form})


# Delete
def delete_post(request, post_id):
    return HttpResponse('Delete post')

# List
""" def get_posts(request):
    return HttpResponse('Get List of posts') """

def get_posts(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})