"""
Admin configuration for the users application.
"""

from __future__ import annotations

from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.
    """

    list_display = (
        "id",
        "telegram_id",
        "username",
        "first_name",
        "role",
        "language",
        "level",
        "xp",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "language",
        "is_active",
    )

    search_fields = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_activity",
    )

    list_editable = (
    "is_active",
    )

    list_per_page = 25
