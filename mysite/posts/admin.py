"""  admin: grace 
 password: user
 email: manager1020@gmail.com  """


from django.contrib import admin

# Register your models here.
from .models import Posts 
from comments.models import Comments # 관리자 페이지에 댓글 연동

# 게시글 조회할 때 댓글도 같이 조회
class CommentsInline(admin.TabularInline): # TabularInline: 테이블 형식으로 보여줌
    model = Comments # 댓글 모델
    extra = 1 # 추가로 보여줄 댓글 수

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_at', )
    inlines = [CommentsInline] # 댓글을 같이 보여줌

admin.site.register(Posts, PostsAdmin)
