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