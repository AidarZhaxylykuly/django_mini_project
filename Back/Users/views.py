from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from Users.models import Profile
from Users.forms import ProfileForm, CustomUserCreationForm
from django.contrib.auth.models import User
from Users.models import Follow
from django.contrib import messages


def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'profile.html', {'profile': profile})


@login_required
@api_view(["GET", "POST"])
def create_or_update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', profile_id=profile.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


def logout_view(request):
    logout(request)
    return redirect('post_list')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            profile = Profile.objects.create(
                user=user,
                bio=form.cleaned_data.get('bio'),
                profile_picture=form.cleaned_data.get('profile_picture')
            )
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_profile(request, user_id):
    try:
        following = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('profile', profile_id=user_id)

    if not Profile.objects.filter(user=following).exists():
        messages.error(request, "Profile for the following user does not exist.")
        return redirect('profile', profile_id=user_id)

    if Follow.objects.filter(follower=request.user, following=following).exists():
        messages.error(request, "Already following this profile.")
        return redirect('profile', profile_id=user_id)

    Follow.objects.create(follower=request.user, following=following)
    messages.success(request, "Successfully followed the profile.")
    return redirect('profile', profile_id=user_id)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_profile(request, user_id):
    try:
        following = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('profile', profile_id=user_id)

    try:
        follow = Follow.objects.get(follower=request.user, following=following)
    except Follow.DoesNotExist:
        messages.error(request, "You are not following this profile.")
        return redirect('profile', profile_id=user_id)

    follow.delete()
    messages.success(request, "Successfully unfollowed the profile.")
    return redirect('profile', profile_id=user_id)