"""
Business logic for the quizzes application.
"""

from __future__ import annotations

from django.db.models import QuerySet

from .models import Choice, Question


class QuestionService:
    """
    Business logic for quiz questions.
    """

    @staticmethod
    def get_questions_by_lesson(lesson_id: int) -> QuerySet[Question]:
        """
        Return all active questions for a lesson.
        """
        return Question.objects.filter(
            lesson_id=lesson_id,
            is_active=True,
        ).order_by("order")

    @staticmethod
    def get_question(question_id: int) -> Question:
        """
        Return a question by ID.
        """
        return Question.objects.select_related(
            "lesson",
            "lesson__subject",
        ).get(
            pk=question_id,
            is_active=True,
        )

    @staticmethod
    def get_first_question(lesson_id: int) -> Question | None:
        """
        Return the first active question of a lesson.
        """
        return (
            Question.objects.filter(
                lesson_id=lesson_id,
                is_active=True,
            )
            .order_by("order")
            .first()
        )

    @staticmethod
    def get_next_question(question: Question) -> Question | None:
        """
        Return the next active question.
        """
        return (
            Question.objects.filter(
                lesson=question.lesson,
                order__gt=question.order,
                is_active=True,
            )
            .order_by("order")
            .first()
        )


class ChoiceService:
    """
    Business logic for answer choices.
    """

    @staticmethod
    def get_choices(question: Question) -> QuerySet[Choice]:
        """
        Return ordered answer choices.
        """
        return question.choices.order_by("order")

    @staticmethod
    def get_correct_choice(question: Question) -> Choice:
        """
        Return the correct answer choice.
        """
        return question.choices.get(
            is_correct=True,
        )