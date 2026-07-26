"""
Choices used only inside the users application.
"""

from __future__ import annotations

from django.db import models

class UserRole(models.TextChoices):
    """
    Available user roles.
    """
    STUDENT='student',"Student"
    ADMIN="admin","Admin"