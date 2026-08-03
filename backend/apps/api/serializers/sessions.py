"""
Serializers for session-related API endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.sessions.models import QuizSession


class QuizSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz sessions.
    """

    class Meta:
        model = QuizSession
        fields = (
            "id",
            "lesson",
            "score",
            "correct_answers",
            "wrong_answers",
            "status",
            "started_at",
            "finished_at",
        )
        read_only_fields = (
            "id",
            "score",
            "correct_answers",
            "wrong_answers",
            "status",
            "started_at",
            "finished_at",
        )


class StartSessionSerializer(serializers.Serializer):
    """
    Serializer for starting a quiz session.
    """

    lesson_id = serializers.IntegerField(
        min_value=1,
    )


class SessionResultSerializer(serializers.ModelSerializer):
    """
    Serializer for completed quiz sessions.
    """

    class Meta:
        model = QuizSession
        fields = (
            "score",
            "correct_answers",
            "wrong_answers",
            "status",
            "started_at",
            "finished_at",
        )