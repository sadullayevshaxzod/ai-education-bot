"""
Custom exceptions for the API application.
"""

from __future__ import annotations

from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequestException(APIException):
    """
    Exception raised for invalid requests.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request"


class UnauthorizedException(APIException):
    """
    Exception raised when authentication fails.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication credentials were not provided."
    default_code = "unauthorized"


class PermissionDeniedException(APIException):
    """
    Exception raised when the user has no permission.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class NotFoundException(APIException):
    """
    Exception raised when an object is not found.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Requested resource was not found."
    default_code = "not_found"


class ConflictException(APIException):
    """
    Exception raised when a resource already exists.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource already exists."
    default_code = "conflict"