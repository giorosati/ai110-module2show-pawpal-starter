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
