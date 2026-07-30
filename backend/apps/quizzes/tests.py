"""
Tests for the quizzes application.
"""

from __future__ import annotations

from django.test import TestCase

from apps.common.choices import Difficulty, QuestionType
from apps.education.models import Lesson, Subject

from .models import Choice, Question
from .services import ChoiceService, QuestionService


class QuestionServiceTests(TestCase):
    """
    Tests for QuestionService.
    """

    def setUp(self) -> None:
        self.subject = Subject.objects.create(
            name="Mathematics",
            slug="mathematics",
            order=1,
        )

        self.lesson = Lesson.objects.create(
            subject=self.subject,
            title="Addition",
            order=1,
            xp_reward=10,
        )

        self.question1 = Question.objects.create(
            lesson=self.lesson,
            question_type=QuestionType.SINGLE_CHOICE,
            difficulty=Difficulty.EASY,
            text="2 + 2 = ?",
            points=10,
            order=1,
        )

        self.question2 = Question.objects.create(
            lesson=self.lesson,
            question_type=QuestionType.SINGLE_CHOICE,
            difficulty=Difficulty.MEDIUM,
            text="5 + 7 = ?",
            points=20,
            order=2,
        )

        self.question3 = Question.objects.create(
            lesson=self.lesson,
            question_type=QuestionType.SINGLE_CHOICE,
            difficulty=Difficulty.HARD,
            text="12 + 18 = ?",
            points=30,
            order=3,
            is_active=False,
        )

    def test_get_questions_by_lesson(self) -> None:
        """
        Should return only active questions.
        """
        questions = QuestionService.get_questions_by_lesson(
            self.lesson.id,
        )

        self.assertEqual(questions.count(), 2)

    def test_get_question(self) -> None:
        """
        Should return question by id.
        """
        question = QuestionService.get_question(
            self.question1.id,
        )

        self.assertEqual(question, self.question1)

    def test_get_first_question(self) -> None:
        """
        Should return first active question.
        """
        question = QuestionService.get_first_question(
            self.lesson.id,
        )

        self.assertEqual(question, self.question1)

    def test_get_next_question(self) -> None:
        """
        Should return next active question.
        """
        question = QuestionService.get_next_question(
            self.question1,
        )

        self.assertEqual(question, self.question2)

    def test_get_next_question_returns_none(self) -> None:
        """
        Should return None if there is no next active question.
        """
        question = QuestionService.get_next_question(
            self.question2,
        )

        self.assertIsNone(question)


class ChoiceServiceTests(TestCase):
    """
    Tests for ChoiceService.
    """

    def setUp(self) -> None:
        self.subject = Subject.objects.create(
            name="Mathematics",
            slug="mathematics",
            order=1,
        )

        self.lesson = Lesson.objects.create(
            subject=self.subject,
            title="Addition",
            order=1,
            xp_reward=10,
        )

        self.question = Question.objects.create(
            lesson=self.lesson,
            question_type=QuestionType.SINGLE_CHOICE,
            difficulty=Difficulty.EASY,
            text="2 + 2 = ?",
            points=10,
            order=1,
        )

        self.choice1 = Choice.objects.create(
            question=self.question,
            text="3",
            order=1,
            is_correct=False,
        )

        self.choice2 = Choice.objects.create(
            question=self.question,
            text="4",
            order=2,
            is_correct=True,
        )

        self.choice3 = Choice.objects.create(
            question=self.question,
            text="5",
            order=3,
            is_correct=False,
        )

    def test_get_choices(self) -> None:
        """
        Should return ordered choices.
        """
        choices = ChoiceService.get_choices(
            self.question,
        )

        self.assertEqual(choices.count(), 3)
        self.assertEqual(choices.first(), self.choice1)

    def test_get_correct_choice(self) -> None:
        """
        Should return correct choice.
        """
        choice = ChoiceService.get_correct_choice(
            self.question,
        )

        self.assertEqual(choice, self.choice2)