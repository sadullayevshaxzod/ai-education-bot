"""
Custom throttling classes for the API.
"""

from __future__ import annotations

from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """
    Throttle for short bursts of requests.
    """

    scope = "burst"


class SustainedRateThrottle(UserRateThrottle):
    """
    Throttle for sustained API usage.
    """

    scope = "sustained"