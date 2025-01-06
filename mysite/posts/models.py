from django.db import models

# db에 연동할 model을 정의

# Create your models here.
class Posts(models.Model):
    title = models.CharField(verbose_name="title", max_length=100)
    content = models.TextField(verbose_name="content")
    password = models.CharField(verbose_name="password", max_length=100)
    username = models.CharField(verbose_name="username", max_length=100)
    filename = models.CharField(verbose_name="filename", max_length=100, null=True, blank=True)
    original_filename = models.CharField(verbose_name="original filename", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated", auto_now=True)

#verbose_name: admin 페이지에서 해당 필드의 이름을 지정

    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "List of posts"
    
    def __str__(self):
        return self.title
