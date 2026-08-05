"""
Tests for quiz API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import (
    Difficulty,
    Language,
    QuestionType,
)
from apps.education.models import Lesson, Subject
from apps.quizzes.models import Choice, Question
from apps.users.choices import UserRole
from apps.users.models import User


class QuizAPITests(APITestCase):
    """
    Tests for quiz API endpoints.
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
            order=1,
        )

        self.lesson = Lesson.objects.create(
            subject=self.subject,
            title="Variables",
            order=1,
            xp_reward=100,
        )

        self.question1 = Question.objects.create(
            lesson=self.lesson,
            text="What is Python?",
            difficulty=Difficulty.EASY,
            question_type=QuestionType.SINGLE_CHOICE,
            points=10,
            order=1,
        )

        self.question2 = Question.objects.create(
            lesson=self.lesson,
            text="What is Django?",
            difficulty=Difficulty.EASY,
            question_type=QuestionType.SINGLE_CHOICE,
            points=20,
            order=2,
        )

        self.choice1 = Choice.objects.create(
            question=self.question1,
            text="Programming Language",
            is_correct=True,
            order=1,
        )

        self.choice2 = Choice.objects.create(
            question=self.question1,
            text="Database",
            is_correct=False,
            order=2,
        )

        self.questions_url = reverse(
            "api:question-list",
            kwargs={
                "lesson_id": self.lesson.id,
            },
        )

        self.question_detail_url = reverse(
            "api:question-detail",
            kwargs={
                "question_id": self.question1.id,
            },
        )

        self.choices_url = reverse(
            "api:question-choices",
            kwargs={
                "question_id": self.question1.id,
            },
        )

        self.next_question_url = reverse(
            "api:next-question",
            kwargs={
                "question_id": self.question1.id,
            },
        )

    def test_get_questions(self) -> None:
        """
        Should return lesson questions.
        """

        response = self.client.get(
            self.questions_url,
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

    def test_get_question_detail(self) -> None:
        """
        Should return question detail.
        """

        response = self.client.get(
            self.question_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["text"],
            self.question1.text,
        )

    def test_get_question_choices(self) -> None:
        """
        Should return question choices.
        """

        response = self.client.get(
            self.choices_url,
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

    def test_get_next_question(self) -> None:
        """
        Should return next question.
        """

        response = self.client.get(
            self.next_question_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["question_id"],
            self.question2.id,
        )

    def test_requires_authentication(self) -> None:
        """
        Anonymous users should not access quiz endpoints.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.questions_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )