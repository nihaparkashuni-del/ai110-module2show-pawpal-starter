from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta


# ── Task ──────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str          # e.g. "Morning walk"
    time: str                 # "HH:MM" format, e.g. "08:00"
    frequency: str            # "once", "daily", or "weekly"
    pet_name: str             # which pet this belongs to
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self):
        """Return a NEW Task for the next occurrence (daily/weekly only)."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None  # "once" tasks don't repeat

        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            pet_name=self.pet_name,
            due_date=next_date,
            completed=False
        )


# ── Pet ───────────────────────────────────────────────────────────────────────

@dataclass
class Pet:
    """Represents a pet with its own list of tasks."""
    name: str
    species: str              # e.g. "Dog", "Cat"
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


# ── Owner ─────────────────────────────────────────────────────────────────────

class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        """Initialize owner with a name and empty pet list."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Collect and return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_pet_names(self) -> List[str]:
        """Return a list of all pet names."""
        return [pet.name for pet in self.pets]


# ── Scheduler ─────────────────────────────────────────────────────────────────

class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an Owner instance."""
        self.owner = owner

    def get_sorted_tasks(self) -> List[Task]:
        """Return all tasks sorted chronologically by time (HH:MM)."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.time)

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a specific pet."""
        return [t for t in self.owner.get_all_tasks() if t.pet_name == pet_name]

    def mark_task_complete(self, task: Task):
        """
        Mark a task complete. If it recurs, add the next occurrence
        to the correct pet's task list.
        """
        task.mark_complete()

        if task.frequency in ("daily", "weekly"):
            next_task = task.reschedule()
            for pet in self.owner.pets:
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
                    break

    def detect_conflicts(self) -> List[str]:
        """
        Check for tasks scheduled at the exact same time for the same pet.
        Returns a list of human-readable warning strings.
        """
        warnings = []
        tasks = self.owner.get_all_tasks()

        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                t1, t2 = tasks[i], tasks[j]
                if t1.time == t2.time and t1.pet_name == t2.pet_name:
                    warnings.append(
                        f"⚠️  Conflict for {t1.pet_name}: "
                        f'"{t1.description}" and "{t2.description}" '
                        f"both scheduled at {t1.time}"
                    )
        return warnings