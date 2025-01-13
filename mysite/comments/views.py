from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

# Comment list
def get_comments(request):
    return HttpResponse('Get List of comments')

# Comment create
def create_comment(request):
    return JsonResponse({'message': 'Create comment'})

# Comment update
def update_comment(request, comment_id):
    return JsonResponse({'message': 'Update comment'})

# Comment delete
def delete_comment(request, comment_id):
    return JsonResponse({'message': 'Delete comment'})


