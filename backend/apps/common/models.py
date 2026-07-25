"""
Base models shared across the project.
"""

from __future__ import annotations

from django.db import models

from .managers import ActiveManager


class BaseModel(models.Model):
    """
    Abstract base model.

    Provides:
        - created_at
        - updated_at
    """
    objects=ActiveManager()
    all_objects=models.Manager()
    created_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created_at"
    )
    updated_at=models.DateTimeField(
        auto_now=True,
        verbose_name="Updated_at"
    )

    class Meta:
        abstract=True

    def __str__(self) ->str:
        return f"{self.__class__.__name__} ({self.pk})"