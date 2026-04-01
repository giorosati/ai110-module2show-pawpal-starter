from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Pet:
    name: str
    species: str
    age: int
    needs: Dict[str, str]
    tasks: List[Task]

    def add_need(self, type: str, detail: str):
        """Add a need to the pet's needs dictionary."""
        self.needs[type] = detail

    def is_med_required(self) -> bool:
        """Check if the pet requires medication."""
        return "medication" in self.needs or any("med" in need.lower() for need in self.needs.values())

@dataclass
class Task:
    id: str
    description: str
    type: str
    duration_minutes: int
    priority: int
    required: bool
    frequency: str  # e.g., "daily", "weekly"
    completion_status: bool  # True if completed

    def update_status(self, new_status: bool):
        """Update the completion status of the task."""
        self.completion_status = new_status

    def set_priority(self, level: int):
        """Set the priority level of the task."""
        self.priority = level

class Owner:
    def __init__(self, name: str, available_minutes_per_day: int, preferences: Dict[str, str], constraints: List[str], pets: List[Pet]):
        for pet in pets:
            if not isinstance(pet, Pet):
                raise ValueError("All pets must be Pet instances")
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences = preferences
        self.constraints = constraints
        self.pets = pets

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def set_availability(self, start: str, end: str):
        """Set the owner's available time based on start and end times."""
        # Parse start and end times to calculate available_minutes_per_day
        # For simplicity, assume start/end are in "HH:MM" format
        # This is a placeholder implementation
        pass

    def add_preference(self, key: str, value: str):
        """Add a preference to the owner's preferences."""
        self.preferences[key] = value

class Scheduler:
    def __init__(self, owner: Owner):
        if not isinstance(owner, Owner):
            raise ValueError("owner must be an Owner instance")
        self.owner = owner

    @property
    def planned_tasks(self) -> List[Task]:
        return self.generate_plan()

    def generate_plan(self) -> List[Task]:
        """Generate a prioritized plan of tasks within time constraints."""
        tasks = self.owner.get_all_tasks()
        # Sort by priority descending (higher priority first)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        # Apply time constraint
        total_time = 0
        plan = []
        for task in sorted_tasks:
            if total_time + task.duration_minutes <= self.owner.available_minutes_per_day:
                plan.append(task)
                total_time += task.duration_minutes
        return plan

    def apply_constraints(self):
        """Apply additional constraints to the plan."""
        # Placeholder: could apply additional constraints like preferences
        pass

    def explain_plan(self) -> str:
        """Provide a string explanation of the generated plan."""
        plan = self.planned_tasks
        if not plan:
            return "No tasks can be scheduled within available time."
        explanation = "Scheduled tasks (prioritized):\n"
        for task in plan:
            pet_name = "Unknown"
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break
            explanation += f"- {task.description} for {pet_name} ({task.duration_minutes} min, priority {task.priority})\n"
        return explanation

    def add_task(self, task: Task, pet_name: str):
        """Add a task to a specific pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                pet.tasks.append(task)
                break

    def remove_task(self, task_id: str):
        """Remove a task by ID from all pets."""
        for pet in self.owner.pets:
            pet.tasks = [t for t in pet.tasks if t.id != task_id]