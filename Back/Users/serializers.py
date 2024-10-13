from rest_framework import serializers

from Users.models import Profile, Follow


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "profile_picture")


class FollowSerializer(serializers.Serializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following")