# PawPal+ Reflection

---

## Section 1: System Design

### Three Core Actions a User Should Be Able to Perform

1. **Add a pet** — the user should be able to register their pet with a name, species, and age so the app knows who to schedule tasks for
2. **Schedule a task** — the user should be able to assign an activity like a walk or feeding to a specific pet with a time and how often it repeats
3. **View today's schedule** — the user should be able to see all tasks sorted by time so they know what needs to be done and in what order

---

### 1a. Initial Design

I designed four main classes for this system:

- **Task** — I chose this because every activity (walk, feeding, medication) is basically one task with a description, a time, a frequency, and a status. Using a dataclass kept it clean.
- **Pet** — Each pet needs to hold its own information and its own list of tasks. I gave it `add_task()` and `get_tasks()` methods so it can manage its own data.
- **Owner** — The owner is the top level. They own all the pets, so I gave them an `add_pet()` method and a way to collect all tasks across every pet with `get_all_tasks()`.
- **Scheduler** — I made this a separate class because I didn't want sorting or conflict logic mixed into the other classes. The Scheduler takes an Owner and does all the smart work on top of the data.

The main relationship is: Owner has many Pets, and each Pet has many Tasks. The Scheduler sits on top and uses the Owner to access everything.

---

### 1b. Design Changes

After thinking through the design more, I added a `reschedule()` method directly on the `Task` class instead of putting that logic in the Scheduler. It made more sense for a Task to know how to create its own next occurrence. The Scheduler just calls it when needed.

I also added a `get_pet_names()` method to Owner because the Streamlit UI needed a list of just the names for the dropdown selector. It was a small addition but it made the UI code a lot cleaner.

---

## Section 2: Algorithmic Layer

### 2a. Algorithms Implemented

**Sorting** — I used Python's `sorted()` function with a lambda key to sort tasks by their time string in `HH:MM` format. Since the format is consistent, string sorting works correctly for chronological order.

**Filtering** — I used list comprehensions to filter tasks by pet name or by completion status. It's simple but effective — one line per filter.

**Conflict Detection** — I used a nested loop to compare every pair of tasks. If two tasks share the same `pet_name` and the same `time`, a warning string gets added to a list and returned. It doesn't crash the app, it just warns the user.

**Recurring Tasks** — When `mark_task_complete()` is called on a daily or weekly task, the Scheduler calls `task.reschedule()` which returns a brand new Task with the due date bumped forward using `timedelta`. That new task gets added to the correct pet's list automatically.

---

### 2b. Tradeoffs

The conflict detection only flags tasks that are scheduled at the **exact same time** (like both at `09:00`). It doesn't catch overlapping durations — for example, if one task runs from 9:00 to 9:30 and another starts at 9:15, the system wouldn't catch that. I made this tradeoff because tasks in this app don't have a duration field, so checking for overlap wasn't possible without redesigning the Task class. For a simple pet care app, exact time matching is good enough.

---

## Section 3: AI Strategy and Reflection

### Which Copilot features were most effective?

The most helpful thing was being able to describe what I wanted in plain English and get working code back quickly. For example when I needed to sort tasks by time, being able to ask "how do I sort by a time string in HH:MM format using a lambda" saved me a lot of time looking things up. The inline suggestions were also helpful for filling in repetitive parts like list comprehensions.

### One example of an AI suggestion I rejected or modified

When I first got the Scheduler skeleton, the AI put the rescheduling logic entirely inside the Scheduler class. I moved it into a `reschedule()` method on the Task class instead because it made more logical sense — a Task should know how to create its next occurrence. Keeping it in the Scheduler would have made that class harder to read and maintain.

### How did using separate chat sessions help?

Keeping the design phase, implementation phase, and testing phase in separate chat sessions helped a lot. If I asked about testing in the same session where I was designing classes, the AI would sometimes mix things up or reference earlier incomplete code. Starting fresh for each phase meant the AI was focused on just that one thing.

### What I learned about being the lead architect

The biggest thing I learned is that AI is really good at writing code but it doesn't always know what your system is supposed to feel like. It can give you something that works but is messy or hard to understand. My job was to look at what it gave me, decide if it made sense for my design, and change it if it didn't. I had to understand the code well enough to catch when something was off — like the rescheduling example above. AI speeds things up a lot but you still have to be the one making the real decisions.