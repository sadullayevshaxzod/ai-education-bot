"""
Database models for the sessions application.
"""

from __future__ import annotations

from django.db import models

from apps.common.choices import SessionStatus
from apps.common.models import BaseModel
from apps.education.models import Lesson
from apps.quizzes.models import Choice, Question
from apps.users.models import User


class QuizSession(BaseModel):
    """
    Represents a user's quiz attempt for a lesson.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_sessions",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="quiz_sessions",
    )

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.STARTED,
    )

    score = models.PositiveIntegerField(
        default=0,
    )

    correct_answers = models.PositiveIntegerField(
        default=0,
    )

    wrong_answers = models.PositiveIntegerField(
        default=0,
    )

    xp_earned = models.PositiveIntegerField(
        default=0,
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "quiz_sessions"
        verbose_name = "Quiz Session"
        verbose_name_plural = "Quiz Sessions"
        ordering = ("-started_at",)

    def __str__(self) -> str:
        return f"{self.user} - {self.lesson}"


class UserAnswer(BaseModel):
    """
    Stores a user's answer for a question.
    """

    session = models.ForeignKey(
        QuizSession,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name="user_answers",
    )

    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.PROTECT,
        related_name="user_answers",
    )

    is_correct = models.BooleanField()

    answered_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "user_answers"
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"
        ordering = ("answered_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["session", "question"],
                name="unique_question_per_session",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.session} - {self.question}"