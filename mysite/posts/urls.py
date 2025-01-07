# post 등록, 조회, 수정, 삭제를 위한 url 

from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('admin/', admin.site.urls),
    path('<int:post_id>/', views.get_post, name='read'),
    path('<int:post_id>/update/', views.update_post, name='update'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
    path('', views.get_posts, name='list'),
    path('<int:post_id>/download/', views.download_file, name='download'), 
    path('tinymce/', include('tinymce.urls')),
]

