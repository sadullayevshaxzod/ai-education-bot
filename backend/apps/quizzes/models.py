"""
Database models for the quizzes application.
"""

from __future__ import annotations

from django.db import models

from apps.common.choices import Difficulty, QuestionType
from apps.common.models import BaseModel
from apps.education.models import Lesson


class Question(BaseModel):
    """
    Quiz question for a lesson.
    """

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="questions",
    )

    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE_CHOICE,
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )

    text = models.TextField()

    explanation = models.TextField(
        blank=True,
        default="",
    )

    points = models.PositiveIntegerField(
        default=10,
    )

    order = models.PositiveIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = (
            "lesson",
            "order",
        )
        constraints = [
            models.UniqueConstraint(
                fields=["lesson", "order"],
                name="unique_question_order_per_lesson",
            ),
        ]

    def __str__(self) -> str:
        return self.text[:60]


class Choice(BaseModel):
    """
    Answer choice for a question.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )

    text = models.CharField(
        max_length=255,
    )

    is_correct = models.BooleanField(
        default=False,
    )

    order = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        db_table = "choices"
        verbose_name = "Choice"
        verbose_name_plural = "Choices"
        ordering = (
            "question",
            "order",
        )
        constraints = [
            models.UniqueConstraint(
                fields=["question", "order"],
                name="unique_choice_order_per_question",
            ),
        ]

    def __str__(self) -> str:
        return self.text