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

--What constraints does your scheduler consider?

The scheduler considers three constraints:

1. **Available time** — the owner specifies how many minutes they have today. The scheduler will not add a task if it would exceed that budget.
2. **Task priority** — each task is rated high, medium, or low. The scheduler always attempts high-priority tasks before medium or low ones.
3. **Completion status** — tasks already marked complete are excluded from scheduling entirely, so the same task is never double-scheduled.

--How did you decide which constraints mattered most?

Available time and priority were the obvious starting point — without a time budget the scheduler has no reason to skip anything, and without priority there is no basis for choosing one task over another. Completion status was added because skipping already-done tasks is a correctness requirement, not an optional feature.

**b. Tradeoffs**

-Describe one tradeoff your scheduler makes.
The scheduler uses a greedy strategy. It sorts tasks by priority (high → medium → low) and adds each one as long as it fits within the remaining time. It never looks ahead to check whether a different combination of tasks could fit more total minutes or better satisfy the owner's preferences.

For example, if a 30-minute high-priority task leaves only 5 minutes, three 5-minute medium-priority tasks would all be skipped, even though fitting two of them instead might serve the owner better overall.

-Why is that tradeoff reasonable for this scenario?
For a daily pet care planner, correctness and simplicity matter more than mathematical optimality. High-priority tasks like medication or feeding must always come first, the owner should never wonder whether a "walk" bumped out "give supplements." A greedy approach is also easier to explain to the user ("we scheduled your most important tasks first") and easier to debug and test. A fully optimal scheduler (e.g. using dynamic programming or backtracking) would add significant complexity for a marginal real-world benefit in this context.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I colloborated with AI for most parts of the project in three main ways. During design, I asked it to review my initial UML and flag anything that looked inconsistent or incomplete. It pointed out that Owner holding tasks instead of Scheduler was a cleaner relationship, which I adopted. During implementation, I used it to suggest small algorithm improvements, like filtering completed tasks before scheduling and adding plain-language conflict warnings instead of technical strings. During testing, I asked it to generate a list of edge cases I might have missed (such as "all tasks already completed" or "two tasks at the exact same start time"), which I then used to write the test suite.

- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific and tied to the code: "review generate_schedule and list what it ignores" was more useful than "how do I make a scheduler." Asking it to explain a tradeoff ("why is greedy reasonable here?") also helped me write the reasoning in section 2b above.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When AI suggested rewriting the entire app.py file to add new features, I rejected that approach. A full rewrite would have removed the Scenario and "What you need to build" expanders that were part of the original project structure. Instead I asked it to use targeted edits only, adding new sections without touching existing content. 

- How did you evaluate or verify what the AI suggested?
I verified by reading the diff before accepting each change and checking that the expanders were still present after each edit.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Eight behaviors were tested in `tests/test_pawpal.py`:
1. `mark_complete()` flips `task.completed` to `True`
2. Adding a task via the owner syncs it to the pet's task list
3. `sort_by_time()` returns tasks in chronological order by start time
4. Completing a `daily` task creates a new task due the following day
5. Completing a `once` task returns `None` and adds no new task
6. Two tasks at the same start time produce exactly one conflict warning
7. Tasks with a gap between them produce no conflict warnings
8. Already-completed tasks are excluded from the generated schedule

- Why were these tests important?
These tests mattered because they cover the three behaviors most likely to go wrong in real use: sorting (which the UI depends on for display), recurrence (which involves date math), and conflict detection.

**b. Confidence**

- How confident are you that your scheduler works correctly?
4 / 5 — the core scheduling behaviors are tested and working. Confidence is not higher because the greedy algorithm's optimality is not tested (only that it runs), edge cases like zero available minutes or all tasks exceeding the time budget are not covered, and there are no tests for the Streamlit UI layer. 

- What edge cases would you test next if you had more time?
If I had more time I would test: owner with 0 available minutes (all tasks skipped), a single task whose duration exactly equals available time (boundary condition on `<=`), and calling `complete_task()` twice on the same daily task to confirm it does not create duplicate next occurrences.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part I am most satisfied with is the recurrence logic in `complete_task()`. It is clean, easy to read, and handles three distinct cases (daily, weekly, once) with a small amount of code using Python's `timedelta`. It also plugs directly into the UI, marking a task complete immediately shows the next due date, which makes the feature feel complete rather than just backend logic with no visible effect.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would redesign the scheduling algorithm to be optimally better rather than purely greedy. The current approach can leave significant time unused when a high-priority task is large and the remaining tasks are all too big to fit. A simple look-ahead, after the greedy pass, try to fill remaining minutes with the best-fitting skipped task, would improve real-world usefulness without adding much complexity. I would also add input validation to `edit_task()` so that setting an invalid priority string or a negative duration raises an error immediately rather than silently corrupting task data.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The most important thing I learned is that a good system design makes testing and UI integration straightforward. Because the Scheduler, Owner, and Task classes each have a single clear responsibility, writing tests was mostly a matter of setting up and asserting one thing. When I needed to add a feature to the UI, the method already existed in the backend, I just had to call it. Starting from a UML diagram and refining it before writing code made that possible.
