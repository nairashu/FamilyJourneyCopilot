"""Data model for the Pregnancy Journey Copilot."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Tuple


@dataclass(frozen=True)
class WeekMilestone:
    """What happens during a single week of pregnancy."""

    week: int
    trimester: int
    baby_development: str
    mother_changes: str
    focus: str

    @property
    def title(self) -> str:
        return f"Week {self.week} (trimester {self.trimester})"


@dataclass(frozen=True)
class Guidance:
    """Practical do's and don'ts for a stage of the journey."""

    dos: Tuple[str, ...] = ()
    donts: Tuple[str, ...] = ()

    def merged_with(self, other: "Guidance") -> "Guidance":
        """Combine two guidance sets, preserving order and dropping duplicates."""

        def _unique(*groups: Tuple[str, ...]) -> Tuple[str, ...]:
            seen: list = []
            for group in groups:
                for item in group:
                    if item not in seen:
                        seen.append(item)
            return tuple(seen)

        return Guidance(
            dos=_unique(self.dos, other.dos),
            donts=_unique(self.donts, other.donts),
        )


@dataclass(frozen=True)
class NewbornStage:
    """A stage of early newborn care, measured in days since birth."""

    name: str
    start_day: int
    end_day: int
    highlights: Tuple[str, ...]
    care_tips: Tuple[str, ...]
    warning_signs: Tuple[str, ...]

    def covers(self, day: int) -> bool:
        return self.start_day <= day <= self.end_day


@dataclass(frozen=True)
class Appointment:
    """A typical care checkpoint during pregnancy."""

    week: int
    name: str
    description: str


@dataclass(frozen=True)
class Briefing:
    """A personalised snapshot of where a family is in the journey."""

    week: int
    trimester: int
    milestone: WeekMilestone
    guidance: Guidance
    partner_tips: Tuple[str, ...]
    upcoming_appointments: Tuple[Appointment, ...] = ()
    due_date: Optional[date] = None
    days_until_due: Optional[int] = None
    notes: Tuple[str, ...] = field(default_factory=tuple)
