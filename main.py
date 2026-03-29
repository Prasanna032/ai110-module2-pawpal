from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup owner ---
jordan = Owner(
    name="Jordan",
    available_minutes=90,
    preferred_start_time="08:00"
)

# --- Create pets ---
puppy  = Pet(name="puppy",  species="dog",   age=3, notes="loves fetch")
luna   = Pet(name="Luna",   species="cat",   age=5, notes="on joint supplements")
pepper = Pet(name="Pepper", species="other", age=2, notes="house rabbit, needs daily exercise")

jordan.add_pet(puppy)
jordan.add_pet(luna)
jordan.add_pet(pepper)

# --- Create tasks added OUT OF ORDER to test sort_by_time() ---
# (start_time values are intentionally scrambled)

# puppy tasks (dog)
morning_walk    = Task(title="Morning Walk",    pet=puppy,  duration_minutes=30, priority="high",   category="walk",       frequency="daily",  start_time="07:00")
feed_puppy      = Task(title="Feed Puppy",      pet=puppy,  duration_minutes=10, priority="high",   category="feeding",    frequency="daily",  start_time="08:00")
evening_walk    = Task(title="Evening Walk",    pet=puppy,  duration_minutes=25, priority="medium", category="walk",       frequency="daily",  start_time="18:00")
bath_puppy      = Task(title="Bath Time",       pet=puppy,  duration_minutes=20, priority="low",    category="grooming",   frequency="weekly", start_time="11:00")
fetch_session   = Task(title="Fetch Session",   pet=puppy,  duration_minutes=15, priority="low",    category="enrichment", frequency="daily",  start_time="16:00")

# Luna tasks (cat)
feed_luna       = Task(title="Feed Luna",       pet=luna,   duration_minutes=10, priority="high",   category="feeding",    frequency="daily",  start_time="08:30")
give_meds       = Task(title="Give Meds",       pet=luna,   duration_minutes=5,  priority="high",   category="medication", frequency="daily",  start_time="09:00")
brush_luna      = Task(title="Brush Luna",      pet=luna,   duration_minutes=15, priority="low",    category="grooming",   frequency="weekly", start_time="14:00")

# Pepper tasks (rabbit) — added in reverse time order to make sorting obvious
feed_pepper     = Task(title="Feed Pepper",     pet=pepper, duration_minutes=10, priority="high",   category="feeding",    frequency="daily",  start_time="08:15")
exercise_pepper = Task(title="Exercise Time",   pet=pepper, duration_minutes=15, priority="medium", category="enrichment", frequency="daily",  start_time="15:00")
clean_hutch     = Task(title="Clean Hutch",     pet=pepper, duration_minutes=20, priority="medium", category="grooming",   frequency="weekly", start_time="10:00")

all_tasks = [
    # added out of time order on purpose
    evening_walk, give_meds, feed_pepper, morning_walk,
    clean_hutch, feed_luna, bath_puppy, exercise_pepper,
    feed_puppy, brush_luna, fetch_session,
]

for task in all_tasks:
    jordan.add_task(task)

# --- Add two intentionally overlapping tasks to trigger conflict detection ---
# morning_walk starts at 07:00 and lasts 30 min (ends 07:30)
# overlap_task starts at 07:15 — squarely inside morning_walk's window
overlap_task = Task(title="Vet Call", pet=puppy, duration_minutes=20,
                    priority="high", category="general", start_time="07:15")
jordan.add_task(overlap_task)

# --- Generate schedule ---
scheduler = Scheduler(owner=jordan)
today = date.today().isoformat()
plan = scheduler.generate_schedule(date=today)

# --- Print schedule ---
print(plan.display())
print()
print("--- Reasoning ---")
print(plan.get_summary())

print("\n" + "=" * 50)

# --- Demo: detect_conflicts() ---
print("\n--- Conflict Detection ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")

# --- Demo: sort_by_time() ---
print("\n--- All tasks sorted by start_time ---")
for t in scheduler.sort_by_time():
    print(f"  {t.start_time}  {t.title} ({t.pet.name})")

# --- Demo: filter_tasks() by pet ---
print("\n--- Tasks for Luna only ---")
for t in scheduler.filter_tasks(pet_name="Luna"):
    print(f"  {t.title} ({t.priority} priority)")

# --- Demo: complete_task() with recurrence ---
print("\n--- Completing 'Give Meds' (daily) and 'Clean Hutch' (weekly) ---")

next_meds = scheduler.complete_task(give_meds)
next_hutch = scheduler.complete_task(clean_hutch)

print(f"  Give Meds completed. Next occurrence due: {next_meds.due_date}")
print(f"  Clean Hutch completed. Next occurrence due: {next_hutch.due_date}")

# Completing a "once" task — no follow-up should be created
fetch_session.frequency = "once"
result = scheduler.complete_task(fetch_session)
print(f"  Fetch Session (once) completed. Follow-up created: {result is not None}")

print("\n--- Completed tasks ---")
for t in scheduler.filter_tasks(completed=True):
    print(f"  {t.title} ({t.pet.name}) — due {t.due_date}")

print("\n--- Pending tasks (includes new recurring instances) ---")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.title} ({t.pet.name}) — due {t.due_date}")
