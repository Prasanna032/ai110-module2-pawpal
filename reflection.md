# PawPal+ Project Reflection

## 1. System Design
Three core actions a user should be able to perform that I identified are: Assigning a pet to the user, add a pet task like walking, feeding ..etc, and generate a list of tasks or plan for a day.

**a. Initial design**

- Briefly describe your initial UML design.
The initial design is a five-class system centered around an Owner who has one or more Pets and a Scheduler that produces a single combined DailyPlan for the day.

- What classes did you include, and what responsibilities did you assign to each?
Owner — holds the owner's name, how many minutes they have available today, and their preferred start time. Also maintains the list of their pets.
Pet — stores basic info about an animal (name, species, age, notes). A simple data object with no scheduling logic.
Task — represents one care activity (e.g., "Morning Walk"). Tracks which pet it belongs to, how long it takes, its priority, category, and whether it's been completed.
Scheduler — the core logic class. Takes the owner and their tasks, then decides which tasks fit within the available time and in what order, based on priority.
DailyPlan — the output of the scheduler. Holds the final ordered list of scheduled tasks, any skipped tasks, total time used, and methods to display the plan and explain the reasoning

**b. Design changes**

**Did your design change during implementation?**

Yes, several changes were made after reviewing the initial skeleton.

**Changes and reasoning:**

1. Owner relationship to Pet changed from 1-to-1 to 1-to-many. The original design assumed one pet per owner, but a more realistic scenario is that an owner may have multiple pets. This required Owner to hold a List[Pet] instead of a single Pet.

2. Owner now holds the task list instead of Scheduler. Tasks were originally added directly to the scheduler, creating a gap — a task could reference a pet the owner doesn't have. Moving tasks to Owner keeps everything in one place and makes the relationship more consistent.

3. self.schedule was removed from Scheduler. It duplicated DailyPlan.scheduled_tasks, which meant two lists would need to be kept in sync. Removing it and storing the full DailyPlan as self.plan on the scheduler was cleaner.

4. Task.frequency was added. The original design had no way to express how often a task recurs. Adding frequency ("daily", "weekly", "once") makes tasks more realistic and gives the scheduler future room to filter tasks by day.

5. Pet now holds its own task list. Originally Pet was a pure data object with no tasks. Adding tasks and add_task() to Pet means you can ask a pet directly what needs to be done, not just filter through the owner's full list.

6. Owner.add_task() was updated to sync both lists. When a task is added to the owner, it is also added to the relevant pet's task list automatically, so both stay in sync without manual effort.

7. Scheduler gained remove_task() and edit_task(). The original skeleton only supported adding tasks. These two methods complete basic task management — needed for the UI to let users modify their task list after creation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
