import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Fixtures (reusable test data) ─────────────────────────────────────────────

@pytest.fixture
def sample_owner():
    """Create an owner with one dog and a few tasks."""
    owner = Owner("Alex")
    dog = Pet(name="Buddy", species="Dog", age=3)
    dog.add_task(Task("Evening walk",    "18:00", "daily",  "Buddy"))
    dog.add_task(Task("Morning walk",    "07:00", "daily",  "Buddy"))
    dog.add_task(Task("Flea medication", "09:00", "weekly", "Buddy"))
    owner.add_pet(dog)
    return owner


# ── Test 1: Task completion changes status ────────────────────────────────────

def test_mark_complete():
    """Calling mark_complete() should set completed to True."""
    task = Task("Bath time", "10:00", "once", "Buddy")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


# ── Test 2: Adding a task increases pet task count ────────────────────────────

def test_add_task_increases_count():
    """Adding a task to a pet should increase its task list by 1."""
    pet = Pet(name="Luna", species="Cat", age=2)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Breakfast", "08:00", "daily", "Luna"))
    assert len(pet.tasks) == 1


# ── Test 3: Sorting returns tasks in chronological order ─────────────────────

def test_sort_by_time(sample_owner):
    """Tasks should be sorted from earliest to latest time."""
    scheduler = Scheduler(sample_owner)
    sorted_tasks = scheduler.get_sorted_tasks()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


# ── Test 4: Recurring task creates next occurrence ───────────────────────────

def test_recurring_task_reschedules(sample_owner):
    """Completing a daily task should add a new task for the next day."""
    scheduler = Scheduler(sample_owner)
    dog = sample_owner.pets[0]
    morning_walk = dog.tasks[1]  # "Morning walk" at 07:00

    original_count = len(dog.tasks)
    original_date = morning_walk.due_date

    scheduler.mark_task_complete(morning_walk)

    assert morning_walk.completed == True
    assert len(dog.tasks) == original_count + 1
    new_task = dog.tasks[-1]
    assert new_task.due_date == original_date + timedelta(days=1)
    assert new_task.completed == False


# ── Test 5: Conflict detection flags duplicate times ─────────────────────────

def test_conflict_detection():
    """Two tasks for the same pet at the same time should be flagged."""
    owner = Owner("Sam")
    dog = Pet(name="Rex", species="Dog", age=4)
    dog.add_task(Task("Medication", "09:00", "once", "Rex"))
    dog.add_task(Task("Vet visit",  "09:00", "once", "Rex"))
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Rex" in conflicts[0]