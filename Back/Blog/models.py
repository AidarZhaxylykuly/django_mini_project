from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_authors",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, content: {self.content}, created_at: {self.created_at}, author: {self.author}'


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comment_posts",
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_users",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'id: {self.id}, content: {self.content}, created_at: {self.created_at}, post: {self.post}, author: {self.author}'