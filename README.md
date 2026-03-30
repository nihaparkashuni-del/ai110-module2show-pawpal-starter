# 🐾 PawPal+

PawPal+ is a pet care management app I built using Python and Streamlit. It helps pet owners keep track of their pets' daily routines like walks, feedings, medications, and vet appointments. The app uses object-oriented programming and some scheduling logic to organize everything automatically.

---

## 📸 Demo

![PawPal App](app_screenshot.png)

---

## ✨ Features

- **Add Pets** — You can add multiple pets with their name, species, and age
- **Schedule Tasks** — Assign tasks to any pet with a specific time and how often it repeats
- **Auto Sorting** — The schedule automatically sorts tasks by time so you always see what's coming up first
- **Filter Tasks** — You can filter by pet or by whether a task is done or still pending
- **Conflict Warnings** — If two tasks for the same pet are at the same time, the app shows a warning
- **Recurring Tasks** — When you complete a daily or weekly task, the next one gets scheduled automatically
- **Persistent UI** — The app remembers your data while you're using it thanks to Streamlit's session state

---

## 🧠 Smarter Scheduling

I added a few algorithms inside the `Scheduler` class to make the app actually useful:

- **Sorting** — I used Python's `sorted()` with a `lambda` to sort tasks by their `HH:MM` time string
- **Conflict Detection** — The scheduler checks every pair of tasks and warns you if two tasks for the same pet overlap at the exact same time
- **Recurring Tasks** — After marking a daily task complete, the code uses `timedelta(days=1)` to create a brand new task for the next day and adds it back automatically
- **Filtering** — You can filter the task list down to just one pet or just pending/completed tasks

---

## 🗂️ Project Structure

```
ai110-module2show-pawpal-starter/
├── app.py               # Streamlit UI
├── pawpal_system.py     # All the backend classes (Task, Pet, Owner, Scheduler)
├── main.py              # CLI script I used to test the logic in the terminal
├── tests/
│   └── test_pawpal.py   # pytest tests
├── uml_final.png        # UML class diagram
├── uml_final.md         # Mermaid.js code for the diagram
├── reflection.md        # My reflection on the project
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## ⚙️ How to Run It

```bash
# 1. Clone the repo
git clone https://github.com/nihaparkashuni-del/ai110-module2show-pawpal-starter.git
cd ai110-module2show-pawpal-starter

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install streamlit pytest

# 4. Run the app
streamlit run app.py
```

---

## 🧪 Testing

To run all the tests:

```bash
python -m pytest tests/ -v
```

Here's what I tested:

- **Task Completion** — checks that `mark_complete()` actually changes the status to `True`
- **Task Addition** — checks that adding a task increases the pet's task count by 1
- **Sorting** — checks that tasks come back in time order (earliest first)
- **Recurrence** — checks that completing a daily task adds a new one for the next day
- **Conflict Detection** — checks that the scheduler catches two tasks at the same time for the same pet

### Confidence Level: ⭐⭐⭐⭐⭐ (5/5)

All 5 tests passed. I feel confident the core logic works correctly.

---

## 🏗️ System Design

The app is built around 4 classes:

- **`Task`** — one activity with a time, frequency, and whether it's done
- **`Pet`** — holds pet info and a list of its tasks
- **`Owner`** — keeps track of all the pets
- **`Scheduler`** — does all the smart stuff: sorting, filtering, conflict checking, and rescheduling

Check out `uml_final.png` to see how they all connect.