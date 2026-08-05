"""
API views for education endpoints.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.api.permissions import IsActiveUser
from apps.api.responses import ApiResponse
from apps.api.serializers.education import (
    LessonDetailSerializer,
    LessonSerializer,
    SubjectSerializer,
)
from apps.education.services import (
    LessonService,
    SubjectService,
)


class SubjectListAPIView(APIView):
    """
    Return all active subjects.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def get(self, request):
        subjects = SubjectService.get_active_subjects()

        serializer = SubjectSerializer(
            subjects,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class LessonListAPIView(APIView):
    """
    Return lessons of a subject.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def get(
        self,
        request,
        subject_id: int,
    ):
        subject = SubjectService.get_subject(
            subject_id=subject_id,
        )

        lessons = LessonService.get_lessons(
            subject=subject,
        )

        serializer = LessonSerializer(
            lessons,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class LessonDetailAPIView(APIView):
    """
    Return lesson details.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def get(
        self,
        request,
        lesson_id: int,
    ):
        lesson = LessonService.get_lesson(
            lesson_id=lesson_id,
        )

        serializer = LessonDetailSerializer(
            lesson,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class NextLessonAPIView(APIView):
    """
    Return the next lesson.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def get(
        self,
        request,
        lesson_id: int,
    ):
        lesson = LessonService.get_lesson(
            lesson_id=lesson_id,
        )

        next_lesson = LessonService.get_next_lesson(
            lesson=lesson,
        )

        if next_lesson is None:
            return ApiResponse.success(
                data=None,
                message="No next lesson available.",
            )

        serializer = LessonSerializer(
            next_lesson,
        )

        return ApiResponse.success(
            data=serializer.data,
        )