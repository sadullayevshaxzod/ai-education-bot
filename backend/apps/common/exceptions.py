"""
Custom exceptions used across the project.
"""

from __future__ import annotations


class BaseProjectException(Exception):
    """
    Base exception for the entire project.

    All custom project exceptions should inherit from this class.
    """

    default_message = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ValidationException(BaseProjectException):
    """
    Raised when business validation fails.
    """

    default_message = "Validation failed."


class NotFoundException(BaseProjectException):
    """
    Raised when an object cannot be found.
    """

    default_message = "Requested object was not found."


class PermissionDeniedException(BaseProjectException):
    """
    Raised when the user has no permission.
    """

    default_message = "Permission denied."


class ServiceException(BaseProjectException):
    """
    Raised when a service cannot complete an operation.
    """

    default_message = "Service operation failed."