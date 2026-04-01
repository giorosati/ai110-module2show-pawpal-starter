# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - I designed a small domain model with four core classes: `Owner`, `Pet`, `Task`, and `Scheduler`.
  - `Owner` stores owner profile and availability constraints.
  - `Pet` stores pet attributes and special needs.
  - `Task` stores task type (walk, feed, meds, enrichment, grooming), duration, priority, and status.
  - `Scheduler` composes tasks and constraints to produce a prioritized daily plan and explanation text.
- What classes did you include, and what responsibilities did you assign to each?
  - `Owner`: preferences, total daily available time, and any hard constraints.
  - `Pet`: species-dependent care requirements and identifiers.
  - `Task`: task metadata and scheduling properties.
  - `Scheduler`: planning algorithm, constraint enforcement, plan generation, and reasoning output.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
AI suggested this modification:
planned_tasks: Initialized as input list – consider making it a derived property to avoid redundancy.

This modification was implemented to avoid storing unnecessary states. Now the plan will be created on demand.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Constraints: Required vs. optional, time budget, priority, completion status.

The most important constraint is "Required" vs. "Optional". Tasks marked required=True (like medication or feeding) sort to the top of every plan regardless of priority score. A pet missing a walk is inconvenient; a pet missing medication is harmful. This made required the highest-order sort key.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Refactored the generate_plan() method from 56 lines → 22 lines with identical behavior: same sort order, same bin-packing (loop never breaks early), same skipped-task list. This dramatically reduced the complexity and made it easier to read and understand.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI tools in every stage of this project, from the initial design and UML digaram to the final testing and UI edits.
I found the prompts about refactoring to be the most helpful because AI suggested improvements that I did not consider.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
AI made suggested an edit to the UI that I rejected because I did not like the way it would display information to the user. I implemented the suggestion, previewed the result, and reversed the change. Then I followed up with a different prompt to achieve a better result.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The suite contains 21 tests organized into five areas:

- **Happy paths** — all tasks fit within the budget, required tasks are scheduled before optional ones, and `explain_plan` lists both scheduled and skipped tasks.
- **Sorting correctness** — `sort_by_time` returns tasks in chronological order; tasks without a `start_time` are placed at the end.
- **Recurrence logic** — completing a daily task creates a new task due the next day; weekly tasks advance by 7 days; one-off tasks return `None`; unknown IDs raise `ValueError`.
- **Conflict detection** — overlapping tasks produce `CONFLICT` strings; adjacent (non-overlapping) tasks do not; tasks missing `start_time` produce `WARNING` strings; a clean schedule returns an empty list.
- **Edge cases** — pet with no tasks, zero-budget owner, task duration exactly equal to budget, duplicate task IDs across pets, and cache invalidation after mutations.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am very confident the scheduler works correctly. Given more time I would test situations involving time changes (daylinght savings time, traversing time zones, times that start before midnight and extend into the next day) as the code is currently not able to handle those situations.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The speed and accuracy of the logic that AI proposed.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would put attention on making the UI better - improved layout, colors, etc. as well as making it responsive for all screen sizes.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
In this experience I found it's ability to do UI design was it's weak point.
