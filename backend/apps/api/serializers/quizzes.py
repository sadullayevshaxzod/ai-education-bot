"""
Serializers for quiz-related API endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.quizzes.models import (
    Choice,
    Question,
)


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for question choices.
    """

    class Meta:
        model = Choice
        fields = (
            "id",
            "text",
            "order",
        )
        read_only_fields = (
            "id",
        )


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz questions.
    """

    choices = ChoiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = (
            "id",
            "text",
            "difficulty",
            "question_type",
            "points",
            "order",
            "choices",
        )
        read_only_fields = (
            "id",
        )


class AnswerSerializer(serializers.Serializer):
    """
    Serializer for submitting an answer.
    """

    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()