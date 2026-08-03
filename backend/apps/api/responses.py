"""
Reusable API response helpers.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    """
    Helper class for standardized API responses.
    """

    @staticmethod
    def success(
        data=None,
        message: str = "Success.",
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """
        Return a successful API response.
        """
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def error(
        message: str = "Request failed.",
        errors=None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        """
        Return an error API response.
        """
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors,
            },
            status=status_code,
        )