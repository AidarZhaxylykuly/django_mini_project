from django import forms
from django.contrib.auth.models import User

from Blog.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            "content": forms.Textarea(attrs={
                'placeholder': 'Enter your comment',
                'rows': 4,
                'cols': 40,
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

