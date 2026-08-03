"""
Custom permissions for the API.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission

from apps.users.choices import UserRole


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view) -> bool:
        user = request.user

        return (
            user.is_authenticated
            and user.role == UserRole.ADMIN
        )


class IsStudentUser(BasePermission):
    """
    Allows access only to student users.
    """

    message = "Only students can perform this action."

    def has_permission(self, request, view) -> bool:
        user = request.user

        return (
            user.is_authenticated
            and user.role == UserRole.STUDENT
        )


class IsActiveUser(BasePermission):
    """
    Allows access only to active users.
    """

    message = "Your account is inactive."

    def has_permission(self, request, view) -> bool:
        user = request.user

        return (
            user.is_authenticated
            and user.is_active
        )