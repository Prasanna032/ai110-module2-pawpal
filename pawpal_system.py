from dataclasses import dataclass
from typing import List, Optional
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# ---------------------------------------------------------------------------
# Pet — represents a single animal
# ---------------------------------------------------------------------------
@dataclass
class Pet:
    name: str
    species: str          # "dog", "cat", "other"
    age: int
    notes: str = ""

    def __post_init__(self):
        self.tasks: List["Task"] = []

    def add_task(self, task: "Task") -> None:
        """Add a task that belongs to this pet."""
        self.tasks.append(task)

    def get_info(self) -> str:
        """Return a short readable summary of this pet."""
        info = f"{self.name} ({self.species}, age {self.age})"
        if self.notes:
            info += f" — {self.notes}"
        return info


# ---------------------------------------------------------------------------
# Task — represents one care activity; holds a direct reference to its Pet
# ---------------------------------------------------------------------------
@dataclass
class Task:
    title: str
    pet: Pet                # direct reference instead of just pet_name string
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    category: str           # "walk", "feeding", "medication", "grooming", "enrichment"
    frequency: str = "daily"              # "daily", "weekly", "once"
    start_time: str = "08:00"            # preferred start time in "HH:MM" format
    due_date: str = ""                   # "YYYY-MM-DD"; set automatically on creation
    completed: bool = False

    def __post_init__(self):
        if not self.due_date:
            self.due_date = date.today().isoformat()

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"


# ---------------------------------------------------------------------------
# Owner — the person using the app; has one or more pets and their tasks
# ---------------------------------------------------------------------------
class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str):
        self.name = name
        self.available_minutes = available_minutes        # total minutes free today
        self.preferred_start_time = preferred_start_time  # e.g. "08:00"
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []                       # all tasks across all pets

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a task to the owner's task list and to the relevant pet's list."""
        self.tasks.append(task)
        task.pet.add_task(task)

    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Return all tasks that belong to a specific pet."""
        return [t for t in self.tasks if t.pet == pet]


# ---------------------------------------------------------------------------
# DailyPlan — the output produced by the Scheduler
# ---------------------------------------------------------------------------
class DailyPlan:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used: int = 0
        self.reasoning: List[str] = []

    def display(self) -> str:
        """Return a formatted string of the full plan, suitable for the UI."""
        if not self.scheduled_tasks:
            return f"No tasks scheduled for {self.date}."

        lines = [f"Daily Plan — {self.date}", ""]
        for i, task in enumerate(self.scheduled_tasks, start=1):
            lines.append(
                f"{i}. [{task.priority.upper()}] {task.title} "
                f"({task.pet.name}, {task.duration_minutes} min)"
            )

        lines.append("")
        lines.append(f"Total time: {self.total_time_used} min")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped:")
            for task in self.skipped_tasks:
                lines.append(f"  - {task.title} ({task.pet.name})")

        return "\n".join(lines)

    def get_summary(self) -> str:
        """Return the reasoning notes recorded during scheduling."""
        if not self.reasoning:
            return "No reasoning recorded."
        return "\n".join(self.reasoning)


# ---------------------------------------------------------------------------
# Time helpers — convert "HH:MM" strings to/from total minutes
# ---------------------------------------------------------------------------
def _to_minutes(hhmm: str) -> int:
    """Convert 'HH:MM' string to total minutes since midnight."""
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def _from_minutes(total: int) -> str:
    """Convert total minutes since midnight back to 'HH:MM' string."""
    return f"{total // 60:02d}:{total % 60:02d}"


# ---------------------------------------------------------------------------
# Scheduler — core logic; builds one combined DailyPlan for the owner
# ---------------------------------------------------------------------------
class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.plan: Optional[DailyPlan] = None

    def add_task(self, task: Task) -> None:
        """Add a task to the owner's task list."""
        self.owner.add_task(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the owner's task list and from the pet's task list."""
        if task in self.owner.tasks:
            self.owner.tasks.remove(task)
        if task in task.pet.tasks:
            task.pet.tasks.remove(task)

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if recurring, schedule the next occurrence."""
        task.mark_complete()

        if task.frequency == "once":
            return None  # no follow-up needed

        current_due = date.fromisoformat(task.due_date)
        if task.frequency == "daily":
            next_due = current_due + timedelta(days=1)
        else:  # weekly
            next_due = current_due + timedelta(weeks=1)

        next_task = Task(
            title=task.title,
            pet=task.pet,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            category=task.category,
            frequency=task.frequency,
            start_time=task.start_time,
            due_date=next_due.isoformat(),
        )
        self.owner.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> List[str]:
        """Return a list of warning messages for tasks whose time windows overlap."""
        warnings = []
        pending = [t for t in self.owner.tasks if not t.completed]

        for i, a in enumerate(pending):
            for b in pending[i + 1:]:
                a_start = _to_minutes(a.start_time)
                a_end   = a_start + a.duration_minutes
                b_start = _to_minutes(b.start_time)
                b_end   = b_start + b.duration_minutes

                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"CONFLICT: '{a.title}' ({a.pet.name}, {a.start_time}–{_from_minutes(a_end)}) "
                        f"overlaps with '{b.title}' ({b.pet.name}, {b.start_time}–{_from_minutes(b_end)})"
                    )
        return warnings

    def sort_by_time(self) -> List[Task]:
        """Return owner's tasks sorted by start_time (HH:MM) ascending."""
        return sorted(self.owner.tasks, key=lambda t: t.start_time)

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        result = self.owner.tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet.name == pet_name]
        return result

    def edit_task(self, task: Task, **updates) -> None:
        """Update attributes of an existing task. Pass keyword args to change (e.g. priority='high')."""
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)

    def generate_schedule(self, date: str) -> DailyPlan:
        """Sort tasks by priority and greedily schedule them within available time."""
        plan = DailyPlan(date)
        time_remaining = self.owner.available_minutes

        # Filter out already-completed tasks, then sort by priority and title
        pending = [t for t in self.owner.tasks if not t.completed]
        sorted_tasks = sorted(
            pending,
            key=lambda t: (PRIORITY_ORDER[t.priority], t.title)
        )

        plan.reasoning.append(
            f"Owner {self.owner.name} has {time_remaining} minutes available on {date}."
        )

        for task in sorted_tasks:
            if task.duration_minutes <= time_remaining:
                plan.scheduled_tasks.append(task)
                time_remaining -= task.duration_minutes
                plan.total_time_used += task.duration_minutes
                plan.reasoning.append(
                    f"SCHEDULED: '{task.title}' for {task.pet.name} "
                    f"({task.priority} priority, {task.duration_minutes} min). "
                    f"{time_remaining} min remaining."
                )
            else:
                plan.skipped_tasks.append(task)
                plan.reasoning.append(
                    f"SKIPPED: '{task.title}' for {task.pet.name} "
                    f"({task.duration_minutes} min needed, only {time_remaining} min left)."
                )

        self.plan = plan
        return plan
