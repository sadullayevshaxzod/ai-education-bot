"""
Admin configuration for the sessions application.
"""

from __future__ import annotations

from django.contrib import admin

from .models import QuizSession, UserAnswer


class UserAnswerInline(admin.TabularInline):
    """
    Inline admin for user answers.
    """

    model = UserAnswer
    extra = 0
    ordering = ("answered_at",)
    readonly_fields = (
        "question",
        "selected_choice",
        "is_correct",
        "answered_at",
    )

    can_delete = False


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the QuizSession model.
    """

    list_display = (
        "id",
        "user",
        "lesson",
        "status",
        "score",
        "correct_answers",
        "wrong_answers",
        "xp_earned",
        "started_at",
    )

    list_filter = (
        "status",
        "lesson__subject",
        "lesson",
    )

    search_fields = (
        "user__username",
        "lesson__title",
        "lesson__subject__name",
    )

    ordering = (
        "-started_at",
    )

    readonly_fields = (
        "started_at",
        "finished_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_select_related = (
        "user",
        "lesson",
        "lesson__subject",
    )

    list_per_page = 25

    inlines = [
        UserAnswerInline,
    ]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserAnswer model.
    """

    list_display = (
        "id",
        "session",
        "question",
        "selected_choice",
        "is_correct",
        "answered_at",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "question__text",
        "selected_choice__text",
        "session__user__username",
    )

    ordering = (
        "-answered_at",
    )

    readonly_fields = (
        "answered_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_select_related = (
        "session",
        "question",
        "selected_choice",
    )

    list_per_page = 25