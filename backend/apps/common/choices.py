"""
Reusable choices used across the project.
"""

from __future__ import annotations

from django.db import models


class Difficulty(models.TextChoices):
    """
    Difficulty level for quizzes and questions.
    """

    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"


class UserRole(models.TextChoices):
    """
    Available user roles.
    """

    STUDENT = "student", "Student"
    ADMIN = "admin", "Admin"


class Language(models.TextChoices):
    """
    Supported application languages.
    """

    UZ = "uz", "Uzbek"
    EN = "en", "English"
    RU = "ru", "Russian"


class ProgressStatus(models.TextChoices):
    """
    Lesson progress status.
    """

    NOT_STARTED = "not_started", "Not Started"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class SessionStatus(models.TextChoices):
    """
    Quiz session status.
    """

    STARTED = "started", "Started"
    FINISHED = "finished", "Finished"
    CANCELLED = "cancelled", "Cancelled"


class QuestionType(models.TextChoices):
    """
    Supported question types.
    """

    TEXT = "text", "Text"
    SINGLE_CHOICE = "single_choice", "Single Choice"
    TRUE_FALSE = "true_false", "True / False"