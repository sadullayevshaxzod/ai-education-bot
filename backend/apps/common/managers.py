"""
Custom managers used across the project.
"""

from __future__ import annotations

from django.db import models


class ActiveManager(models.Manager):
    """
    Manager that returns only active (not deleted) objects.
    """

    def get_queryset(self):
        """
        Return only objects that are not soft deleted.
        """
        return super().get_queryset().filter(deleted_at__isnull=True)