"""
Serializers for education-related API endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.education.models import (
    Lesson,
    Subject,
)


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for subjects.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "order",
        )
        read_only_fields = (
            "id",
        )


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for lesson list.
    """

    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "subject",
            "title",
            "description",
            "order",
            "xp_reward",
        )
        read_only_fields = (
            "id",
        )


class LessonDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for lesson details.
    """

    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "subject",
            "title",
            "description",
            "order",
            "xp_reward",
        )
        read_only_fields = (
            "id",
        )