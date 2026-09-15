"""Command line interface for the Pregnancy Journey Copilot."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from typing import Iterable, List, Optional, Sequence

from .content import DISCLAIMER, EMERGENCY_SIGNS, LAST_WEEK
from .journey import (
    build_briefing,
    estimate_due_date,
    guidance_for_week,
    newborn_guidance,
    newborn_stage_for_day,
    partner_tips,
    timeline,
    week_from_due_date,
)
from .models import Briefing, Guidance


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid date '{value}', expected format YYYY-MM-DD"
        ) from exc


def _bullets(items: Iterable[str], marker: str = "-") -> List[str]:
    return [f"  {marker} {item}" for item in items]


def _format_guidance(guidance: Guidance) -> List[str]:
    lines = ["Do's:"]
    lines += _bullets(guidance.dos)
    lines += ["", "Don'ts:"]
    lines += _bullets(guidance.donts)
    return lines


def _format_briefing(briefing: Briefing) -> List[str]:
    milestone = briefing.milestone
    lines = [milestone.title, "=" * len(milestone.title), ""]
    if briefing.due_date is not None:
        lines.append(f"Due date: {briefing.due_date.isoformat()} ({briefing.days_until_due} days to go)")
        lines.append("")
    lines.append(f"Baby: {milestone.baby_development}")
    lines.append(f"Mother: {milestone.mother_changes}")
    lines.append(f"Focus this week: {milestone.focus}")
    lines.append("")
    lines += _format_guidance(briefing.guidance)
    lines += ["", "Partner support:"]
    lines += _bullets(briefing.partner_tips)
    if briefing.upcoming_appointments:
        lines += ["", "Upcoming checkpoints:"]
        lines += _bullets(
            f"week {a.week} - {a.name}: {a.description}" for a in briefing.upcoming_appointments
        )
    if briefing.notes:
        lines += ["", "Notes:"]
        lines += _bullets(briefing.notes)
    return lines


def _resolve_week(args: argparse.Namespace) -> int:
    if args.week is not None:
        if not 1 <= args.week <= LAST_WEEK:
            raise SystemExit(f"error: --week must be between 1 and {LAST_WEEK}")
        return args.week
    return week_from_due_date(args.due_date)


def _add_stage_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--week", type=int, help=f"pregnancy week (1-{LAST_WEEK})")
    group.add_argument("--due-date", type=_parse_date, help="estimated due date (YYYY-MM-DD)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pregnancy-copilot",
        description="A companion for pregnancy education, newborn guidance and partner support.",
        epilog=DISCLAIMER,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    week_parser = subparsers.add_parser("week", help="show a personalised briefing for a week")
    _add_stage_arguments(week_parser)

    timeline_parser = subparsers.add_parser("timeline", help="show the stage-based pregnancy timeline")
    timeline_parser.add_argument("--from", dest="start", type=int, default=1, help="first week to show")
    timeline_parser.add_argument("--to", dest="end", type=int, default=LAST_WEEK, help="last week to show")

    guidance_parser = subparsers.add_parser("guidance", help="show do's and don'ts for a week")
    _add_stage_arguments(guidance_parser)

    partner_parser = subparsers.add_parser("partner", help="show partner support tips for a week")
    _add_stage_arguments(partner_parser)

    newborn_parser = subparsers.add_parser("newborn", help="show early newborn care guidance")
    newborn_parser.add_argument("--day", type=int, help="days since birth")
    newborn_parser.add_argument("--birth-date", type=_parse_date, help="date of birth (YYYY-MM-DD)")

    due_parser = subparsers.add_parser("due-date", help="estimate the due date from the last period")
    due_parser.add_argument("--last-period", type=_parse_date, required=True,
                            help="first day of the last menstrual period (YYYY-MM-DD)")

    subparsers.add_parser("emergency", help="list signs that need urgent medical attention")
    return parser


def _run(args: argparse.Namespace) -> List[str]:
    if args.command == "week":
        if args.week is not None:
            briefing = build_briefing(week=_resolve_week(args))
        else:
            briefing = build_briefing(due_date=args.due_date)
        return _format_briefing(briefing)

    if args.command == "timeline":
        if not 1 <= args.start <= LAST_WEEK or not 1 <= args.end <= LAST_WEEK:
            raise SystemExit(f"error: weeks must be between 1 and {LAST_WEEK}")
        if args.start > args.end:
            raise SystemExit("error: --from must not be greater than --to")
        lines = ["Pregnancy timeline", "=================="]
        current_trimester: Optional[int] = None
        for milestone in timeline(args.start, args.end):
            if milestone.trimester != current_trimester:
                current_trimester = milestone.trimester
                lines += ["", f"Trimester {current_trimester}"]
            lines.append(f"  Week {milestone.week:>2}: {milestone.baby_development}")
            lines.append(f"           Focus: {milestone.focus}")
        return lines

    if args.command == "guidance":
        week = _resolve_week(args)
        return [f"Do's and don'ts for week {week}", ""] + _format_guidance(guidance_for_week(week))

    if args.command == "partner":
        week = _resolve_week(args)
        return [f"Partner support for week {week}", ""] + _bullets(partner_tips(week))

    if args.command == "newborn":
        if args.day is not None and args.birth_date is not None:
            raise SystemExit("error: use either --day or --birth-date, not both")
        if args.birth_date is not None:
            day = (date.today() - args.birth_date).days
            if day < 0:
                raise SystemExit("error: --birth-date is in the future")
        elif args.day is not None:
            if args.day < 0:
                raise SystemExit("error: --day must not be negative")
            day = args.day
        else:
            day = 0
        stage = newborn_stage_for_day(day)
        lines = [f"Newborn stage: {stage.name} (day {day})", ""]
        lines.append("What is happening:")
        lines += _bullets(stage.highlights)
        lines += ["", "Care tips:"]
        lines += _bullets(stage.care_tips)
        lines += ["", "Call your provider if you notice:"]
        lines += _bullets(stage.warning_signs, marker="!")
        lines += [""] + _format_guidance(newborn_guidance())
        return lines

    if args.command == "due-date":
        due = estimate_due_date(args.last_period)
        week = week_from_due_date(due)
        return [
            f"Estimated due date: {due.isoformat()}",
            f"Current week today: {week}",
        ]

    # args.command == "emergency"
    return ["Seek urgent care if you notice:"] + _bullets(EMERGENCY_SIGNS, marker="!")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    for line in _run(args):
        print(line)
    print()
    print(DISCLAIMER)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
