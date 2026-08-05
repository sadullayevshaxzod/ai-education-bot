"""
API views for achievement endpoints.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.achievements.services import AchievementService
from apps.api.permissions import IsActiveUser
from apps.api.responses import ApiResponse
from apps.api.serializers.achievements import (
    AchievementSerializer,
    UserAchievementSerializer,
)


class AchievementListAPIView(APIView):
    """
    Return all available achievements.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(self, request):
        achievements = AchievementService.get_achievements()

        serializer = AchievementSerializer(
            achievements,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class UserAchievementListAPIView(APIView):
    """
    Return achievements unlocked by the authenticated user.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(self, request):
        achievements = AchievementService.get_user_achievements(
            user=request.user,
        )

        serializer = UserAchievementSerializer(
            achievements,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class AchievementDetailAPIView(APIView):
    """
    Return achievement details.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(
        self,
        request,
        achievement_id: int,
    ):
        achievement = AchievementService.get_achievement(
            achievement_id=achievement_id,
        )

        serializer = AchievementSerializer(
            achievement,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class UnlockAchievementAPIView(APIView):
    """
    Unlock an achievement for the authenticated user.
    """

    permission_classes = (
        IsActiveUser,
    )

    def post(
        self,
        request,
        achievement_id: int,
    ):
        achievement = AchievementService.get_achievement(
            achievement_id=achievement_id,
        )

        user_achievement = AchievementService.unlock_achievement(
            user=request.user,
            achievement=achievement,
        )

        if user_achievement is None:
            return ApiResponse.success(
                data=None,
                message="Achievement already unlocked.",
                status_code=status.HTTP_200_OK,
            )

        serializer = UserAchievementSerializer(
            user_achievement,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Achievement unlocked successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class CheckLevelAchievementsAPIView(APIView):
    """
    Unlock all achievements available for the user's current level.
    """

    permission_classes = (
        IsActiveUser,
    )

    def post(self, request):
        achievements = AchievementService.check_level_achievements(
            user=request.user,
        )

        serializer = UserAchievementSerializer(
            achievements,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Level achievements checked successfully.",
        )