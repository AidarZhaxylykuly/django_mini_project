from django.contrib import admin

from Blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'author')
    search_fields = ('id', 'title', 'author')


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at', 'post', 'author')
    search_fields = ('id', 'author', )