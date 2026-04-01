from pawpal_system import Owner, Pet, Task, Scheduler

# Tasks added intentionally out of time order to demonstrate sort_by_time
task1 = Task(
    id="1",
    description="Evening walk",
    type="exercise",
    duration_minutes=30,
    priority=5,
    required=True,
    frequency="daily",
    completion_status=False,
    start_time="18:00"
)

task2 = Task(
    id="2",
    description="Feed breakfast",
    type="feeding",
    duration_minutes=10,
    priority=4,
    required=True,
    frequency="daily",
    completion_status=True,   # already done
    start_time="07:30"
)

task3 = Task(
    id="3",
    description="Administer medication",
    type="health",
    duration_minutes=5,
    priority=5,
    required=True,
    frequency="daily",
    completion_status=False,
    start_time="12:00"
)

task4 = Task(
    id="4",
    description="Afternoon playtime",
    type="play",
    duration_minutes=20,
    priority=3,
    required=False,
    frequency="daily",
    completion_status=False,
    start_time="14:30"
)

task5 = Task(
    id="5",
    description="Morning grooming",
    type="hygiene",
    duration_minutes=15,
    priority=2,
    required=False,
    frequency="daily",
    completion_status=True,   # already done
    start_time="09:00"
)

# Create pets
pet1 = Pet(
    name="Buddy",
    species="Dog",
    age=3,
    needs={"exercise": "high", "medication": "daily"},
    tasks=[task1, task2, task4]   # added out of time order
)

pet2 = Pet(
    name="Whiskers",
    species="Cat",
    age=2,
    needs={"grooming": "weekly"},
    tasks=[task3, task5]          # added out of time order
)

# Create owner and scheduler
owner = Owner(
    name="John Doe",
    available_minutes_per_day=60,
    preferences={"morning": "preferred"},
    constraints=["no evening tasks"],
    pets=[pet1, pet2]
)

scheduler = Scheduler(owner)

# ── Sort by time ──────────────────────────────────────────────────────────────
all_tasks = owner.get_all_tasks()
sorted_tasks = scheduler.sort_by_time(all_tasks)

print("=== All tasks sorted by start time ===")
for t in sorted_tasks:
    time_label = t.start_time if t.start_time else "(no time)"
    status = "done" if t.completion_status else "pending"
    print(f"  {time_label}  {t.description} [{status}]")

# ── Filter: incomplete tasks only ─────────────────────────────────────────────
print("\n=== Incomplete tasks (still to do today) ===")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.description}")

# ── Filter: completed tasks only ─────────────────────────────────────────────
print("\n=== Completed tasks (already done) ===")
for t in scheduler.filter_tasks(completed=True):
    print(f"  {t.description}")

# ── Filter: tasks for Buddy only ─────────────────────────────────────────────
print("\n=== Buddy's tasks ===")
for t in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {t.description}")

# ── Filter: Whiskers' incomplete tasks ───────────────────────────────────────
print("\n=== Whiskers' incomplete tasks ===")
for t in scheduler.filter_tasks(pet_name="Whiskers", completed=False):
    print(f"  {t.description}")

# ── Full schedule explanation ─────────────────────────────────────────────────
print("\n=== Today's Schedule ===")
print(scheduler.explain_plan())

# ── Conflict detection ────────────────────────────────────────────────────────
# Add two tasks that intentionally overlap to test conflict detection.
# Evening walk runs 18:00–18:30 (30 min). These two new tasks overlap it:
#   - "Post-walk treat" for Buddy starts at 18:15 (same pet, overlaps by 15 min)
#   - "Whiskers dinner" for Whiskers starts at 18:20 (different pet, overlaps by 10 min)
# A third task has no start_time to verify the untimed-task warning.

conflict_task1 = Task(
    id="7",
    description="Post-walk treat",
    type="feeding",
    duration_minutes=10,
    priority=3,
    required=False,
    frequency="daily",
    completion_status=False,
    start_time="18:15",   # overlaps Evening walk (18:00–18:30)
)
conflict_task2 = Task(
    id="8",
    description="Whiskers dinner",
    type="feeding",
    duration_minutes=15,
    priority=4,
    required=True,
    frequency="daily",
    completion_status=False,
    start_time="18:20",   # overlaps both above tasks
)
no_time_task = Task(
    id="9",
    description="Free-form play",
    type="play",
    duration_minutes=10,
    priority=2,
    required=False,
    frequency="daily",
    completion_status=False,
    start_time=None,      # no time — should trigger untimed warning
)

scheduler.add_task(conflict_task1, "Buddy")
scheduler.add_task(conflict_task2, "Whiskers")
scheduler.add_task(no_time_task, "Buddy")

print("=== Conflict Detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for msg in conflicts:
        print(f"  {msg}")
else:
    print("  No conflicts found.")

print()

# ── Recurring task demo ───────────────────────────────────────────────────────
print("=== Marking tasks complete and auto-scheduling next occurrence ===")

# Mark the daily "Administer medication" complete
next_med = scheduler.mark_task_complete("3")
if next_med:
    print(f"  'Administer medication' marked done.")
    print(f"  Next occurrence created: '{next_med.description}' due {next_med.due_date} (id: {next_med.id})")

# Add and mark a weekly task complete to show timedelta(weeks=1)
weekly_task = Task(
    id="6",
    description="Flea treatment",
    type="health",
    duration_minutes=10,
    priority=4,
    required=True,
    frequency="weekly",
    completion_status=False,
    start_time="10:00",
)
scheduler.add_task(weekly_task, "Buddy")
next_flea = scheduler.mark_task_complete("6")
if next_flea:
    print(f"\n  'Flea treatment' marked done.")
    print(f"  Next occurrence created: '{next_flea.description}' due {next_flea.due_date} (id: {next_flea.id})")

# Confirm new tasks appear in Buddy's incomplete filter
print("\n  Buddy's pending tasks after completions:")
for t in scheduler.filter_tasks(pet_name="Buddy", completed=False):
    due = f" (due {t.due_date})" if t.due_date else ""
    print(f"    - {t.description}{due}")
