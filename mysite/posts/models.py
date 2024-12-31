from django.db import models

# Create your models here.
class Posts(models.Model):
    title = models.CharField(verbose_name="title", max_length=100)
    content = models.TextField(verbose_name="content")
    password = models.CharField(verbose_name="password", max_length=100)
    username = models.CharField(verbose_name="username", max_length=100)
    created_at = models.DateTimeField(verbose_name="created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated", auto_now=True)

    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "List of posts"
    
    def __str__(self):
        return self.title
