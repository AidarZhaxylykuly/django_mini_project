from django.contrib import admin

from Users.models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'profile_picture')
    search_fields = ('id', 'user')


@admin.register(Follow)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')
    search_fields = ('id',)

