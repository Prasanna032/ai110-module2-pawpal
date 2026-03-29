import streamlit as st
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

if st.button("Add task"):
    if st.session_state.owner is None:
        st.warning("Save your owner & pet first.")
    else:
        owner = st.session_state.owner
        pet = owner.pets[0]
        task = Task(title=task_title, pet=pet, duration_minutes=int(duration),
                    priority=priority, category="general")
        st.session_state.scheduler.add_task(task)
        st.success(f"Added '{task_title}' ({priority}, {duration} min)")

if st.session_state.owner and st.session_state.owner.tasks:
    st.write("Current tasks:")
    st.table([
        {"Title": t.title, "Pet": t.pet.name, "Duration": t.duration_minutes, "Priority": t.priority}
        for t in st.session_state.owner.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if st.session_state.scheduler is None or not st.session_state.owner.tasks:
        st.warning("Add an owner, pet, and at least one task first.")
    else:
        from datetime import date
        plan = st.session_state.scheduler.generate_schedule(date=date.today().isoformat())
        st.success("Schedule generated!")
        st.text(plan.display())
        with st.expander("Reasoning"):
            st.text(plan.get_summary())
