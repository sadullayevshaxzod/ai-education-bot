"""
Tests for the sessions application.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.choices import (
    Difficulty,
    QuestionType,
    SessionStatus,
    UserRole,
)
from apps.education.models import Lesson, Subject
from apps.quizzes.models import Choice, Question
from apps.sessions.models import QuizSession
from apps.sessions.services import SessionService
from apps.users.models import User


class SessionServiceTests(TestCase):
    """
    Tests for SessionService.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            telegram_id=123456789,
            first_name="Test User",
            username="test_user",
            role=UserRole.STUDENT,
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

    def test_start_session(self) -> None:
        """
        Should create a new quiz session.
        """
        session = SessionService.start_session(
            user=self.user,
            lesson=self.lesson,
        )

        self.assertEqual(session.user, self.user)
        self.assertEqual(session.lesson, self.lesson)
        self.assertEqual(session.status, SessionStatus.STARTED)

    def test_submit_correct_answer(self) -> None:
        """
        Should save correct answer and update score.
        """
        session = SessionService.start_session(
            self.user,
            self.lesson,
        )

        SessionService.submit_answer(
            session=session,
            question=self.question1,
            selected_choice=self.choice1,
        )

        session.refresh_from_db()

        self.assertEqual(session.score, 10)
        self.assertEqual(session.correct_answers, 1)
        self.assertEqual(session.wrong_answers, 0)

    def test_submit_wrong_answer(self) -> None:
        """
        Should save wrong answer.
        """
        session = SessionService.start_session(
            self.user,
            self.lesson,
        )

        SessionService.submit_answer(
            session=session,
            question=self.question1,
            selected_choice=self.choice2,
        )

        session.refresh_from_db()

        self.assertEqual(session.score, 0)
        self.assertEqual(session.correct_answers, 0)
        self.assertEqual(session.wrong_answers, 1)

    def test_get_next_question(self) -> None:
        """
        Should return the next question.
        """
        question = SessionService.get_next_question(
            self.question1,
        )

        self.assertEqual(question, self.question2)

    def test_finish_session(self) -> None:
        """
        Should finish the session.
        """
        session = SessionService.start_session(
            self.user,
            self.lesson,
        )

        SessionService.finish_session(session)

        session.refresh_from_db()

        self.assertEqual(
            session.status,
            SessionStatus.FINISHED,
        )

        self.assertIsNotNone(
            session.finished_at,
        )