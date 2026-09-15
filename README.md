# FamilyJourneyCopilot

AI copilot for pregnancy and newborn guidance, with timelines, education, and support for parents and partners.

Pregnancy Journey Copilot is a companion for expecting parents. It turns the
journey into clear stages and answers the question "what matters right now?"
with week-by-week milestones, practical do's and don'ts, early newborn care,
and support tips for fathers and partners.

## Features

- **Stage-based timeline** - milestones for all 40 pregnancy weeks, grouped by trimester.
- **Personalised briefings** - by week number or estimated due date, including days to go and upcoming appointments.
- **Do's and don'ts** - general advice plus trimester-specific guidance.
- **Partner support** - concrete actions for fathers and partners in every trimester.
- **Newborn guidance** - stages from the golden hour to four months, with care tips and warning signs.
- **Urgent signs** - a short list of symptoms that need immediate medical attention.

## Requirements

Python 3.9 or newer. No third-party dependencies.

## Usage

Run directly from a clone:

```bash
python -m pregnancy_copilot week --week 20
python -m pregnancy_copilot week --due-date 2026-10-08
python -m pregnancy_copilot timeline --from 12 --to 16
python -m pregnancy_copilot guidance --week 8
python -m pregnancy_copilot partner --due-date 2026-10-08
python -m pregnancy_copilot newborn --birth-date 2026-10-01
python -m pregnancy_copilot due-date --last-period 2026-01-01
python -m pregnancy_copilot emergency
```

Or install it to get the `pregnancy-copilot` command:

```bash
pip install .
pregnancy-copilot week --week 20
```

## Library API

The logic is pure Python and can back a web service or a chat assistant:

```python
from datetime import date
from pregnancy_copilot import build_briefing, newborn_stage_for_day

briefing = build_briefing(due_date=date(2026, 10, 8))
print(briefing.week, briefing.trimester)
print(briefing.guidance.dos)
print(briefing.partner_tips)

print(newborn_stage_for_day(10).care_tips)
```

## Tests

```bash
python -m unittest discover -s tests
```

## Disclaimer

This project provides **educational information only and is not medical
advice**. Always follow the guidance of your midwife, obstetrician or
paediatrician, and seek urgent care if something feels wrong.
