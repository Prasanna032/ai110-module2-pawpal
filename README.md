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

## 📸 Demo

> run `streamlit run app.py`.
![Home page](screenshots/1.png)
![Owner and Pet info](screenshots/2.png)
![Tasks](screenshots/3.png)
![Conflicts](screenshots/4.png)
![Schedule](screenshots/5.png)

---

## Features

- **Priority-based scheduling** — Tasks are sorted high → medium → low before scheduling. Within the same priority, tasks are ordered alphabetically so the output is always consistent.
- **Greedy time-fitting** — The scheduler fits as many tasks as possible into the owner's available minutes, skipping any task that no longer fits and recording why.
- **Completed-task filtering** — Tasks already marked done are excluded from the daily schedule automatically, so they never re-appear.
- **Sorting by start time** — sort_by_time() returns all tasks ordered chronologically by their start_time field, used to display the task table in the UI.
- **Conflict detection** — detect_conflicts() checks every pair of pending tasks for overlapping time windows and returns a plain-language warning for each conflict found.
- **Daily and weekly recurrence** — complete_task() marks a task done and immediately creates the next occurrence: +1 day for daily tasks, +7 days for weekly tasks. One-time tasks (frequency="once") are not re-created.
- **Task filtering** — filter_tasks(completed, pet_name) lets the UI query tasks by completion status, by pet, or both at once.
- **Inline task editing** — edit_task() updates any attribute of an existing task (title, priority, duration, start time, etc.) without removing and re-adding it.

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

## Testing PawPal+

### Run the tests

```bash
python -m pytest
```

### What the tests cover

| Test | Behavior verified |
|---|---|
| test_mark_complete_changes_status | mark_complete() flips task.completed to True |
| test_add_task_increases_pet_task_count | Adding a task syncs it to both the owner list and the pet's own list |
| test_sort_by_time_returns_chronological_order | sort_by_time() returns tasks ordered by start_time earliest-first |
| test_complete_daily_task_creates_next_occurrence | Completing a daily task creates a new task due the following day |
| test_complete_once_task_returns_none | Completing a once task returns None and does not grow the task list |
| test_detect_conflicts_flags_overlapping_tasks | Two tasks at the same time produce exactly one CONFLICT warning |
| test_detect_conflicts_clear_for_non_overlapping_tasks | Tasks with a gap between them produce no conflict warnings |
| test_generate_schedule_skips_completed_tasks | Already-completed tasks are excluded from the generated schedule |

### Confidence Level

**4 / 5 stars**

The core behaviors: priority sorting, completed-task filtering, recurrence, and conflict detection, are all tested and working. Confidence is not higher because the greedy scheduling algorithm is not tested for optimality, edge cases like 0 available minutes or all tasks already completed are not covered, and there are no tests for the Streamlit UI layer.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
