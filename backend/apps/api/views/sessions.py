"""
API views for quiz session endpoints.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.api.permissions import IsActiveUser
from apps.api.responses import ApiResponse
from apps.api.serializers.sessions import (
    QuizSessionSerializer,
    UserAnswerSerializer,
)
from apps.education.services import LessonService
from apps.quizzes.services import (
    ChoiceService,
    QuestionService,
)
from apps.sessions.services import SessionService


class StartSessionAPIView(APIView):
    """
    Start a new quiz session.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def post(
        self,
        request,
        lesson_id: int,
    ):
        lesson = LessonService.get_lesson(
            lesson_id=lesson_id,
        )

        session = SessionService.start_session(
            user=request.user,
            lesson=lesson,
        )

        serializer = QuizSessionSerializer(
            session,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Quiz session started.",
            status_code=status.HTTP_201_CREATED,
        )


class SubmitAnswerAPIView(APIView):
    """
    Submit an answer for a question.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def post(
        self,
        request,
        session_id: int,
        question_id: int,
    ):
        session = request.user.quiz_sessions.get(
            pk=session_id,
        )

        question = QuestionService.get_question(
            question_id=question_id,
        )

        choice = ChoiceService.get_choices(
            question=question,
        ).get(
            pk=request.data["choice_id"],
        )

        answer = SessionService.submit_answer(
            session=session,
            question=question,
            selected_choice=choice,
        )

        serializer = UserAnswerSerializer(
            answer,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Answer submitted.",
        )


class NextQuestionAPIView(APIView):
    """
    Return the next question.
    """

    permission_classes = (
        IsAuthenticated,
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

        next_question = SessionService.get_next_question(
            current_question=question,
        )

        if next_question is None:
            return ApiResponse.success(
                data=None,
                message="Quiz completed.",
            )

        return ApiResponse.success(
            data={
                "question_id": next_question.id,
            },
        )


class FinishSessionAPIView(APIView):
    """
    Finish a quiz session.
    """

    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def post(
        self,
        request,
        session_id: int,
    ):
        session = request.user.quiz_sessions.get(
            pk=session_id,
        )

        session = SessionService.finish_session(
            session=session,
        )

        serializer = QuizSessionSerializer(
            session,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Quiz session finished.",
        )