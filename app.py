import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# Initialize session state for persistent data
if 'owner' not in st.session_state:
    st.session_state.owner = None
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = None

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Create Pet"):
    # Improvement #9: prevent duplicate pet names (causes silent bugs in add/remove_task)
    existing_names = [p.name for p in st.session_state.owner.pets] if st.session_state.owner else []
    if pet_name in existing_names:
        st.error(f"A pet named '{pet_name}' already exists. Use a unique name.")
    else:
        pet = Pet(name=pet_name, species=species, age=1, needs={}, tasks=[])
        if st.session_state.owner:
            st.session_state.owner.pets.append(pet)
            st.success(f"Pet {pet_name} added to existing owner!")
        else:
            st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=60, preferences={}, constraints=[], pets=[pet])
            st.success(f"Pet {pet_name} created!")

# Display current pets
if st.session_state.owner:
    st.write("Current Pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species})")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.owner:
        priority_map = {"low": 1, "medium": 3, "high": 5}
        task = Task(
            id=str(len(st.session_state.tasks) + 1),
            description=task_title,
            type="general",
            duration_minutes=duration,
            priority=priority_map[priority],
            required=True,
            frequency="daily",
            completion_status=False
        )
        scheduler = Scheduler(st.session_state.owner)
        scheduler.add_task(task, pet_name)
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority, "pet": pet_name}
        )
        st.success("Task added!")
    else:
        st.error("Create a pet first.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if st.session_state.owner:
        scheduler = Scheduler(st.session_state.owner)
        plan_explanation = scheduler.explain_plan()
        st.write("Today's Schedule:")
        st.text(plan_explanation)
    else:
        st.error("Create a pet first.")
