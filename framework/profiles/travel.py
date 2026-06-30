"""Evaluation profiles for travel planning agents."""

from framework.models import EvaluationProfile
from framework.evaluation.dimensions import (
    CONSTRAINT_SATISFACTION,
    PLANNING_QUALITY,
    INFORMATION_ACCURACY,
    PERSONALIZATION,
    ADAPTABILITY,
)

TRAVEL_PROFILE = EvaluationProfile(
    name="travel-agent",
    weights={
        CONSTRAINT_SATISFACTION: 25.0,
        PLANNING_QUALITY: 20.0,
        INFORMATION_ACCURACY: 20.0,
        PERSONALIZATION: 20.0,
        ADAPTABILITY: 15.0,
    },
    pass_threshold=75.0,
)
