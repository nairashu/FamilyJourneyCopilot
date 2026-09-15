import io
import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta

from pregnancy_copilot.cli import main


def run(*argv):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        exit_code = main(list(argv))
    return exit_code, buffer.getvalue()


class CliTests(unittest.TestCase):
    def test_week_briefing(self):
        code, out = run("week", "--week", "20")
        self.assertEqual(code, 0)
        self.assertIn("Week 20 (trimester 2)", out)
        self.assertIn("Do's:", out)
        self.assertIn("Don'ts:", out)
        self.assertIn("Partner support:", out)
        self.assertIn("not medical advice", out)

    def test_week_from_due_date(self):
        due = date.today() + timedelta(days=70)
        code, out = run("week", "--due-date", due.isoformat())
        self.assertEqual(code, 0)
        self.assertIn("Week 31", out)
        self.assertIn("70 days to go", out)

    def test_timeline_range(self):
        code, out = run("timeline", "--from", "12", "--to", "15")
        self.assertEqual(code, 0)
        self.assertIn("Week 12", out)
        self.assertIn("Week 15", out)
        self.assertNotIn("Week 16", out)
        self.assertIn("Trimester 2", out)

    def test_guidance_and_partner(self):
        _, guidance_out = run("guidance", "--week", "8")
        self.assertIn("Do's:", guidance_out)
        _, partner_out = run("partner", "--week", "8")
        self.assertIn("Partner support for week 8", partner_out)

    def test_newborn_defaults_to_day_zero(self):
        code, out = run("newborn")
        self.assertEqual(code, 0)
        self.assertIn("day 0", out)
        self.assertIn("Care tips:", out)

    def test_newborn_from_birth_date(self):
        birth = date.today() - timedelta(days=10)
        _, out = run("newborn", "--birth-date", birth.isoformat())
        self.assertIn("day 10", out)

    def test_due_date_command(self):
        _, out = run("due-date", "--last-period", "2026-01-01")
        self.assertIn("2026-10-08", out)

    def test_emergency_command(self):
        _, out = run("emergency")
        self.assertIn("Seek urgent care", out)

    def test_invalid_week_exits(self):
        with self.assertRaises(SystemExit):
            run("week", "--week", "99")

    def test_invalid_date_format_exits(self):
        with self.assertRaises(SystemExit):
            run("due-date", "--last-period", "01-01-2026")

    def test_newborn_rejects_conflicting_arguments(self):
        with self.assertRaises(SystemExit):
            run("newborn", "--day", "3", "--birth-date", date.today().isoformat())

    def test_newborn_rejects_future_birth_date(self):
        future = date.today() + timedelta(days=2)
        with self.assertRaises(SystemExit):
            run("newborn", "--birth-date", future.isoformat())

    def test_timeline_rejects_reversed_range(self):
        with self.assertRaises(SystemExit):
            run("timeline", "--from", "20", "--to", "10")


if __name__ == "__main__":
    unittest.main()
