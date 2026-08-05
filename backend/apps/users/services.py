"""
Business logic for the users application.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.common.choices import Language

from .choices import UserRole
from .models import User


class UserService:
    """
    User business logic.
    """

    @staticmethod
    @transaction.atomic
    def get_or_create_user(
        *,
        telegram_id: int,
        username: str = "",
        first_name: str,
        last_name: str = "",
    ) -> tuple[User, bool]:
        """
        Get an existing user or create a new one.
        """

        return User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "language": Language.UZ,
                "role": UserRole.STUDENT,
            },
        )

    @staticmethod
    def get_user(*, user_id: int) -> User:
        """
        Return user by id.
        """

        return User.objects.get(pk=user_id)

    @staticmethod
    @transaction.atomic
    def update_profile(
        *,
        user: User,
        username: str,
        first_name: str,
        last_name: str,
        language: str,
    ) -> User:
        """
        Update user profile.
        """

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.language = language

        user.save(
            update_fields=[
                "username",
                "first_name",
                "last_name",
                "language",
            ]
        )

        return user

    @staticmethod
    def get_leaderboard():
        """
        Return users ordered by experience points.
        """

        return User.objects.order_by(
            "-xp",
            "-level",
            "first_name",
        )

    @staticmethod
    def update_last_activity(user: User) -> None:
        """
        Update user's last activity time.
        """

        user.last_activity = timezone.now()
        user.save(update_fields=["last_activity"])

    @staticmethod
    def set_language(
        user: User,
        language: str,
    ) -> None:
        """
        Update user language.
        """

        user.language = language
        user.save(update_fields=["language"])

    @staticmethod
    def set_role(
        user: User,
        role: str,
    ) -> None:
        """
        Update user role.
        """

        user.role = role
        user.save(update_fields=["role"])

    @staticmethod
    def add_xp(
        user: User,
        xp: int,
    ) -> None:
        """
        Add experience points.
        """

        if xp <= 0:
            return

        user.xp += xp
        user.save(update_fields=["xp"])