"""
URL configuration for API endpoints.
"""

from __future__ import annotations

from django.urls import path

from apps.api.views import (
    AchievementDetailAPIView,
    AchievementListAPIView,
    CheckLevelAchievementsAPIView,
    FinishSessionAPIView,
    LeaderboardAPIView,
    LessonDetailAPIView,
    LessonListAPIView,
    NextLessonAPIView,
    NextQuestionAPIView,
    QuestionChoicesAPIView,
    QuestionDetailAPIView,
    QuestionListAPIView,
    StartSessionAPIView,
    SubjectListAPIView,
    SubmitAnswerAPIView,
    UnlockAchievementAPIView,
    UserAchievementListAPIView,
    UserProfileAPIView,
    UserUpdateAPIView,
)

app_name = "api"

urlpatterns = [
    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    path(
        "users/me/",
        UserProfileAPIView.as_view(),
        name="user-profile",
    ),
    path(
        "users/me/update/",
        UserUpdateAPIView.as_view(),
        name="user-update",
    ),
    path(
        "leaderboard/",
        LeaderboardAPIView.as_view(),
        name="leaderboard",
    ),

    # ------------------------------------------------------------------
    # Education
    # ------------------------------------------------------------------
    path(
        "subjects/",
        SubjectListAPIView.as_view(),
        name="subject-list",
    ),
    path(
        "subjects/<int:subject_id>/lessons/",
        LessonListAPIView.as_view(),
        name="lesson-list",
    ),
    path(
        "lessons/<int:lesson_id>/",
        LessonDetailAPIView.as_view(),
        name="lesson-detail",
    ),
    path(
        "lessons/<int:lesson_id>/next/",
        NextLessonAPIView.as_view(),
        name="next-lesson",
    ),

    # ------------------------------------------------------------------
    # Quizzes
    # ------------------------------------------------------------------
    path(
        "lessons/<int:lesson_id>/questions/",
        QuestionListAPIView.as_view(),
        name="question-list",
    ),
    path(
        "questions/<int:question_id>/",
        QuestionDetailAPIView.as_view(),
        name="question-detail",
    ),
    path(
        "questions/<int:question_id>/choices/",
        QuestionChoicesAPIView.as_view(),
        name="question-choices",
    ),
    path(
        "questions/<int:question_id>/next/",
        NextQuestionAPIView.as_view(),
        name="next-question",
    ),

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------
    path(
        "lessons/<int:lesson_id>/start/",
        StartSessionAPIView.as_view(),
        name="start-session",
    ),
    path(
        "sessions/<int:session_id>/questions/<int:question_id>/answer/",
        SubmitAnswerAPIView.as_view(),
        name="submit-answer",
    ),
    path(
        "sessions/<int:session_id>/finish/",
        FinishSessionAPIView.as_view(),
        name="finish-session",
    ),

    # ------------------------------------------------------------------
    # Achievements
    # ------------------------------------------------------------------
    path(
        "achievements/",
        AchievementListAPIView.as_view(),
        name="achievement-list",
    ),
    path(
        "achievements/<int:achievement_id>/",
        AchievementDetailAPIView.as_view(),
        name="achievement-detail",
    ),
    path(
        "users/me/achievements/",
        UserAchievementListAPIView.as_view(),
        name="user-achievements",
    ),
    path(
        "achievements/<int:achievement_id>/unlock/",
        UnlockAchievementAPIView.as_view(),
        name="unlock-achievement",
    ),
    path(
        "achievements/check/",
        CheckLevelAchievementsAPIView.as_view(),
        name="check-achievements",
    ),
]