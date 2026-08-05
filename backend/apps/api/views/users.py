"""
API views for user endpoints.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.api.permissions import IsActiveUser
from apps.api.responses import ApiResponse
from apps.api.serializers.users import (
    LeaderboardUserSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.users.services import UserService


class UserProfileAPIView(APIView):
    """
    Retrieve authenticated user profile.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(self, request):
        user = UserService.get_user(
            user_id=request.user.id,
        )

        serializer = UserSerializer(user)

        return ApiResponse.success(
            data=serializer.data,
        )


class UserUpdateAPIView(APIView):
    """
    Update authenticated user profile.
    """

    permission_classes = (
        IsActiveUser,
    )

    def patch(self, request):
        serializer = UserUpdateSerializer(
            instance=request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = UserService.update_profile(
            user=request.user,
            username=serializer.validated_data.get(
                "username",
                request.user.username,
            ),
            first_name=serializer.validated_data.get(
                "first_name",
                request.user.first_name,
            ),
            last_name=serializer.validated_data.get(
                "last_name",
                request.user.last_name,
            ),
            language=serializer.validated_data.get(
                "language",
                request.user.language,
            ),
        )

        return ApiResponse.success(
            data=UserSerializer(user).data,
            status_code=status.HTTP_200_OK,
        )


class LeaderboardAPIView(APIView):
    """
    Return leaderboard ordered by experience.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(self, request):
        users = UserService.get_leaderboard()

        serializer = LeaderboardUserSerializer(
            users,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )