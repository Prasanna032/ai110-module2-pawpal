from pawpal_system import Owner, Pet, Task


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status"""
    pet = Pet(name="Puppy", species="dog", age=3)
    task = Task(title="Morning Walk", pet=pet, duration_minutes=30, priority="high", category="walk")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count"""
    owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00")
    pet = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(pet)

    assert len(pet.tasks) == 0

    task = Task(title="Feed Luna", pet=pet, duration_minutes=10, priority="high", category="feeding")
    owner.add_task(task)

    assert len(pet.tasks) == 1
