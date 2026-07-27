"""
Database models for the education application.
"""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel
class Subject(BaseModel):
    """
    Learning subject.
    """
    name=models.CharField(
        max_length=100,
        unique=True,
    )

    slug=models.CharField(
        max_length=100,
        unique=True,
    )
    description=models.TextField(
        blank=True,
        default="",
    )
    order=models.PositiveIntegerField(
        default=1,
    )
    is_active=models.BooleanField(
        default=True,
    )
    class Meta:
        db_table="subjects"
        verbose_name="Subject"
        verbose_name_plural="Subjects"
        ordering=("order",)
    def __str__(self):
        return self.name


class Lesson(BaseModel):
    """
    Learning lesson.
    """
    subject=models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="lesson",
    )
    title=models.CharField(
        max_length=120,
    )
    description=models.TextField(
        blank=True,
        default="",
    )
    order=models.PositiveIntegerField(
        default=1,
    )
    xp_reward=models.PositiveIntegerField(
        default=10,
    )
    is_active=models.BooleanField(
        default=True,
    )
    class Meta:
        db_table="lesson"
        verbose_name="Lesson"
        verbose_name_plural="Lessons"
        ordering=(
            "subject",
            "order",
        )
        constraints=[
            models.UniqueConstraint(
                fields=["subject","order"],
                name="unique_lesson_order_per_subject",
            ),
        ]
        def __str__(self) -> str:
            return f"{self.subject.name} - {self.title}"    