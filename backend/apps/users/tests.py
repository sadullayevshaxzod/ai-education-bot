"""
Tests for the users application.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.choices import Language

from .choices import UserRole
from .models import User
from .services import UserService


class UserServiceTests(TestCase):
    """
    Tests for UserService.
    """

    def test_create_new_user(self) -> None:
        """
        Should create a new user.
        """
        user, created = UserService.get_or_create_user(
            telegram_id=123456789,
            username="john_doe",
            first_name="John",
            last_name="Doe",
        )

        self.assertTrue(created)
        self.assertEqual(user.telegram_id, 123456789)
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.language, Language.UZ)
        self.assertEqual(user.role, UserRole.STUDENT)
        self.assertEqual(user.level, 1)
        self.assertEqual(user.xp, 0)

    def test_get_existing_user(self) -> None:
        """
        Should return existing user.
        """
        User.objects.create(
            telegram_id=123456789,
            username="john_doe",
            first_name="John",
        )

        user, created = UserService.get_or_create_user(
            telegram_id=123456789,
            username="another_username",
            first_name="Another",
        )

        self.assertFalse(created)
        self.assertEqual(user.username, "john_doe")

    def test_add_xp(self) -> None:
        """
        Should increase user XP.
        """
        user = User.objects.create(
            telegram_id=111111111,
            first_name="Ali",
        )

        UserService.add_xp(user, 50)

        user.refresh_from_db()

        self.assertEqual(user.xp, 50)

    def test_set_language(self) -> None:
        """
        Should update user language.
        """
        user = User.objects.create(
            telegram_id=111111111,
            first_name="Ali",
        )

        UserService.set_language(
            user,
            Language.EN,
        )

        user.refresh_from_db()

        self.assertEqual(user.language, Language.EN)

    def test_update_last_activity(self) -> None:
        """
        Should update last activity.
        """
        user = User.objects.create(
            telegram_id=111111111,
            first_name="Ali",
        )

        old_time = user.last_activity

        UserService.update_last_activity(user)

        user.refresh_from_db()

        self.assertGreaterEqual(
            user.last_activity,
            old_time,
        )