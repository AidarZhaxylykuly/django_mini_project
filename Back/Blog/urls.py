from django.urls import path
from Blog.views import comments_of_post, post_list, create_comment, create_post, edit_post, delete_post

urlpatterns = [
    # Posts' urls
    path('posts/create/', create_post, name='create_post'),
    path('posts/edit/<int:pk>/', edit_post, name='edit_post'),
    path('posts/delete/<int:pk>/', delete_post, name='delete_post'),
    path('posts/', post_list, name='post_list'),

    # Comments' urls
    path('posts/<int:pk>/comments/', comments_of_post, name='comments_of_post'),
    path('posts/<int:pk>/comments/create/', create_comment, name='create_comment'),
]
