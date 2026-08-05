"""
Tests for session API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.choices import (
    Difficulty,
    Language,
    QuestionType,
    SessionStatus,
)
from apps.education.models import Lesson, Subject
from apps.quizzes.models import Choice, Question
from apps.sessions.models import QuizSession
from apps.users.choices import UserRole
from apps.users.models import User


class SessionAPITests(APITestCase):
    """
    Tests for session API endpoints.
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

        self.question = Question.objects.create(
            lesson=self.lesson,
            text="What is Python?",
            difficulty=Difficulty.EASY,
            question_type=QuestionType.SINGLE_CHOICE,
            points=10,
            order=1,
        )

        self.choice_correct = Choice.objects.create(
            question=self.question,
            text="Programming language",
            is_correct=True,
            order=1,
        )

        self.choice_wrong = Choice.objects.create(
            question=self.question,
            text="Database",
            is_correct=False,
            order=2,
        )

        self.start_url = reverse(
            "api:start-session",
            kwargs={
                "lesson_id": self.lesson.id,
            },
        )

    def test_start_session(self) -> None:
        """
        Should create a new quiz session.
        """

        response = self.client.post(
            self.start_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["message"],
            "Quiz session started.",
        )

        self.assertEqual(
            QuizSession.objects.count(),
            1,
        )

    def test_submit_correct_answer(self) -> None:
        """
        Should submit a correct answer.
        """

        session = QuizSession.objects.create(
            user=self.user,
            lesson=self.lesson,
        )

        url = reverse(
            "api:submit-answer",
            kwargs={
                "session_id": session.id,
                "question_id": self.question.id,
            },
        )

        response = self.client.post(
            url,
            {
                "choice_id": self.choice_correct.id,
            },
            format="json",
        )

        session.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            session.score,
            10,
        )

        self.assertEqual(
            session.correct_answers,
            1,
        )

    def test_submit_wrong_answer(self) -> None:
        """
        Should submit a wrong answer.
        """

        session = QuizSession.objects.create(
            user=self.user,
            lesson=self.lesson,
        )

        url = reverse(
            "api:submit-answer",
            kwargs={
                "session_id": session.id,
                "question_id": self.question.id,
            },
        )

        response = self.client.post(
            url,
            {
                "choice_id": self.choice_wrong.id,
            },
            format="json",
        )

        session.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            session.score,
            0,
        )

        self.assertEqual(
            session.wrong_answers,
            1,
        )

    def test_finish_session(self) -> None:
        """
        Should finish a session.
        """

        session = QuizSession.objects.create(
            user=self.user,
            lesson=self.lesson,
        )

        url = reverse(
            "api:finish-session",
            kwargs={
                "session_id": session.id,
            },
        )

        response = self.client.post(
            url,
        )

        session.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            session.status,
            SessionStatus.FINISHED,
        )

        self.assertIsNotNone(
            session.finished_at,
        )

    def test_requires_authentication(self) -> None:
        """
        Anonymous users should not access session endpoints.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.post(
            self.start_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )