from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from Blog.forms import CommentForm, PostForm
from django.core.paginator import Paginator

from Blog.models import Comment, Post
from Blog.serializers import PostSerializer


@api_view(["GET"])
def comments_of_post(request, pk=None):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        comments = Comment.objects.filter(post=post)
        return render(request, 'post_detail.html', {
            'post': post,
            'values': comments,
            'form': CommentForm(),
        })


@login_required
@api_view(["POST"])
def create_comment(request, pk=None):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            author = request.user

            Comment.objects.create(post=post, content=content, author=author)
            return redirect('comments_of_post', pk=pk)
        else:
            return render(request, 'post_detail.html', {
                'post': post,
                'values': Comment.objects.filter(post=pk),
                'form': form,
            })


@api_view(["GET"])
def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    serialized_posts = PostSerializer(page_obj, many=True)
    return render(request, 'post_list.html', {'values': serialized_posts.data, 'query': query, 'page_obj': page_obj})


@login_required
@api_view(["GET", "POST"])
def create_post(request):
    if request.method == "GET":
        form = PostForm()
        user_posts = Post.objects.filter(author=request.user)
        return render(request, 'post_form.html', {
            'form': form,
            'user_posts': user_posts
        })

    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')

        return render(request, 'post_form.html', {
            'form': form,
            'user_posts': Post.objects.filter(author=request.user)
        })


@login_required
@api_view(["GET", "POST"])
def edit_post(request, pk):
    try:
        post = Post.objects.get(id=pk, author=request.user)
    except Post.DoesNotExist:
        return redirect('post_list')

    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, 'post_form.html', {'form': form})

    elif request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')

        return render(request, 'post_form.html', {'form': form})


@login_required
@api_view(["POST"])
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    post.delete()
    return redirect('post_list')
