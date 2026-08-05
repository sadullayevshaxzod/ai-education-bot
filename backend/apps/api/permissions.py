"""
Custom permissions for the API.
"""

from __future__ import annotations

from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission

from apps.users.choices import UserRole


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)

        return (
            user is not None
            and user.is_active
            and user.role == UserRole.ADMIN
        )


class IsStudentUser(BasePermission):
    """
    Allows access only to student users.
    """

    message = "Only students can perform this action."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)

        return (
            user is not None
            and user.is_active
            and user.role == UserRole.STUDENT
        )


class IsActiveUser(BasePermission):
    """
    Allows access only to active users.
    """

    message = "Your account is inactive."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)

        if user is None or not getattr(user, "is_authenticated", False):
            raise NotAuthenticated()

        if not user.is_active:
            raise PermissionDenied(detail=self.message)

        return True