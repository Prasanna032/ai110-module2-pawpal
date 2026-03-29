from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def _make_owner(minutes=120):
    return Owner(name="Jordan", available_minutes=minutes, preferred_start_time="08:00")


def _make_pet(name="Puppy", species="dog", age=3):
    return Pet(name=name, species=species, age=age)


# ---------------------------------------------------------------------------
# Existing tests
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status"""
    pet = _make_pet()
    task = Task(title="Morning Walk", pet=pet, duration_minutes=30, priority="high", category="walk")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count"""
    owner = _make_owner()
    pet = _make_pet("Luna", "cat", 5)
    owner.add_pet(pet)

    assert len(pet.tasks) == 0

    task = Task(title="Feed Luna", pet=pet, duration_minutes=10, priority="high", category="feeding")
    owner.add_task(task)

    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# 1. Sorting correctness — tasks come back in chronological (start_time) order
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() must return tasks ordered earliest start_time first."""
    owner = _make_owner()
    pet = _make_pet()
    owner.add_pet(pet)

    t1 = Task(title="Evening Walk", pet=pet, duration_minutes=30, priority="low",
              category="walk", start_time="18:00")
    t2 = Task(title="Morning Feed", pet=pet, duration_minutes=10, priority="high",
              category="feeding", start_time="07:00")
    t3 = Task(title="Midday Meds",  pet=pet, duration_minutes=5,  priority="high",
              category="medication", start_time="12:00")

    for t in [t1, t2, t3]:
        owner.add_task(t)

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time()

    assert ordered[0].start_time == "07:00"
    assert ordered[1].start_time == "12:00"
    assert ordered[2].start_time == "18:00"


# ---------------------------------------------------------------------------
# 2. Recurrence logic — completing a daily task creates a next-day task
# ---------------------------------------------------------------------------

def test_complete_daily_task_creates_next_occurrence():
    """complete_task() on a daily task must add a new task due the following day."""
    owner = _make_owner()
    pet = _make_pet()
    owner.add_pet(pet)

    today = date.today().isoformat()
    task = Task(title="Morning Walk", pet=pet, duration_minutes=30,
                priority="high", category="walk", frequency="daily", due_date=today)
    owner.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == (date.today() + timedelta(days=1)).isoformat()
    assert next_task.title == task.title
    assert next_task in owner.tasks


def test_complete_once_task_returns_none():
    """complete_task() on a frequency='once' task must return None and not add a new task."""
    owner = _make_owner()
    pet = _make_pet()
    owner.add_pet(pet)

    task = Task(title="Vet Visit", pet=pet, duration_minutes=60,
                priority="high", category="medication", frequency="once")
    owner.add_task(task)
    initial_count = len(owner.tasks)

    scheduler = Scheduler(owner)
    result = scheduler.complete_task(task)

    assert result is None
    assert task.completed is True
    assert len(owner.tasks) == initial_count   # no new task added


# ---------------------------------------------------------------------------
# 3. Conflict detection — overlapping and non-overlapping time windows
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_overlapping_tasks():
    """detect_conflicts() must return a warning when two tasks share time."""
    owner = _make_owner()
    pet = _make_pet()
    owner.add_pet(pet)

    # Both start at 09:00 and both run 30 min — clear overlap
    t1 = Task(title="Walk",    pet=pet, duration_minutes=30, priority="high",
              category="walk",    start_time="09:00")
    t2 = Task(title="Feeding", pet=pet, duration_minutes=30, priority="high",
              category="feeding", start_time="09:00")

    for t in [t1, t2]:
        owner.add_task(t)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "CONFLICT" in conflicts[0]


def test_detect_conflicts_clear_for_non_overlapping_tasks():
    """detect_conflicts() must return no warnings when tasks don't overlap."""
    owner = _make_owner()
    pet = _make_pet()
    owner.add_pet(pet)

    # 08:00–08:30, then 09:00–09:30 — gap of 30 min between them
    t1 = Task(title="Morning Walk", pet=pet, duration_minutes=30, priority="high",
              category="walk",    start_time="08:00")
    t2 = Task(title="Feed",         pet=pet, duration_minutes=30, priority="high",
              category="feeding", start_time="09:00")

    for t in [t1, t2]:
        owner.add_task(t)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


# ---------------------------------------------------------------------------
# 4. Completed tasks are excluded from the generated schedule
# ---------------------------------------------------------------------------

def test_generate_schedule_skips_completed_tasks():
    """generate_schedule() must not include tasks that are already completed."""
    owner = _make_owner(minutes=120)
    pet = _make_pet()
    owner.add_pet(pet)

    done  = Task(title="Done Task",    pet=pet, duration_minutes=20, priority="high",
                 category="feeding")
    todo  = Task(title="Pending Task", pet=pet, duration_minutes=20, priority="high",
                 category="walk")
    done.mark_complete()

    owner.add_task(done)
    owner.add_task(todo)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_schedule(date.today().isoformat())

    scheduled_titles = [t.title for t in plan.scheduled_tasks]
    assert "Done Task"    not in scheduled_titles
    assert "Pending Task" in scheduled_titles
