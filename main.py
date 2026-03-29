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

# --- Create tasks (total possible = 155 min, limit = 90 min — several will be skipped) ---

# puppy tasks (dog)
morning_walk    = Task(title="Morning Walk",       pet=puppy,  duration_minutes=30, priority="high",   category="walk",       frequency="daily")
feed_puppy      = Task(title="Feed puppy",         pet=puppy,  duration_minutes=10, priority="high",   category="feeding",    frequency="daily")
evening_walk    = Task(title="Evening Walk",        pet=puppy,  duration_minutes=25, priority="medium", category="walk",       frequency="daily")
bath_puppy      = Task(title="Bath Time",           pet=puppy,  duration_minutes=20, priority="low",    category="grooming",   frequency="weekly")
fetch_session   = Task(title="Fetch Session",       pet=puppy,  duration_minutes=15, priority="low",    category="enrichment", frequency="daily")

# Luna tasks (cat)
feed_luna       = Task(title="Feed Luna",           pet=luna,   duration_minutes=10, priority="high",   category="feeding",    frequency="daily")
give_meds       = Task(title="Give Supplements",    pet=luna,   duration_minutes=5,  priority="high",   category="medication", frequency="daily")
brush_luna      = Task(title="Brush Luna",          pet=luna,   duration_minutes=15, priority="low",    category="grooming",   frequency="weekly")

# Pepper tasks (rabbit)
feed_pepper     = Task(title="Feed Pepper",         pet=pepper, duration_minutes=10, priority="high",   category="feeding",    frequency="daily")
clean_hutch     = Task(title="Clean Hutch",         pet=pepper, duration_minutes=20, priority="medium", category="grooming",   frequency="weekly")
exercise_pepper = Task(title="Exercise Time",       pet=pepper, duration_minutes=15, priority="medium", category="enrichment", frequency="daily")

all_tasks = [
    morning_walk, feed_puppy, evening_walk, bath_puppy, fetch_session,
    feed_luna, give_meds, brush_luna,
    feed_pepper, clean_hutch, exercise_pepper,
]

for task in all_tasks:
    jordan.add_task(task)

# --- Generate schedule ---
scheduler = Scheduler(owner=jordan)
today = date.today().isoformat()
plan = scheduler.generate_schedule(date=today)

# --- Print results ---
print(plan.display())
print()
print("--- Reasoning ---")
print(plan.get_summary())
