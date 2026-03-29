from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# Pet — represents a single animal
# ---------------------------------------------------------------------------
@dataclass
class Pet:
    name: str
    species: str          # "dog", "cat", "other"
    age: int
    notes: str = ""

    def get_info(self) -> str:
        """Return a short readable summary of this pet."""
        pass


# ---------------------------------------------------------------------------
# Task — represents one care activity for a specific pet
# ---------------------------------------------------------------------------
@dataclass
class Task:
    title: str
    pet_name: str
    duration_minutes: int
    priority: str         # "low", "medium", "high"
    category: str         # "walk", "feeding", "medication", "grooming", "enrichment"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        pass


# ---------------------------------------------------------------------------
# Owner — the person using the app; has one or more pets
# ---------------------------------------------------------------------------
class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str):
        self.name = name
        self.available_minutes = available_minutes      # total minutes free today
        self.preferred_start_time = preferred_start_time  # e.g. "08:00"
        self.pets: List[Pet] = []

    def get_available_time(self) -> int:
        """Return how many minutes the owner has available today."""
        pass


# ---------------------------------------------------------------------------
# DailyPlan — the output produced by the Scheduler
# ---------------------------------------------------------------------------
class DailyPlan:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used: int = 0

    def display(self) -> str:
        """Return a formatted string of the full plan, suitable for the UI."""
        pass

    def get_summary(self) -> str:
        """Return a short text summary with reasoning for each decision."""
        pass


# ---------------------------------------------------------------------------
# Scheduler — core logic; builds one combined DailyPlan for the owner
# ---------------------------------------------------------------------------
class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []
        self.schedule: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the list of tasks to be scheduled."""
        pass

    def generate_schedule(self) -> DailyPlan:
        """Pick and order tasks based on priority and available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were chosen or skipped."""
        pass
