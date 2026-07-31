"""
Business logic for the sessions application.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.quizzes.models import Choice, Question
from apps.quizzes.services import QuestionService

from .models import QuizSession, UserAnswer


class SessionService:
    """
    Business logic for quiz sessions.
    """

    @staticmethod
    @transaction.atomic
    def start_session(user, lesson) -> QuizSession:
        """
        Create a new quiz session.
        """
        return QuizSession.objects.create(
            user=user,
            lesson=lesson,
        )

    @staticmethod
    @transaction.atomic
    def submit_answer(
        session: QuizSession,
        question: Question,
        selected_choice: Choice,
    ) -> UserAnswer:
        """
        Save user's answer.
        """
        is_correct = selected_choice.is_correct

        answer = UserAnswer.objects.create(
            session=session,
            question=question,
            selected_choice=selected_choice,
            is_correct=is_correct,
        )

        if is_correct:
            session.correct_answers += 1
            session.score += question.points
        else:
            session.wrong_answers += 1

        session.save(
            update_fields=[
                "score",
                "correct_answers",
                "wrong_answers",
                "updated_at",
            ]
        )

        return answer

    @staticmethod
    def get_next_question(
        current_question: Question,
    ) -> Question | None:
        """
        Return the next question.
        """
        return QuestionService.get_next_question(
            current_question,
        )

    @staticmethod
    @transaction.atomic
    def finish_session(
        session: QuizSession,
    ) -> QuizSession:
        """
        Finish quiz session.
        """
        session.status = "finished"
        session.finished_at = timezone.now()

        session.save(
            update_fields=[
                "status",
                "finished_at",
                "updated_at",
            ]
        )

        return session