"""
Admin configuration for the achievements application.
"""

from __future__ import annotations

from django.contrib import admin

from .models import (
    Achievement,
    UserAchievement,
)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Admin configuration for Achievement model.
    """

    list_display = (
        "id",
        "name",
        "required_level",
        "xp_reward",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "required_level",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "required_level",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserAchievement model.
    """

    list_display = (
        "id",
        "user",
        "achievement",
        "earned_at",
    )

    list_filter = (
        "achievement",
        "earned_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "achievement__name",
    )

    ordering = (
        "-earned_at",
    )

    readonly_fields = (
        "earned_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_select_related = (
    "user",
    "achievement",
)