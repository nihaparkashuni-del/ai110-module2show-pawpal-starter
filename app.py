import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Session State (persistent memory) ────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Household")

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🐾 PawPal+")
st.caption("Smart pet care management system")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Add a Pet
# ══════════════════════════════════════════════════════════════════════════════
st.header("➕ Add a Pet")

with st.form("add_pet_form"):
    col1, col2, col3 = st.columns(3)
    pet_name    = col1.text_input("Pet Name")
    pet_species = col2.text_input("Species (e.g. Dog, Cat)")
    pet_age     = col3.number_input("Age", min_value=0, max_value=30, value=1)
    submitted   = st.form_submit_button("Add Pet")

if submitted:
    if pet_name.strip() == "":
        st.warning("Please enter a pet name.")
    elif pet_name in owner.get_pet_names():
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=pet_species, age=int(pet_age)))
        st.success(f"🐶 {pet_name} added!")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Add a Task
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Schedule a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        task_pet   = col1.selectbox("Pet", owner.get_pet_names())
        task_desc  = col2.text_input("Task Description")
        col3, col4 = st.columns(2)
        task_time  = col3.text_input("Time (HH:MM)", value="08:00")
        task_freq  = col4.selectbox("Frequency", ["once", "daily", "weekly"])
        task_submitted = st.form_submit_button("Add Task")

    if task_submitted:
        if task_desc.strip() == "":
            st.warning("Please enter a task description.")
        else:
            new_task = Task(
                description=task_desc,
                time=task_time,
                frequency=task_freq,
                pet_name=task_pet,
                due_date=date.today()
            )
            for pet in owner.pets:
                if pet.name == task_pet:
                    pet.add_task(new_task)
            st.success(f"✅ Task '{task_desc}' added for {task_pet}!")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Today's Schedule
# ══════════════════════════════════════════════════════════════════════════════
st.header(f"📅 Today's Schedule — {date.today()}")

# Conflict warnings
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)

# Sorted task list
sorted_tasks = scheduler.get_sorted_tasks()

if not sorted_tasks:
    st.info("No tasks scheduled yet.")
else:
    for i, task in enumerate(sorted_tasks):
        col1, col2 = st.columns([4, 1])
        status_icon = "✅" if task.completed else "🔲"
        col1.markdown(
            f"{status_icon} **[{task.time}]** {task.pet_name}: {task.description} "
            f"_({task.frequency})_"
        )
        if not task.completed:
            if col2.button("Complete", key=f"complete_{i}"):
                scheduler.mark_task_complete(task)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Filter Tasks
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔍 Filter Tasks")

if owner.pets:
    col1, col2 = st.columns(2)
    filter_pet    = col1.selectbox("Filter by Pet", ["All"] + owner.get_pet_names())
    filter_status = col2.selectbox("Filter by Status", ["All", "Pending", "Completed"])

    filtered = scheduler.get_sorted_tasks()

    if filter_pet != "All":
        filtered = [t for t in filtered if t.pet_name == filter_pet]
    if filter_status == "Pending":
        filtered = [t for t in filtered if not t.completed]
    elif filter_status == "Completed":
        filtered = [t for t in filtered if t.completed]

    if filtered:
        for task in filtered:
            status = "✅ Done" if task.completed else "🔲 Pending"
            st.markdown(f"- **{task.pet_name}** | {task.time} | {task.description} | {status}")
    else:
        st.info("No tasks match that filter.")