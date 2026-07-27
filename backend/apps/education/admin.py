"""
Admin configuration for the education application.
"""

from __future__ import annotations

from django.contrib import admin

from .models import Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subject model.
    """

    list_display = (
        "id",
        "name",
        "order",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_per_page = 25


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Lesson model.
    """

    list_display = (
        "id",
        "title",
        "subject",
        "order",
        "xp_reward",
        "is_active",
        "created_at",
    )

    list_filter = (
        "subject",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "subject__name",
    )

    ordering = (
        "subject",
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_select_related = (
        "subject",
    )

    list_per_page = 25