"""
Business logic for the education application.
"""

from __future__ import annotations

from django.db import transaction

from .models import Lesson, Subject


class SubjectService:
    """
    Business logic for subjects.
    """
    @staticmethod
    def get_active_subjects():
        """
        Return all active subjects.
        """
        return Subject.objects.filter(
            is_active=True,
        ).order_by("order")
    @staticmethod
    def get_subject(subject_id: int) ->Subject:
        """
        Return a subject by ID.
        """
        return Subject.objects.get(
            pk=subject_id,
            is_active=True,
        )

class LessonService:
    """
    Business logic for lessons.
    """
    @staticmethod
    def get_lessons(subject:Subject):
        """
        Return all active lessons of a subject.
        """
        return Lesson.objects.filter(
            subject=subject,
            is_active=True,
        ).order_by("order")
    @staticmethod
    def get_lesson(lesson_id: int) ->Lesson:
        """
        Return lesson by ID
        """
        return Lesson.objects.get(
            pk=lesson_id,
            is_active=True,
        )
    @staticmethod
    def get_first_lesson(subject: Subject) ->Lesson | None:
        """
        Return the first lesson of a subject.
        """
        return (
            Lesson.objects.filter(
            subject=subject,
            is_active=True,
        )
        .order_by("order")
        .first()
        )
    @staticmethod
    def get_next_lesson(lesson: Lesson) ->Lesson | None :
        """
        Return the next lesson
        """
        return (
            Lesson.objects.filter(
                subject=lesson.subject,
                order__gt=lesson.order,
                is_active=True,
            )
            .order_by("order")
            .first()
        )
        
    
        