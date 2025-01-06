from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Posts

from django.contrib import messages
from .form import PostCreateForm
from .form2 import PostUpdateForm


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
""" def delete_post(request, post_id):
    return HttpResponse('Delete post') """

def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    password = request.POST.get('password')

    if request.method == 'POST':
        if password == post.password:
            post.delete()
            messages.success(request, 'Post deleted successfully')
            return redirect('posts:list')
        else:
            messages.error(request, 'Password is incorrect')
            return redirect('posts:read', post_id=post.id)

# List
""" def get_posts(request):
    return HttpResponse('Get List of posts') """

def get_posts(request):
    page = request.GET.get('page', 1)
    posts = Posts.objects.all().order_by('-created_at') # 최신순으로 정렬

    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')

    # search
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
        if searchType == 'all':
            posts = posts.filter(
                Q(title__contains=searchKeyword) |
                Q(content__contains=searchKeyword) |
                Q(username__contains=searchKeyword)
            )
        elif searchType == 'title':
            posts = posts.filter(
                Q(title__contains=searchKeyword)
            )
        elif searchType == 'content':
            posts = posts.filter(
                Q(content__contains=searchKeyword)
            )
        elif searchType == 'username':
            posts = posts.filter(
                Q(username__contains=searchKeyword)
            )

    #pagination
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    # calculate the start index of the sequence
    start_index = paginator.count - (paginator.per_page * (page_obj.number -1))

    # calculate the sequence and add it to the post list
    for index, _ in enumerate(page_obj, start=0):
        page_obj[index].index_number = start_index - index

    #return render(request, 'posts/list.html', {'posts': page_obj})

    return render(request, 'posts/list.html', {
        'posts': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword,
    })