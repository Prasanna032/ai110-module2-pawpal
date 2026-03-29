# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Owner {
        +String name
        +int available_minutes
        +String preferred_start_time
        +List pets
        +List tasks
    }

    class Pet {
        +String name
        +String species
        +int age
        +String notes
        +get_info() str
    }

    class Task {
        +String title
        +Pet pet
        +int duration_minutes
        +String priority
        +String category
        +bool completed
        +mark_complete() None
        +is_high_priority() bool
    }

    class Scheduler {
        +Owner owner
        +DailyPlan plan
        +add_task(task) None
        +generate_schedule(date) DailyPlan
    }

    class DailyPlan {
        +String date
        +List scheduled_tasks
        +List skipped_tasks
        +int total_time_used
        +List reasoning
        +display() str
        +get_summary() str
    }

    Owner "1" --> "many" Pet : owns
    Owner "1" --> "many" Task : has
    Owner "1" --> "1" Scheduler : uses
    Task "many" --> "1" Pet : belongs to
    Scheduler "1" --> "1" DailyPlan : produces
    DailyPlan "1" --> "many" Task : contains
```
