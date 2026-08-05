"""
Tests for education API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import Language
from apps.education.models import Lesson, Subject
from apps.users.choices import UserRole
from apps.users.models import User


class EducationAPITests(APITestCase):
    """
    Tests for education API endpoints.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language=Language.UZ,
            role=UserRole.STUDENT,
            is_active=True,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.subject = Subject.objects.create(
            name="Python",
            slug="python",
            description="Python course",
            order=1,
        )

        self.lesson1 = Lesson.objects.create(
            subject=self.subject,
            title="Variables",
            description="Variables lesson",
            order=1,
            xp_reward=100,
        )

        self.lesson2 = Lesson.objects.create(
            subject=self.subject,
            title="Functions",
            description="Functions lesson",
            order=2,
            xp_reward=150,
        )

        self.subjects_url = reverse(
            "api:subject-list",
        )

        self.lessons_url = reverse(
            "api:lesson-list",
            kwargs={
                "subject_id": self.subject.id,
            },
        )

        self.lesson_detail_url = reverse(
            "api:lesson-detail",
            kwargs={
                "lesson_id": self.lesson1.id,
            },
        )

        self.next_lesson_url = reverse(
            "api:next-lesson",
            kwargs={
                "lesson_id": self.lesson1.id,
            },
        )

    def test_get_subjects(self) -> None:
        """
        Should return all active subjects.
        """

        response = self.client.get(
            self.subjects_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

    def test_get_lessons(self) -> None:
        """
        Should return subject lessons.
        """

        response = self.client.get(
            self.lessons_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            2,
        )

    def test_get_lesson_detail(self) -> None:
        """
        Should return lesson detail.
        """

        response = self.client.get(
            self.lesson_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["title"],
            self.lesson1.title,
        )

    def test_get_next_lesson(self) -> None:
        """
        Should return the next lesson.
        """

        response = self.client.get(
            self.next_lesson_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["id"],
            self.lesson2.id,
        )

    def test_requires_authentication(self) -> None:
        """
        Anonymous users should not access education endpoints.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.subjects_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )