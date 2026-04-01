from pawpal_system import Owner, Pet, Task, Scheduler

# Create tasks
task1 = Task(
    id="1",
    description="Morning walk",
    type="exercise",
    duration_minutes=30,
    priority=5,
    required=True,
    frequency="daily",
    completion_status=False
)

task2 = Task(
    id="2",
    description="Feed breakfast",
    type="feeding",
    duration_minutes=10,
    priority=4,
    required=True,
    frequency="daily",
    completion_status=False
)

task3 = Task(
    id="3",
    description="Administer medication",
    type="health",
    duration_minutes=5,
    priority=5,
    required=True,
    frequency="daily",
    completion_status=False
)

# Create pets
pet1 = Pet(
    name="Buddy",
    species="Dog",
    age=3,
    needs={"exercise": "high", "medication": "daily"},
    tasks=[task1, task2]
)

pet2 = Pet(
    name="Whiskers",
    species="Cat",
    age=2,
    needs={"grooming": "weekly"},
    tasks=[task3]
)

# Create owner
owner = Owner(
    name="John Doe",
    available_minutes_per_day=60,  # 1 hour
    preferences={"morning": "preferred"},
    constraints=["no evening tasks"],
    pets=[pet1, pet2]
)

# Create scheduler
scheduler = Scheduler(owner)

# Print today's schedule
print("Today's Schedule:")
print(scheduler.explain_plan())