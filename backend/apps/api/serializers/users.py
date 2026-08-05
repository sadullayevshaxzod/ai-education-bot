"""
Serializers for user-related API endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user information.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "telegram_id",
            "username",
            "first_name",
            "last_name",
            "language",
            "role",
            "xp",
            "level",
            "is_active",
            "last_activity",
        )
        read_only_fields = (
            "id",
            "role",
            "xp",
            "level",
            "is_active",
            "last_activity",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Telegram user.
    """

    class Meta:
        model = User
        fields = (
            "telegram_id",
            "username",
            "first_name",
            "last_name",
            "language",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "language",
        )


class LeaderboardUserSerializer(serializers.ModelSerializer):
    """
    Serializer for leaderboard.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "level",
            "xp",
        )