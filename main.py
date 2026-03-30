from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# ── Create Owner and Pets ─────────────────────────────────────────────────────
owner = Owner("Alex")

dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Luna",  species="Cat", age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# ── Add Tasks (intentionally out of order to test sorting) ───────────────────
dog.add_task(Task("Evening walk",    "18:00", "daily",  "Buddy"))
dog.add_task(Task("Morning walk",    "07:00", "daily",  "Buddy"))
dog.add_task(Task("Flea medication", "09:00", "weekly", "Buddy"))
dog.add_task(Task("Vet appointment", "09:00", "once",   "Buddy"))  # conflict!

cat.add_task(Task("Breakfast",       "08:00", "daily",  "Luna"))
cat.add_task(Task("Playtime",        "15:00", "daily",  "Luna"))

# ── Create Scheduler ─────────────────────────────────────────────────────────
scheduler = Scheduler(owner)

# ── Print Today's Sorted Schedule ────────────────────────────────────────────
print("=" * 50)
print(f"  🐾 PawPal+ — Today's Schedule ({date.today()})")
print("=" * 50)

for task in scheduler.get_sorted_tasks():
    status = "✅" if task.completed else "🔲"
    print(f"  {status} [{task.time}] {task.pet_name}: {task.description}  ({task.frequency})")

# ── Conflict Detection ────────────────────────────────────────────────────────
print("\n--- Conflict Check ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts found.")

# ── Test Recurring Task ───────────────────────────────────────────────────────
print("\n--- Marking 'Morning walk' complete (daily → reschedules) ---")
morning_walk = dog.tasks[1]  # "Morning walk"
scheduler.mark_task_complete(morning_walk)
print(f"  '{morning_walk.description}' completed: {morning_walk.completed}")
print(f"  Buddy now has {len(dog.tasks)} tasks (rescheduled task added)")