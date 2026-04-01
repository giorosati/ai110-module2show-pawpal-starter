from typing import Dict, List

class Owner:
    def __init__(self, name: str, available_minutes_per_day: int, preferences: Dict[str, str], constraints: List[str]):
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences = preferences
        self.constraints = constraints

    def set_availability(self, start: str, end: str):
        pass

    def add_preference(self, key: str, value: str):
        pass

class Pet:
    def __init__(self, name: str, species: str, age: int, needs: Dict[str, str]):
        self.name = name
        self.species = species
        self.age = age
        self.needs = needs

    def add_need(self, type: str, detail: str):
        pass

    def is_med_required(self) -> bool:
        pass

class Task:
    def __init__(self, id: str, title: str, type: str, duration_minutes: int, priority: int, required: bool, status: str):
        self.id = id
        self.title = title
        self.type = type
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.required = required
        self.status = status

    def update_status(self, new_status: str):
        pass

    def set_priority(self, level: int):
        pass

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task], planned_tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.planned_tasks = planned_tasks

    def generate_plan(self):
        pass

    def apply_constraints(self):
        pass

    def explain_plan(self):
        pass

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_id: str):
        pass