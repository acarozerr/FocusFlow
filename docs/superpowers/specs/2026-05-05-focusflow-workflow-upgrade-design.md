# FocusFlow Workflow Upgrade Design

## Goal

Extend FocusFlow from a simple task checklist into a more practical team workflow tool by adding richer task status tracking, a single internal note field, list filtering, and a more informative dashboard.

## Scope

This upgrade adds four connected capabilities:

- Task statuses with four stages: `To Do`, `In Progress`, `Blocked`, `Done`
- A single note field on each task for extra context
- Search and filter controls on the main task board
- Dashboard metrics that reflect the new workflow states

The goal is to improve day-to-day usability without turning the project into a complex project management platform.

Out of scope:

- Multi-comment discussion threads
- File uploads or attachments
- Notifications
- Per-user permissions beyond the current admin/non-admin split
- Full kanban drag-and-drop behavior

## Product Direction

The upgraded version should still feel lightweight and calm, but significantly more useful for real team coordination.

- Statuses make work progress visible
- Notes give a task one extra layer of context without creating a conversation system
- Search and filters reduce scanning friction when the task list grows
- Dashboard summaries help admins identify stalled or blocked work quickly

## Data Model Changes

### Status

Each task will receive a new `status` field with these allowed values:

- `To Do`
- `In Progress`
- `Blocked`
- `Done`

`Done` becomes the canonical completion state.

The existing boolean `completed` field should remain for compatibility with current logic, but it should be synchronized with `status`:

- If status becomes `Done`, `completed` should be `True`
- If status is anything else, `completed` should be `False`

This avoids breaking current templates and views while the app transitions to the new workflow model.

### Note

Each task will receive a new optional `note` field.

- This is a single free-text field
- It is meant for internal task context, not threaded discussion
- It should appear on create and edit surfaces where relevant
- It should appear in task detail presentations only when it contains content

## Task Board Behavior

The main task board should remain the primary landing page, but become more actionable.

### Search and Filters

The board will include:

- Text search
- Status filter
- Priority filter
- Assignee filter

These controls should work together in one query flow rather than as separate disconnected tools.

For non-admin users:

- They should still only see their own assigned tasks
- Filters should apply only within that already-limited task set

For admins:

- They should see all tasks
- Filters should operate across the full task set

### Task Presentation

Task cards should show:

- Title
- Description
- Due date
- Assigned users
- Priority
- Status
- Note preview when present

The visual hierarchy should make `Blocked` and overdue tasks easier to notice than normal tasks.

## Create and Edit Flow

The task form should expand slightly but stay simple.

Admins should be able to set:

- Title
- Description
- Note
- Due date
- Assignees
- Priority
- Status

For new tasks:

- Default status should be `To Do`

The current project does not appear to have a dedicated edit flow. If edit support is added as part of this feature, it should reuse the same form structure rather than introducing a separate form system.

For this iteration, create flow support is required and edit flow support is optional. If edit is not introduced now, the note field only needs to be captured during task creation and displayed afterward.

## Completed and Archive Behavior

The completed tasks page should be driven by `Done` tasks.

- Items with status `Done` should appear there
- Items not marked `Done` should not appear there
- Existing delete behavior can stay the same for now

This keeps the archive view aligned with the new status system.

## Dashboard Changes

The admin dashboard should move from simple totals to workflow-aware summaries.

Recommended top-level metrics:

- Total tasks
- Open tasks
- Done tasks
- Blocked tasks

Recommended secondary summaries:

- Tasks by priority
- Tasks by user
- Tasks by status

Optional lightweight highlights if the implementation stays simple:

- Overdue open task count
- Due today task count

The dashboard should help answer:

- How much work exists?
- How much is finished?
- What is currently blocked?
- Who is carrying the most work?

## Filtering Strategy

The filtering implementation should stay centralized in view logic rather than duplicated in templates.

Recommended behavior:

- Read query parameters from the request
- Build one filtered queryset incrementally
- Reuse that queryset for grouping into sections

This keeps the feature easier to extend later and avoids repeated branching across multiple templates.

## Visual Treatment

The new features should remain inside the existing FocusFlow design language.

- Search and filter controls should feel like part of the same system
- Status badges should be visually distinct
- `Blocked` should stand out clearly without overwhelming the interface
- Notes should read as supporting detail, not primary content

## Migration and Compatibility

Because this changes the task schema, a migration will be required.

Existing tasks should get a safe default:

- Status defaults to `To Do` unless current logic explicitly marks them completed
- Existing completed tasks should map to `Done`
- Existing incomplete tasks should map to `To Do`

This keeps old records usable without manual repair.

## Testing

Verification should cover both model behavior and page behavior.

- Migration applies cleanly
- Existing tasks receive sensible default statuses
- Status and `completed` stay synchronized
- Search works with partial text matches
- Combined filters produce expected subsets
- Non-admin users cannot see tasks outside their own assignments
- Dashboard counts reflect the new workflow states
- Completed page only shows `Done` tasks

## Risks

- Status and `completed` can drift apart if synchronization is not enforced in one place
- Filter logic can become messy if spread across multiple conditional branches
- Dashboard counts may silently disagree if they reuse different query rules
- Template complexity may grow quickly if badges, filters, and note previews are bolted on ad hoc

## Implementation Shape

Expected files include:

- `tasks/models.py`
- `tasks/forms.py`
- `tasks/views.py`
- `tasks/templates/tasks/task_list.html`
- `tasks/templates/tasks/create_task.html`
- `tasks/templates/tasks/completed_tasks.html`
- `tasks/templates/tasks/admin_dashboard.html`
- `tasks/static/tasks/css/style.css.css`
- new migration file under `tasks/migrations/`

The safest implementation order is:

1. Add model fields and migration
2. Update form and synchronization logic
3. Update task list filtering and display
4. Update completed view behavior
5. Upgrade dashboard metrics and summaries
6. Apply final UI polish
