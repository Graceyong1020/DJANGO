from django.shortcuts import render

#from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone

from .models import Comments
from posts.models import Posts

# Comment list
""" def get_comments(request):
    return HttpResponse('Get List of comments')
 """
def get_comments(post_id):
    comments = Comments.objects.filter(post_id=post_id).order_by('-created_at')
    comments_list = []
    for comment in comments:
        comments_list.append({
            'id': comment.id,
            'content': comment.content,
            'created_by': comment.created_by.first_name,
            'updated_by': comment.updated_by.first_name,
            'created_at': comment.created_at
                            .astimezone(timezone.get_current_timezone())
                            .strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at
                            .astimezone(timezone.get_current_timezone())
                            .strftime('%Y-%m-%d %H:%M:%S')
        })
    return comments_list


# Comment create
""" def create_comment(request):
    return JsonResponse({'message': 'Create comment'}) """

def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': 'You are not logged in.'})
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': 'Invalid post id.'})
        
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': 'Post not found.'})
        
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'result': 'error', 'message': 'Content is required.'})
        
        comment = Comments(
            post=post,
            content=content,
            created_by=request.user,
            updated_by=request.user
        )
        comment.save()

        comments = get_comments(post_id)
        return JsonResponse({'result': 'success', 'comments': comments})


# Comment update
""" def update_comment(request, comment_id):
    return JsonResponse({'message': 'Update comment'}) """
def update_comment(request, comment_id): 
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': 'You are not logged in.'})
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': 'Invalid post id.'})
        
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': 'Post not found.'})
        
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'result': 'error', 'message': 'Content is required.'})
        
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return JsonResponse({'result': 'error', 'message': 'Invalid comment id.'})
        
        comment = Comments.objects.get(id=comment_id)
        if not comment:
            return JsonResponse({'result': 'error', 'message': 'Comment not found.'})
        
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': 'You are not authorized to update this comment.'})
        
        # update comment
        comment.content = content
        comment.updated_by = request.user
        comment.save()

        # comment list
        comments = get_comments(post_id)

        return JsonResponse({'result': 'success', 'comments': comments})

# Comment delete
""" def delete_comment(request, comment_id):
    return JsonResponse({'message': 'Delete comment'}) """

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': 'You are not logged in.'})
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': 'Invalid post id.'})
        
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': 'Post not found.'})
        
        #content = request.POST.get('content')
        #if not content:
        #    return JsonResponse({'result': 'error', 'message': 'Content is required.'})
                
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return JsonResponse({'result': 'error', 'message': 'Invalid comment id.'})
        
        comment = Comments.objects.get(id=comment_id)
        if not comment:
            return JsonResponse({'result': 'error', 'message': 'Comment not found.'})
        
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': 'You are not authorized to delete this comment.'})
        
        # delete comment
        comment.delete()

        # comment list
        comments = get_comments(post_id)

        return JsonResponse({'result': 'success', 'comments': comments})


