# PawPal+ UI To-Do

Missing UI elements identified by comparing `app.py` against the backend in `pawpal_system.py`.

---

## 1. Owner time budget input
The owner is hardcoded to `available_minutes_per_day=60` with no way to change it.
`set_availability(start, end)` already exists — wire it up with two `st.time_input` widgets
or a `st.slider`.

---

## 2. Missing task fields in the "Add task" form
Three task fields are silently hardcoded and never exposed:

| Field | Hardcoded value | Suggested widget |
|---|---|---|
| `required` | always `True` | checkbox "Required?" |
| `frequency` | always `"daily"` | selectbox: daily / weekly / once |
| `start_time` | always `None` | time picker (optional) |

Without `start_time`, every task triggers a WARNING in conflict detection and
`sort_by_time` has nothing to sort on.

---

## 3. No "Mark complete" button
`scheduler.mark_task_complete(task_id)` exists and auto-creates the next recurrence,
but there is no button in the UI to call it. The task table shows tasks but nothing
lets the user check one off.

---

## 4. Conflict detection is never shown
`detect_conflicts()` is fully implemented but never called. Display `st.warning(...)`
for each conflict string returned, right below "Generate schedule".

---

## 5. Scheduler not persisted in session state
A fresh `Scheduler(st.session_state.owner)` is created on every button press.
Tasks added via `scheduler.add_task()` on one press are gone on the next.
Store the scheduler in `st.session_state.scheduler` and only re-create it when
the owner changes.

---

## 6. No task filter controls
`scheduler.filter_tasks(pet_name, completed)` exists but the UI has no way to show
only incomplete tasks or tasks for a specific pet.

---

## Suggested layout

```
Sidebar
└── Owner setup (name + availability window)

Main area
├── Pets panel (add pet, list pets)
├── Add Task form
│   ├── title, duration, priority          ← already there
│   ├── required checkbox                  ← missing
│   ├── frequency selectbox                ← missing
│   └── start time picker (optional)       ← missing
├── Task table
│   ├── filter by pet / show incomplete    ← missing
│   └── "Mark complete" button per row     ← missing
└── Schedule panel
    ├── Generate schedule                  ← already there
    ├── Sort by time display               ← missing
    └── Conflict warnings                  ← missing
```
