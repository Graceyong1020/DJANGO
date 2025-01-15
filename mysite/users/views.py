from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User # 사용자 모델
from django.db.models import Q 
from django.core.paginator import Paginator # 페이징 처리
from django.shortcuts import render, get_object_or_404, redirect # render: 템플릿을 사용하여 HTML 페이지를 출력
from django.contrib import messages # 메시지 프레임워크


# user list
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    page = request.GET.get('page', 1)
    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')
    users = User.objects.all().order_by('username') # 사용자 목록을 이름 순으로 정렬

    # search
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
        if searchType == 'all':
            users = users.filter(
                Q(username__contains=searchKeyword) |
                Q(first_name__contains=searchKeyword) |
                Q(email__contains=searchKeyword)
            )

    # pagination
    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page)

    # 현재 페이지의 첫 번째 사용자 번호 계산
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))

    # 순번 계산하여 사용자 리스트에 추가
    for index, _ in enumerate(page_obj, start=0):
        page_obj[index].index_number = start_index - index

    return render(request, 'users/list.html', {
        'users': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword,
    })

# user detail
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/read.html', {'user': user})

# delete user
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'You cannot delete the superuser.')
        return redirect('users:read', user_id=user.id)
    
    user.delete()
    return redirect('users:list')