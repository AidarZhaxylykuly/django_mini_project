from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile_users",
        null=False,
        blank=False
    )
    bio = models.TextField()
    profile_picture = models.ImageField()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f'id: {self.id}, user: {self.user}, bio: {self.bio}, profile_picture: {self.profile_picture}'


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follow_followers",
        null=False,
        blank=False
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follow_followings",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"

    def __str__(self):
        return f'id:{self.id}, follower:{self.follower}, following:{self.following}'