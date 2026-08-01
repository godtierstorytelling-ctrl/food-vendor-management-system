# Lessons Learned

## Overview

The Food Vendor Management System became one of the most educational projects in my software-development coursework.

The application itself required object-oriented programming, relational database operations, input validation, file generation, authentication, unit testing, and integration testing.

However, the most valuable learning occurred during debugging.

The project demonstrated that building software is not simply a matter of writing code. It requires interpreting requirements, coordinating components, understanding dependencies, validating assumptions, and systematically investigating failures.

---

# 1. Clear Requirements Are Part of the Architecture

One of the most important lessons was that unclear requirements create problems far beyond the planning stage.

If a method's inputs, outputs, dependencies, or expected side effects are not clearly defined, developers may create implementations that are logically correct but incompatible with the environment in which they execute.

This project included methods that depended on:

- A live database connection
- A specific user-object type
- Previously initialized tables
- A particular method-call sequence
- Shared state between classes

When those assumptions were not explicit, debugging became significantly more difficult.

The experience reinforced that requirements gathering should define not only what a feature does, but also:

- Who owns each dependency
- Which object initializes shared resources
- What each method receives
- What each method returns
- What state each method changes
- How errors should be handled

---

# 2. Working Locally Does Not Guarantee Environmental Compatibility

The completed application worked locally through unit tests, integration tests, and full command-line workflows.

However, some methods behaved differently under an external automated grading environment.

The difference was often not the business logic itself. It was the way objects and database dependencies were initialized or passed to methods.

This taught me to distinguish between:

```text
The code is incorrect.
```

and:

```text
The code and execution environment disagree about an interface contract.
```

That distinction is essential in professional development.

Similar issues can occur when code moves between:

- Local machines
- Continuous-integration environments
- Containers
- Development servers
- Staging environments
- Production environments
- Third-party APIs
- Automated test harnesses

Environmental assumptions must therefore be documented and tested explicitly.

---

# 3. Debugging Should Be Treated as an Experiment

Early in the debugging process, it was tempting to change several things at once.

That approach made it difficult to determine which change affected the result.

The process became more effective when I began treating each debugging attempt as a controlled experiment:

1. Form a specific hypothesis.
2. Change one thing.
3. Run the test.
4. Observe whether the result changed.
5. Record the outcome.
6. Restore the previous version when necessary.
7. Form the next hypothesis.

This approach converted vague runtime errors into useful evidence.

For example, a change from:

```text
ERROR
```

to:

```text
FAIL
```

revealed that a method could now execute, even if its output was still incorrect.

That distinction helped isolate whether a problem involved:

- Method discovery
- Method signatures
- Input handling
- Database access
- Return values
- Expected side effects

---

# 4. Preserve a Known-Good Version

One of the most valuable process improvements was preserving a stable checkpoint.

Once multiple methods passed, I created and protected a known-good version rather than continuing to edit every file freely.

This made it possible to:

- Protect working functionality
- Compare experimental versions
- Roll back unsuccessful changes
- Avoid introducing regressions
- Isolate remaining failures

The practice mirrors source-control workflows used in professional engineering teams.

A stable branch or release candidate should remain protected while experimental work occurs elsewhere.

---

# 5. Unit Tests and Integration Tests Solve Different Problems

Unit testing helped verify individual behaviors, including:

- Table creation
- Record insertion
- Record retrieval
- Profile updates
- Price updates
- Receipt creation
- Login validation

However, methods that passed independently could still fail when connected.

Integration testing exposed issues involving:

- Database ownership
- Object state
- Method signatures
- Menu routing
- User-profile persistence
- Receipt history
- Reward calculations
- Application-loop behavior

For example:

```text
member_menu()
→ order_food()
→ create_receipt()
→ DbManager
```

required several individually working components to share the same database and user state correctly.

This reinforced that unit tests answer:

```text
Does this component work independently?
```

while integration tests answer:

```text
Do these components work together?
```

Both are necessary.

---

# 6. Database Ownership Must Be Explicit

The most persistent technical challenge involved determining which object owned or received the active database connection.

Locally, the application stored the database manager in the `FoodVendor` object:

```python
self.db = database
```

Some user-related methods also accepted a database object as a parameter.

This produced several possible access patterns:

```python
self.db
database
active_db
```

The application could work locally while still encountering problems if another environment called a method without establishing the same database context.

The primary lesson was that dependencies should be consistent.

A future design would choose one clear approach:

- Constructor injection
- Method injection
- A service layer
- A repository layer
- Dependency injection through a framework

Mixing several approaches makes interfaces harder to reason about and test.

---

# 7. Database Mutations Require Special Verification

Read operations and update operations were often easier to validate because the resulting values could be queried directly.

Insert and delete operations were more difficult under the external grader because successful execution did not always mean the grader observed the same database state.

This reinforced the importance of verifying database mutations through independent queries.

For an insertion:

```sql
SELECT *
FROM menu
WHERE item_name = ?;
```

For a deletion:

```sql
SELECT *
FROM user
WHERE user_name = ?;
```

A mutation should not be considered successful merely because no exception was raised.

The resulting database state must also be confirmed.

---

# 8. Interfaces Matter More Than Internal Cleverness

Several methods were individually logical but depended on specific calling conventions.

A method may expect:

```python
method(database)
```

while an external system expects:

```python
method()
```

Both implementations may make sense in isolation, but the mismatch prevents integration.

This project reinforced the importance of stable method contracts:

- Method name
- Parameters
- Optional parameters
- Return type
- Side effects
- Exceptions
- Required object state

A clear interface is often more valuable than a clever internal implementation.

---

# 9. Refactoring Should Wait Until Behavior Is Stable

During debugging, it was tempting to clean up formatting, consolidate logic, rename variables, or redesign method signatures.

However, refactoring during active debugging can introduce new variables into the investigation.

The safer sequence is:

1. Make the behavior correct.
2. Verify it with tests.
3. Preserve a stable version.
4. Refactor in a separate pass.
5. Run regression tests.

This lesson helped prevent working code from being unintentionally destabilized.

---

# 10. Error Messages Are Evidence, Even When They Are Vague

The automated grader often returned only:

```text
runtime error
```

without a traceback.

Although frustrating, the type of result still provided evidence.

### `ERROR`

Suggested that:

- The method crashed
- The grader could not call the method
- A dependency was missing
- The test harness encountered an exception

### `FAIL`

Suggested that:

- The method executed
- The result or side effect did not match expectations

### `PASS`

Confirmed that:

- The method executed
- The grader observed the expected result

Learning to interpret these categories helped turn an opaque environment into a limited but useful diagnostic system.

---

# 11. The Application Should Be Tested as a Complete System

After method-level testing, I ran full application workflows directly through:

```bash
python3 FoodVendor.py
```

The tested journeys included:

## Guest journey

```text
Main Menu
→ Guest Order
→ Select Category
→ Select Item
→ Select Side Option
→ Checkout
→ Enter Payment Information
→ Generate Receipt
→ Return to Main Menu
→ Exit
```

## Customer journey

```text
Main Menu
→ Customer Login
→ Member Menu
→ Logout
→ Return to Main Menu
→ Exit
```

## Administrator journey

```text
Main Menu
→ Administrator Login
→ Admin Menu
→ Logout
→ Return to Main Menu
→ Exit
```

These tests confirmed that the application worked as a connected system rather than only as a collection of isolated methods.

---

# 12. Documentation Is Part of Shipping

The original project was developed as a capstone assignment.

Transforming it into a portfolio project required additional work:

- Organizing the repository
- Creating a professional README
- Explaining the architecture
- Documenting the database schema
- Recording limitations
- Describing the testing strategy
- Identifying future improvements
- Writing this lessons-learned review

This process showed that software is not fully shipped when the code merely runs.

A project becomes easier to evaluate, maintain, and extend when its design and decisions are documented.

---

# 13. Time-Boxing Is an Engineering Skill

The project also reinforced the importance of evaluating debugging effort against expected value.

At some point, continuing to investigate an opaque external grader produced diminishing returns.

The application was functional locally, the major workflows were tested, and the academic outcome was already strong.

That created a legitimate engineering decision:

```text
Is another hour of debugging the highest-value use of time?
```

Professional development teams make similar decisions when evaluating:

- Low-priority bugs
- Edge cases
- Technical debt
- Release deadlines
- Opportunity cost
- Product value

Choosing to stop after sufficient validation is not the same as giving up.

It is often a rational delivery decision.

---

# 14. The Most Important Outcome Was the Process

The greatest value of this project was not the food-ordering domain.

It was learning how to:

- Read and understand a multi-file program
- Trace data through multiple classes
- Design and query a relational database
- Use inheritance
- Build CRUD functionality
- Test individual methods
- Test integrated workflows
- Generate output files
- Preserve application state
- Debug hidden dependencies
- Document architectural decisions
- Evaluate effort against business value

The project marked a transition from practicing Python syntax to thinking more broadly about software engineering systems.

---

# What I Would Change in a Future Version

A future implementation would include:

- Persistent database storage
- Constructor-based dependency injection
- Dedicated service and repository layers
- Formal automated testing with `pytest`
- Test fixtures
- Mocked database dependencies
- Custom exceptions
- Structured logging
- Secure password hashing
- Tokenized or externalized payment handling
- Normalized order and order-item tables
- Full order history
- Web-based frontend
- REST API
- Deployment pipeline
- Continuous integration

---

# Connection to Future Projects

The Food Vendor Management System serves as a foundation for future CRUD applications.

The next project in this progression is a timeline-management system for writers.

Many concepts transfer directly:

| Food Vendor System | Timeline System |
|---|---|
| Customer | Writer |
| Menu item | Timeline event |
| Menu category | Plotline or character track |
| Order | Timeline arrangement |
| Receipt | Timeline export |
| User profile | Writer profile |
| Administrator tools | Project-management tools |
| SQLite records | Story-development records |

The domain changes, but the core engineering skills remain:

- Modeling data
- Managing users
- Creating and updating records
- Validating input
- Connecting application logic to persistence
- Testing complete workflows

The Food Vendor project therefore represents both a completed application and the starting point for more advanced full-stack development.
