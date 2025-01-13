from django.db import models

from django.contrib.auth.models import User

from posts.models import Posts

# comment model
class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name="post", related_name="comments")
    content = models.TextField(verbose_name="content")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="created by",
                                   null=True, blank=True, related_name="comments_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="updated by",
                                      null=True, blank=True, related_name="comments_updated_by")
    created_at = models.DateTimeField(verbose_name="created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated", auto_now=True)

    class Meta:
        db_table = "comments"
        verbose_name = "comment"
        verbose_name_plural = "List of comments"

    def __str__(self):
        return self.content
