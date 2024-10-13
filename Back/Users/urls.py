from django.urls import path
from django.views.generic import RedirectView

from Users.views import create_or_update_profile, profile_detail, follow_profile, unfollow_profile, logout_view, \
    login_view, register

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),

    path('profile/', create_or_update_profile, name='create_or_update_profile'),
    path('profile/<int:profile_id>/', profile_detail, name='profile'),

    path('profile/follow/<int:user_id>/', follow_profile, name='follow_profile'),
    path('profile/unfollow/<int:user_id>/', unfollow_profile, name='unfollow_profile'),

    path('', RedirectView.as_view(url='users/profile/'), name='home'),
]
