import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Minutes available today", min_value=10, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save owner & pet"):
    pet = Pet(name=pet_name, species=species, age=0)
    owner = Owner(name=owner_name, available_minutes=int(available_minutes), preferred_start_time="08:00")
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Saved {owner_name} with pet {pet_name}.")

st.markdown("### Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    category = st.selectbox("Category", ["walk", "feeding", "medication", "grooming", "enrichment"])
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

start_time = st.text_input("Start time (HH:MM)", value="08:00")

if st.button("Add task"):
    if st.session_state.owner is None:
        st.warning("Save your owner & pet first.")
    else:
        owner = st.session_state.owner
        pet = owner.pets[0]
        task = Task(title=task_title, pet=pet, duration_minutes=int(duration),
                    priority=priority, category=category, frequency=frequency,
                    start_time=start_time)
        st.session_state.scheduler.add_task(task)
        st.success(f"Added '{task_title}' ({priority}, {duration} min, starts {start_time})")

if st.session_state.owner and st.session_state.owner.tasks:
    scheduler = st.session_state.scheduler

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")

    # Tasks sorted chronologically by start_time
    st.write("Current tasks (sorted by start time):")
    st.table([
        {
            "Title": t.title,
            "Pet": t.pet.name,
            "Start": t.start_time,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.upper(),
            "Category": t.category,
            "Frequency": t.frequency,
            "Done": "✓" if t.completed else "",
        }
        for t in scheduler.sort_by_time()
    ])

    # Mark complete
    st.markdown("**Mark a task complete**")
    pending_tasks = scheduler.filter_tasks(completed=False)
    if pending_tasks:
        task_to_complete = st.selectbox(
            "Select task to mark complete",
            options=pending_tasks,
            format_func=lambda t: f"{t.title} ({t.pet.name}, {t.start_time})",
        )
        if st.button("Mark complete"):
            next_task = scheduler.complete_task(task_to_complete)
            if next_task:
                st.success(
                    f"'{task_to_complete.title}' marked complete. "
                    f"Next occurrence scheduled for {next_task.due_date}."
                )
            else:
                st.success(f"'{task_to_complete.title}' marked complete (one-time task, no recurrence).")
            st.rerun()
    else:
        st.info("All tasks are complete.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.scheduler is None or not st.session_state.owner.tasks:
        st.warning("Add an owner, pet, and at least one task first.")
    else:
        scheduler = st.session_state.scheduler
        plan = scheduler.generate_schedule(date=date.today().isoformat())

        scheduled_count = len(plan.scheduled_tasks)
        skipped_count = len(plan.skipped_tasks)

        if scheduled_count == 0:
            st.warning("No tasks could be scheduled — all tasks are complete or exceed available time.")
        else:
            st.success(f"Schedule generated: {scheduled_count} task(s) scheduled, {skipped_count} skipped.")

        if plan.scheduled_tasks:
            st.markdown("**Scheduled tasks**")
            st.table([
                {
                    "#": i,
                    "Title": t.title,
                    "Pet": t.pet.name,
                    "Priority": t.priority.upper(),
                    "Duration (min)": t.duration_minutes,
                }
                for i, t in enumerate(plan.scheduled_tasks, start=1)
            ])

        if plan.skipped_tasks:
            st.markdown("**Skipped tasks** (not enough time remaining)")
            st.table([
                {"Title": t.title, "Pet": t.pet.name, "Duration (min)": t.duration_minutes}
                for t in plan.skipped_tasks
            ])

        st.metric("Total time used", f"{plan.total_time_used} min",
                  delta=f"{st.session_state.owner.available_minutes - plan.total_time_used} min free")

        with st.expander("Scheduling reasoning"):
            st.text(plan.get_summary())
