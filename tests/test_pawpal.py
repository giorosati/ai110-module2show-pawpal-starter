import pytest
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Verify that calling update_status(True) changes the task's completion_status to True."""
    task = Task(
        id="test1",
        description="Test task",
        type="test",
        duration_minutes=10,
        priority=3,
        required=False,
        frequency="daily",
        completion_status=False
    )
    assert not task.completion_status
    task.update_status(True)
    assert task.completion_status

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(
        name="TestPet",
        species="Dog",
        age=2,
        needs={},
        tasks=[]
    )
    owner = Owner(
        name="TestOwner",
        available_minutes_per_day=60,
        preferences={},
        constraints=[],
        pets=[pet]
    )
    scheduler = Scheduler(owner)
    initial_count = len(pet.tasks)
    task = Task(
        id="new_task",
        description="New task",
        type="test",
        duration_minutes=5,
        priority=2,
        required=False,
        frequency="daily",
        completion_status=False
    )
    scheduler.add_task(task, pet.name)
    assert len(pet.tasks) == initial_count + 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(id, description, duration, priority, required=False,
              frequency="daily", completed=False, start_time=None):
    return Task(
        id=id,
        description=description,
        type="test",
        duration_minutes=duration,
        priority=priority,
        required=required,
        frequency=frequency,
        completion_status=completed,
        start_time=start_time,
    )


def make_scheduler(tasks, budget=120):
    pet = Pet(name="Rex", species="Dog", age=3, needs={}, tasks=tasks)
    owner = Owner(name="Alex", available_minutes_per_day=budget,
                  preferences={}, constraints=[], pets=[pet])
    return Scheduler(owner)


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------

def test_schedule_all_tasks_fit():
    """All tasks fit within the budget — none are skipped."""
    tasks = [
        make_task("t1", "Walk",  30, priority=3),
        make_task("t2", "Feed",  20, priority=2),
    ]
    scheduler = make_scheduler(tasks, budget=60)
    scheduled, skipped = scheduler.generate_plan()
    assert len(scheduled) == 2
    assert skipped == []


def test_required_tasks_scheduled_before_optional():
    """Required tasks consume budget before optional ones."""
    tasks = [
        make_task("t1", "Optional play",  50, priority=5, required=False),
        make_task("t2", "Required meds",  50, priority=1, required=True),
    ]
    # Budget fits exactly one 50-min task
    scheduler = make_scheduler(tasks, budget=50)
    scheduled, skipped = scheduler.generate_plan()
    assert len(scheduled) == 1
    assert scheduled[0].id == "t2"
    assert len(skipped) == 1
    assert skipped[0].id == "t1"


def test_explain_plan_lists_scheduled_and_skipped():
    """explain_plan output mentions both scheduled and skipped tasks."""
    tasks = [
        make_task("t1", "Walk",  30, priority=3),
        make_task("t2", "Bath",  120, priority=2),
    ]
    scheduler = make_scheduler(tasks, budget=60)
    explanation = scheduler.explain_plan()
    assert "Walk" in explanation
    assert "Bath" in explanation
    assert "Could not schedule" in explanation


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_chronological_order():
    """Tasks are returned sorted earliest to latest start_time."""
    tasks = [
        make_task("t1", "Afternoon walk",  30, priority=1, start_time="13:00"),
        make_task("t2", "Morning feed",    20, priority=1, start_time="08:00"),
        make_task("t3", "Mid-morning med", 15, priority=1, start_time="09:30"),
    ]
    scheduler = make_scheduler(tasks)
    sorted_tasks = scheduler.sort_by_time(tasks)
    times = [t.start_time for t in sorted_tasks]
    assert times == ["08:00", "09:30", "13:00"]


def test_sort_by_time_untimed_tasks_go_last():
    """Tasks without start_time are placed after all timed tasks."""
    tasks = [
        make_task("t1", "Untimed grooming", 20, priority=1, start_time=None),
        make_task("t2", "Morning feed",     20, priority=1, start_time="08:00"),
    ]
    scheduler = make_scheduler(tasks)
    sorted_tasks = scheduler.sort_by_time(tasks)
    assert sorted_tasks[0].start_time == "08:00"
    assert sorted_tasks[1].start_time is None


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_mark_daily_task_complete_creates_next_occurrence():
    """Completing a daily task creates a new task due the following day."""
    from datetime import date, timedelta
    task = make_task("t1", "Walk", 30, priority=3, frequency="daily")
    scheduler = make_scheduler([task])
    next_task = scheduler.mark_task_complete("t1")

    assert next_task is not None
    assert next_task.completion_status is False
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_mark_weekly_task_complete_creates_next_occurrence():
    """Completing a weekly task creates a new task due seven days later."""
    from datetime import date, timedelta
    task = make_task("t1", "Vet checkup", 60, priority=4, frequency="weekly")
    scheduler = make_scheduler([task])
    next_task = scheduler.mark_task_complete("t1")

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(weeks=1)


def test_mark_nonrecurring_task_complete_returns_none():
    """Completing a one-off task returns None (no recurrence created)."""
    task = make_task("t1", "One-time bath", 30, priority=2, frequency="once")
    scheduler = make_scheduler([task])
    result = scheduler.mark_task_complete("t1")
    assert result is None


def test_mark_complete_unknown_id_raises():
    """mark_task_complete raises ValueError for an unknown task ID."""
    scheduler = make_scheduler([])
    with pytest.raises(ValueError):
        scheduler.mark_task_complete("nonexistent")


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_same_start_time():
    """Two tasks starting at the same time are flagged as a CONFLICT."""
    tasks = [
        make_task("t1", "Walk",  30, priority=3, start_time="09:00"),
        make_task("t2", "Feed",  20, priority=2, start_time="09:00"),
    ]
    scheduler = make_scheduler(tasks, budget=120)
    warnings = scheduler.detect_conflicts()
    assert any("CONFLICT" in w for w in warnings)


def test_detect_conflicts_partial_overlap():
    """A task that starts before another ends is flagged as a CONFLICT."""
    tasks = [
        make_task("t1", "Walk",  60, priority=3, start_time="09:00"),  # 09:00–10:00
        make_task("t2", "Feed",  30, priority=2, start_time="09:30"),  # 09:30–10:00
    ]
    scheduler = make_scheduler(tasks, budget=120)
    warnings = scheduler.detect_conflicts()
    assert any("CONFLICT" in w for w in warnings)


def test_no_conflict_when_tasks_are_adjacent():
    """A task ending exactly when the next one starts is NOT a conflict."""
    tasks = [
        make_task("t1", "Walk",  60, priority=3, start_time="08:00"),  # 08:00–09:00
        make_task("t2", "Feed",  30, priority=2, start_time="09:00"),  # 09:00–09:30
    ]
    scheduler = make_scheduler(tasks, budget=120)
    warnings = scheduler.detect_conflicts()
    assert not any("CONFLICT" in w for w in warnings)


def test_detect_conflicts_warning_for_untimed_task():
    """A scheduled task without start_time produces a WARNING entry."""
    tasks = [
        make_task("t1", "Untimed grooming", 30, priority=2, start_time=None),
    ]
    scheduler = make_scheduler(tasks, budget=120)
    warnings = scheduler.detect_conflicts()
    assert any("WARNING" in w for w in warnings)


def test_no_conflicts_clean_schedule():
    """Non-overlapping timed tasks return an empty conflict list."""
    tasks = [
        make_task("t1", "Walk",  30, priority=3, start_time="08:00"),  # 08:00–08:30
        make_task("t2", "Feed",  20, priority=2, start_time="09:00"),  # 09:00–09:20
    ]
    scheduler = make_scheduler(tasks, budget=120)
    assert scheduler.detect_conflicts() == []


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks_produces_empty_plan():
    """An owner whose pet has zero tasks results in an empty schedule."""
    scheduler = make_scheduler([], budget=120)
    scheduled, skipped = scheduler.generate_plan()
    assert scheduled == []
    assert skipped == []


def test_zero_budget_skips_all_tasks():
    """With 0 available minutes every task lands in skipped."""
    tasks = [make_task("t1", "Walk", 30, priority=3)]
    scheduler = make_scheduler(tasks, budget=0)
    scheduled, skipped = scheduler.generate_plan()
    assert scheduled == []
    assert len(skipped) == 1


def test_task_duration_exactly_equals_budget():
    """A single task whose duration equals the budget is scheduled, not skipped."""
    tasks = [make_task("t1", "Long walk", 60, priority=3)]
    scheduler = make_scheduler(tasks, budget=60)
    scheduled, skipped = scheduler.generate_plan()
    assert len(scheduled) == 1
    assert skipped == []


def test_duplicate_task_ids_deduplicated():
    """The same task ID on two pets is only scheduled once."""
    shared_task_id = "shared"
    pet1 = Pet(name="Rex",   species="Dog", age=3, needs={},
               tasks=[make_task(shared_task_id, "Walk", 30, priority=3)])
    pet2 = Pet(name="Bella", species="Cat", age=2, needs={},
               tasks=[make_task(shared_task_id, "Walk", 30, priority=3)])
    owner = Owner(name="Alex", available_minutes_per_day=120,
                  preferences={}, constraints=[], pets=[pet1, pet2])
    all_tasks = owner.get_all_tasks()
    ids = [t.id for t in all_tasks]
    assert ids.count(shared_task_id) == 1


def test_cache_invalidated_after_add_task():
    """planned_tasks reflects a newly added task after add_task is called."""
    scheduler = make_scheduler([], budget=120)
    assert scheduler.planned_tasks == []

    new_task = make_task("t1", "Walk", 30, priority=3)
    scheduler.add_task(new_task, "Rex")
    assert any(t.id == "t1" for t in scheduler.planned_tasks)