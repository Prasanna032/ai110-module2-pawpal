# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

PawPal+ was designed and built in phases. Here is a summary of what was implemented:

**Core classes** (`pawpal_system.py`):
- `Pet` — stores animal details (name, species, age, notes) and its own task list
- `Task` — represents one care activity with title, priority, duration, category, frequency, start time, due date, and completion status
- `Owner` — manages multiple pets and all their tasks in one place
- `Scheduler` — the brain; reads the owner's tasks and produces a `DailyPlan`
- `DailyPlan` — the output; holds scheduled tasks, skipped tasks, total time used, and reasoning notes

**Scheduling logic:**
- Tasks are sorted by priority (high → medium → low) then scheduled greedily within the owner's available time budget
- Already-completed tasks are excluded automatically
- Skipped tasks are recorded with an explanation of why they didn't fit

**Smarter scheduling features:**
- **Recurring tasks** — `complete_task()` marks a task done and automatically creates the next occurrence (daily = +1 day, weekly = +7 days) using Python's `timedelta`
- **Conflict detection** — `detect_conflicts()` checks every pair of pending tasks for overlapping time windows and returns human-readable warnings without crashing
- **Sort by time** — `sort_by_time()` returns tasks ordered chronologically by `start_time`
- **Filter tasks** — `filter_tasks(completed, pet_name)` queries the task list by completion status, pet, or both

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
