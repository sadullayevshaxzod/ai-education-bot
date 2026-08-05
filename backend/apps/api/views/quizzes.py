"""
API views for quiz endpoints.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.api.permissions import IsActiveUser
from apps.api.responses import ApiResponse
from apps.api.serializers.quizzes import (
    ChoiceSerializer,
    QuestionSerializer,
)
from apps.quizzes.services import (
    ChoiceService,
    QuestionService,
)


class QuestionListAPIView(APIView):
    """
    Return all questions for a lesson.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(
        self,
        request,
        lesson_id: int,
    ):
        questions = QuestionService.get_questions_by_lesson(
            lesson_id=lesson_id,
        )

        serializer = QuestionSerializer(
            questions,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class QuestionDetailAPIView(APIView):
    """
    Return question details.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(
        self,
        request,
        question_id: int,
    ):
        question = QuestionService.get_question(
            question_id=question_id,
        )

        serializer = QuestionSerializer(
            question,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class QuestionChoicesAPIView(APIView):
    """
    Return answer choices for a question.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(
        self,
        request,
        question_id: int,
    ):
        question = QuestionService.get_question(
            question_id=question_id,
        )

        choices = ChoiceService.get_choices(
            question=question,
        )

        serializer = ChoiceSerializer(
            choices,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
        )


class NextQuestionAPIView(APIView):
    """
    Return the next question.
    """

    permission_classes = (
        IsActiveUser,
    )

    def get(
        self,
        request,
        question_id: int,
    ):
        question = QuestionService.get_question(
            question_id=question_id,
        )

        next_question = QuestionService.get_next_question(
            question=question,
        )

        if next_question is None:
            return ApiResponse.success(
                data=None,
                message="No next question available.",
            )

        serializer = QuestionSerializer(
            next_question,
        )

        return ApiResponse.success(
            data=serializer.data,
        )