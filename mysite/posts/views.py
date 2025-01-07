#from django.http import HttpResponse

# register view 
import os
import uuid
from mysite import settings

# file download 
from urllib.parse import quote # url encoding
from django.http import HttpResponse # http response

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 암호화 및 비교

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
        form = PostCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.password = make_password(form.cleaned_data['password'])
            post.save()

            # file upload
            if 'uploadFile' in request.FILES:
                filename = uuid.uuid4().hex
                file = request.FILES['uploadFile']

                # save path 
                file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(filename))
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                # save file
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                
                post.filename = filename
                post.original_filename = file.name
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
    post.password = post.password
    form = PostUpdateForm(instance=post)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            if check_password(form.cleaned_data['password'], post.password): # 비밀번호 확인
                post = form.save(commit=False)
                post.password = make_password(form.cleaned_data['password'])
                post.save()

                # delete file
                if form.cleaned_data.get('deleteFile'):
                    if post.filename:
                        # delete existing file
                        file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        post.filename = None
                        post.original_filename = None
                        post.save()

                # file upload
                if 'uploadFile' in request.FILES:
                    if post.filename:
                            # delete existing file
                            file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                            if os.path.exists(file_path):
                                os.remove(file_path)

                    filename = uuid.uuid4().hex
                    file = request.FILES['uploadFile']

                    # save path
                    file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(filename))
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))

                    # save file
                    with open(file_path, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)

                    post.filename = filename
                    post.original_filename = file.name
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
        if check_password(password, post.password):
            # delete file
            if post.filename:
                file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                if os.path.exists(file_path):
                    os.remove(file_path)

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

# file download
def download_file(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            encoded_filename = quote(post.original_filename)
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            return response
    return HttpResponse(status=404) # file not found