from dataclasses import dataclass
from typing import List, Optional

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
    frequency: str = "daily"  # "daily", "weekly", "once"
    completed: bool = False

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

    def edit_task(self, task: Task, **updates) -> None:
        """Update attributes of an existing task. Pass keyword args to change (e.g. priority='high')."""
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)

    def generate_schedule(self, date: str) -> DailyPlan:
        """Sort tasks by priority and greedily schedule them within available time."""
        plan = DailyPlan(date)
        time_remaining = self.owner.available_minutes

        # Sort by priority, then alphabetically by title for consistent ordering
        sorted_tasks = sorted(
            self.owner.tasks,
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
