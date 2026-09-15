import unittest
from datetime import date, timedelta

from pregnancy_copilot import (
    LAST_WEEK,
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
from pregnancy_copilot.content import NEWBORN_STAGES, WEEK_MILESTONES
from pregnancy_copilot.models import Guidance


class TimelineTests(unittest.TestCase):
    def test_every_week_has_content(self):
        self.assertEqual(sorted(WEEK_MILESTONES), list(range(1, LAST_WEEK + 1)))
        for week, milestone in WEEK_MILESTONES.items():
            self.assertEqual(milestone.week, week)
            self.assertTrue(milestone.baby_development)
            self.assertTrue(milestone.mother_changes)
            self.assertTrue(milestone.focus)

    def test_trimester_boundaries(self):
        self.assertEqual(trimester_for_week(1), 1)
        self.assertEqual(trimester_for_week(13), 1)
        self.assertEqual(trimester_for_week(14), 2)
        self.assertEqual(trimester_for_week(27), 2)
        self.assertEqual(trimester_for_week(28), 3)
        self.assertEqual(trimester_for_week(40), 3)

    def test_timeline_slice_is_ordered(self):
        weeks = [m.week for m in timeline(10, 14)]
        self.assertEqual(weeks, [10, 11, 12, 13, 14])

    def test_full_timeline_default(self):
        self.assertEqual(len(timeline()), LAST_WEEK)

    def test_invalid_weeks_are_rejected(self):
        for bad in (0, -1, LAST_WEEK + 1):
            with self.assertRaises(ValueError):
                milestone_for_week(bad)
        with self.assertRaises(ValueError):
            timeline(10, 5)
        with self.assertRaises(TypeError):
            trimester_for_week("12")


class DatingTests(unittest.TestCase):
    def test_due_date_from_last_period(self):
        self.assertEqual(estimate_due_date(date(2026, 1, 1)), date(2026, 10, 8))

    def test_gestational_age_counts_completed_weeks(self):
        due = date(2026, 10, 8)
        self.assertEqual(gestational_age(due, today=due - timedelta(days=280)), (0, 0))
        self.assertEqual(gestational_age(due, today=due), (40, 0))
        self.assertEqual(gestational_age(due, today=due - timedelta(days=70)), (30, 0))

    def test_week_from_due_date(self):
        due = date(2026, 10, 8)
        self.assertEqual(week_from_due_date(due, today=due - timedelta(days=280)), 1)
        self.assertEqual(week_from_due_date(due, today=due - timedelta(days=274)), 1)
        self.assertEqual(week_from_due_date(due, today=due - timedelta(days=273)), 2)
        self.assertEqual(week_from_due_date(due, today=due - timedelta(days=7)), 40)

    def test_week_is_clamped_outside_the_range(self):
        due = date(2026, 10, 8)
        self.assertEqual(week_from_due_date(due, today=due - timedelta(days=300)), 1)
        self.assertEqual(week_from_due_date(due, today=due + timedelta(days=10)), LAST_WEEK)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            estimate_due_date("2026-01-01")
        with self.assertRaises(TypeError):
            week_from_due_date("2026-01-01")


class GuidanceTests(unittest.TestCase):
    def test_guidance_combines_general_and_trimester_advice(self):
        first = guidance_for_week(6)
        third = guidance_for_week(34)
        self.assertTrue(any("alcohol" in item.lower() for item in first.donts))
        self.assertTrue(any("caffeine" in item.lower() for item in first.donts))
        self.assertTrue(any("movement" in item.lower() for item in third.dos))
        self.assertNotEqual(first.donts, third.donts)

    def test_guidance_has_no_duplicates(self):
        for week in (1, 20, 40):
            guidance = guidance_for_week(week)
            self.assertEqual(len(set(guidance.dos)), len(guidance.dos))
            self.assertEqual(len(set(guidance.donts)), len(guidance.donts))

    def test_merged_with_preserves_order_and_dedupes(self):
        a = Guidance(dos=("x", "y"), donts=("n",))
        b = Guidance(dos=("y", "z"), donts=())
        merged = a.merged_with(b)
        self.assertEqual(merged.dos, ("x", "y", "z"))
        self.assertEqual(merged.donts, ("n",))

    def test_partner_tips_differ_per_trimester(self):
        self.assertNotEqual(partner_tips(5), partner_tips(30))
        for week in (5, 20, 35):
            self.assertTrue(partner_tips(week))

    def test_upcoming_appointments(self):
        appointments = upcoming_appointments(19, limit=2)
        self.assertEqual([a.week for a in appointments], [20, 24])
        self.assertEqual(upcoming_appointments(40, limit=5)[0].week, 40)
        self.assertEqual(upcoming_appointments(20, limit=0), ())


class NewbornTests(unittest.TestCase):
    def test_stages_cover_the_first_four_months_without_gaps(self):
        self.assertEqual(NEWBORN_STAGES[0].start_day, 0)
        for earlier, later in zip(NEWBORN_STAGES, NEWBORN_STAGES[1:]):
            self.assertEqual(later.start_day, earlier.end_day + 1)

    def test_stage_lookup(self):
        self.assertEqual(newborn_stage_for_day(0).start_day, 0)
        self.assertTrue(newborn_stage_for_day(3).covers(3))
        self.assertTrue(newborn_stage_for_day(45).covers(45))
        self.assertIs(newborn_stage_for_day(900), NEWBORN_STAGES[-1])

    def test_stage_content_present(self):
        for stage in NEWBORN_STAGES:
            self.assertTrue(stage.highlights)
            self.assertTrue(stage.care_tips)
            self.assertTrue(stage.warning_signs)

    def test_safe_sleep_guidance_is_included(self):
        guidance = newborn_guidance()
        self.assertTrue(any("back to sleep" in item.lower() for item in guidance.dos))

    def test_invalid_day(self):
        with self.assertRaises(ValueError):
            newborn_stage_for_day(-1)
        with self.assertRaises(TypeError):
            newborn_stage_for_day(1.5)


class BriefingTests(unittest.TestCase):
    def test_briefing_from_week(self):
        briefing = build_briefing(week=20)
        self.assertEqual(briefing.week, 20)
        self.assertEqual(briefing.trimester, 2)
        self.assertIsNone(briefing.due_date)
        self.assertTrue(briefing.partner_tips)
        self.assertTrue(briefing.guidance.dos)
        self.assertEqual(briefing.upcoming_appointments[0].week, 20)

    def test_briefing_from_due_date(self):
        due = date(2026, 10, 8)
        today = due - timedelta(days=70)
        briefing = build_briefing(due_date=due, today=today)
        self.assertEqual(briefing.week, 31)
        self.assertEqual(briefing.trimester, 3)
        self.assertEqual(briefing.days_until_due, 70)
        self.assertEqual(briefing.notes, ())

    def test_briefing_past_due_date_adds_note(self):
        due = date(2026, 10, 8)
        briefing = build_briefing(due_date=due, today=due + timedelta(days=5))
        self.assertEqual(briefing.week, LAST_WEEK)
        self.assertTrue(briefing.notes)

    def test_briefing_requires_exactly_one_input(self):
        with self.assertRaises(ValueError):
            build_briefing()
        with self.assertRaises(ValueError):
            build_briefing(week=10, due_date=date(2026, 10, 8))

    def test_briefing_rejects_out_of_range_week(self):
        for bad in (0, LAST_WEEK + 1):
            with self.assertRaises(ValueError):
                build_briefing(week=bad)


if __name__ == "__main__":
    unittest.main()
