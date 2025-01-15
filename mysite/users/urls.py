# 사용자 관리 앱 URL 설정

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.get_users, name='list'),
    path('<int:user_id>/', views.get_user, name='read'),
    path('<int:user_id>/delete/', views.delete_user, name='delete'),
]