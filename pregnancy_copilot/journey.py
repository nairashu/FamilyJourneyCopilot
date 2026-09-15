"""Core logic of the Pregnancy Journey Copilot.

Everything here is pure and deterministic so it can be reused by the CLI, a
web service or a chat assistant.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional, Tuple

from .content import (
    APPOINTMENTS,
    DISCLAIMER,
    EMERGENCY_SIGNS,
    FIRST_TRIMESTER_LAST_WEEK,
    GENERAL_GUIDANCE,
    GESTATION_DAYS,
    LAST_WEEK,
    NEWBORN_GUIDANCE,
    NEWBORN_STAGES,
    PARTNER_TIPS,
    SECOND_TRIMESTER_LAST_WEEK,
    TRIMESTER_GUIDANCE,
    WEEK_MILESTONES,
)
from .models import Appointment, Briefing, Guidance, NewbornStage, WeekMilestone

__all__ = [
    "DISCLAIMER",
    "EMERGENCY_SIGNS",
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


def trimester_for_week(week: int) -> int:
    """Return the trimester (1, 2 or 3) that contains ``week``."""

    _validate_week(week)
    if week <= FIRST_TRIMESTER_LAST_WEEK:
        return 1
    if week <= SECOND_TRIMESTER_LAST_WEEK:
        return 2
    return 3


def _validate_week(week: int) -> None:
    if not isinstance(week, int) or isinstance(week, bool):
        raise TypeError("week must be an integer")
    if not 1 <= week <= LAST_WEEK:
        raise ValueError(f"week must be between 1 and {LAST_WEEK}, got {week}")


def estimate_due_date(last_period: date) -> date:
    """Estimate the due date from the first day of the last menstrual period."""

    if not isinstance(last_period, date):
        raise TypeError("last_period must be a datetime.date")
    return last_period + timedelta(days=GESTATION_DAYS)


def gestational_age(due_date: date, today: Optional[date] = None) -> Tuple[int, int]:
    """Return gestational age as ``(completed_weeks, extra_days)``.

    The value can be negative before conception dating starts and can exceed
    40 weeks for a post-term pregnancy; callers decide how to clamp it.
    """

    if not isinstance(due_date, date):
        raise TypeError("due_date must be a datetime.date")
    today = today or date.today()
    elapsed = GESTATION_DAYS - (due_date - today).days
    weeks, days = divmod(elapsed, 7)
    return weeks, days


def week_from_due_date(due_date: date, today: Optional[date] = None) -> int:
    """Return the current pregnancy week (1-40) for a due date.

    Week 1 covers gestational days 0-6, so the current week is the number of
    completed weeks plus one. The result is clamped to the 1-40 range.
    """

    weeks, _ = gestational_age(due_date, today)
    return max(1, min(LAST_WEEK, weeks + 1))


def milestone_for_week(week: int) -> WeekMilestone:
    """Return the milestone information for a pregnancy week."""

    _validate_week(week)
    return WEEK_MILESTONES[week]


def timeline(start_week: int = 1, end_week: int = LAST_WEEK) -> List[WeekMilestone]:
    """Return the ordered milestones between ``start_week`` and ``end_week``."""

    _validate_week(start_week)
    _validate_week(end_week)
    if start_week > end_week:
        raise ValueError("start_week must not be greater than end_week")
    return [WEEK_MILESTONES[week] for week in range(start_week, end_week + 1)]


def guidance_for_week(week: int) -> Guidance:
    """Return general plus trimester-specific do's and don'ts for a week."""

    trimester = trimester_for_week(week)
    return GENERAL_GUIDANCE.merged_with(TRIMESTER_GUIDANCE[trimester])


def partner_tips(week: int) -> Tuple[str, ...]:
    """Return support tips for the partner during the given week."""

    return PARTNER_TIPS[trimester_for_week(week)]


def upcoming_appointments(week: int, limit: int = 3) -> Tuple[Appointment, ...]:
    """Return the next care checkpoints at or after ``week``."""

    _validate_week(week)
    if limit < 0:
        raise ValueError("limit must not be negative")
    return tuple(a for a in APPOINTMENTS if a.week >= week)[:limit]


def newborn_stage_for_day(day: int) -> NewbornStage:
    """Return the newborn stage covering ``day`` days since birth."""

    if not isinstance(day, int) or isinstance(day, bool):
        raise TypeError("day must be an integer")
    if day < 0:
        raise ValueError("day must not be negative")
    for stage in NEWBORN_STAGES:
        if stage.covers(day):
            return stage
    return NEWBORN_STAGES[-1]


def newborn_guidance() -> Guidance:
    """Return the do's and don'ts for early newborn care."""

    return NEWBORN_GUIDANCE


def build_briefing(
    week: Optional[int] = None,
    due_date: Optional[date] = None,
    today: Optional[date] = None,
) -> Briefing:
    """Build a personalised snapshot from either a week or a due date."""

    if (week is None) == (due_date is None):
        raise ValueError("provide exactly one of week or due_date")

    days_until_due: Optional[int] = None
    notes: List[str] = []
    current_week: int = week or 1

    if due_date is not None:
        today = today or date.today()
        days_until_due = (due_date - today).days
        raw_weeks, _ = gestational_age(due_date, today)
        current_week = week_from_due_date(due_date, today)
        if raw_weeks + 1 < 1:
            notes.append("The due date suggests the pregnancy has not started yet; showing week 1.")
        elif raw_weeks + 1 > LAST_WEEK:
            notes.append("You are past the due date; contact your provider about monitoring options.")

    milestone = milestone_for_week(current_week)
    return Briefing(
        week=current_week,
        trimester=milestone.trimester,
        milestone=milestone,
        guidance=guidance_for_week(current_week),
        partner_tips=partner_tips(current_week),
        upcoming_appointments=upcoming_appointments(current_week),
        due_date=due_date,
        days_until_due=days_until_due,
        notes=tuple(notes),
    )
