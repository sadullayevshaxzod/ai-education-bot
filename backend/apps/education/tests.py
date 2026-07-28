"""
Tests for the education application.
"""

from __future__ import annotations

from django.test import TestCase

from .models import Lesson, Subject
from .services import LessonService, SubjectService


class SubjectServiceTests(TestCase):
    """
    Tests for SubjectService.
    """

    def setUp(self) -> None:
        self.math = Subject.objects.create(
            name="Mathematics",
            slug="mathematics",
            order=1,
            is_active=True,
        )

        self.english = Subject.objects.create(
            name="English",
            slug="english",
            order=2,
            is_active=False,
        )

    def test_get_active_subjects(self) -> None:
        """
        Should return only active subjects.
        """
        subjects = SubjectService.get_active_subjects()

        self.assertEqual(subjects.count(), 1)
        self.assertEqual(subjects.first(), self.math)

    def test_get_subject(self) -> None:
        """
        Should return subject by id.
        """
        subject = SubjectService.get_subject(self.math.id)

        self.assertEqual(subject, self.math)


class LessonServiceTests(TestCase):
    """
    Tests for LessonService.
    """

    def setUp(self) -> None:
        self.subject = Subject.objects.create(
            name="Mathematics",
            slug="mathematics",
            order=1,
        )

        self.lesson1 = Lesson.objects.create(
            subject=self.subject,
            title="Addition",
            order=1,
            xp_reward=10,
        )

        self.lesson2 = Lesson.objects.create(
            subject=self.subject,
            title="Subtraction",
            order=2,
            xp_reward=10,
        )

        self.lesson3 = Lesson.objects.create(
            subject=self.subject,
            title="Multiplication",
            order=3,
            xp_reward=20,
            is_active=False,
        )

    def test_get_lessons(self) -> None:
        """
        Should return only active lessons.
        """
        lessons = LessonService.get_lessons(self.subject)

        self.assertEqual(lessons.count(), 2)

    def test_get_lesson(self) -> None:
        """
        Should return lesson by id.
        """
        lesson = LessonService.get_lesson(self.lesson1.id)

        self.assertEqual(lesson, self.lesson1)

    def test_get_first_lesson(self) -> None:
        """
        Should return first lesson.
        """
        lesson = LessonService.get_first_lesson(self.subject)

        self.assertEqual(lesson, self.lesson1)

    def test_get_next_lesson(self) -> None:
        """
        Should return next active lesson.
        """
        lesson = LessonService.get_next_lesson(self.lesson1)

        self.assertEqual(lesson, self.lesson2)

    def test_get_next_lesson_returns_none(self) -> None:
        """
        Should return None if there is no next active lesson.
        """
        lesson = LessonService.get_next_lesson(self.lesson2)

        self.assertIsNone(lesson)