"""Pregnancy Journey Copilot.

An AI-ready companion that turns pregnancy and early newborn care into a
stage-based journey: timelines, educational content, practical do's and
don'ts, and tailored support for mothers, fathers and partners.
"""

from .content import DISCLAIMER, EMERGENCY_SIGNS, LAST_WEEK
from .journey import (
    build_briefing,
    estimate_due_date,
    gestational_age,
    guidance_for_week,
    milestone_for_week,
    newborn_guidance,
    newborn_stage_for_day,
    partner_tips,
    timeline,
    trimester_for_week,
    upcoming_appointments,
    week_from_due_date,
)
from .models import Appointment, Briefing, Guidance, NewbornStage, WeekMilestone

__version__ = "0.1.0"

__all__ = [
    "Appointment",
    "Briefing",
    "DISCLAIMER",
    "EMERGENCY_SIGNS",
    "Guidance",
    "LAST_WEEK",
    "NewbornStage",
    "WeekMilestone",
    "__version__",
    "build_briefing",
    "estimate_due_date",
    "gestational_age",
    "guidance_for_week",
    "milestone_for_week",
    "newborn_guidance",
    "newborn_stage_for_day",
    "partner_tips",
    "timeline",
    "trimester_for_week",
    "upcoming_appointments",
    "week_from_due_date",
]
