# FocusFlow Workflow Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add workflow-aware task statuses, a single note field, search/filter controls, and a richer admin dashboard to FocusFlow.

**Architecture:** Extend the existing `Task` model with minimal schema changes, keep the current admin/non-admin permission split, and centralize filtering in `tasks/views.py`. Reuse the current create form and FocusFlow templates instead of introducing new pages or a separate filtering layer.

**Tech Stack:** Django models, migrations, Django forms, Django TestCase, Bootstrap-based Django templates, app-scoped CSS

---

## File Structure

- Modify: `tasks/models.py`
  Responsibility: add workflow fields and status/completion synchronization helpers
- Modify: `tasks/forms.py`
  Responsibility: expose `note` and `status` in the task form with FocusFlow styling
- Modify: `tasks/views.py`
  Responsibility: centralize filtered queryset construction, update completed/archive logic, expand dashboard metrics
- Modify: `tasks/templates/tasks/task_list.html`
  Responsibility: render filter controls, status badges, note preview, overdue emphasis
- Modify: `tasks/templates/tasks/create_task.html`
  Responsibility: expose status and note inputs in the create flow
- Modify: `tasks/templates/tasks/completed_tasks.html`
  Responsibility: align archive view with `Done` status
- Modify: `tasks/templates/tasks/admin_dashboard.html`
  Responsibility: add workflow-aware summary cards and status breakdown
- Modify: `tasks/static/tasks/css/style.css.css`
  Responsibility: style filters, status badges, note blocks, overdue treatment, dashboard additions
- Modify: `tasks/tests.py`
  Responsibility: cover model synchronization, filtering behavior, non-admin visibility, completed page, dashboard metrics
- Create: `tasks/migrations/<new_migration>.py`
  Responsibility: add `status` and `note` fields and migrate existing data safely

### Task 1: Add workflow fields and model tests

**Files:**
- Modify: `tasks/models.py`
- Modify: `tasks/tests.py`
- Create: `tasks/migrations/<new_migration>.py`

- [ ] **Step 1: Write failing model tests for status synchronization and display helpers**

Add tests covering:

```python
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Task


class TaskModelTests(TestCase):
    def test_done_status_sets_completed_true(self):
        task = Task.objects.create(
            title="Ship release",
            description="Prepare release notes",
            due_date=date(2026, 5, 6),
            status="Done",
        )
        self.assertTrue(task.completed)

    def test_non_done_status_sets_completed_false(self):
        task = Task.objects.create(
            title="Investigate issue",
            description="Check blocker",
            due_date=date(2026, 5, 6),
            completed=True,
            status="Blocked",
        )
        self.assertFalse(task.completed)

    def test_formatted_assignees_capitalizes_names(self):
        first = User.objects.create_user(username="ozer")
        second = User.objects.create_user(username="peker")
        task = Task.objects.create(
            title="Plan sprint",
            description="Create sprint outline",
            due_date=date(2026, 5, 6),
        )
        task.assigned_to.set([first, second])
        self.assertEqual(task.formatted_assignees(), "Ozer, Peker")
```

- [ ] **Step 2: Run model tests to verify they fail before implementation**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskModelTests`
Expected: FAIL because `status` does not exist yet

- [ ] **Step 3: Implement `status`, `note`, and synchronization in `tasks/models.py`**

Add:

```python
class Task(models.Model):
    STATUS_TODO = "To Do"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_BLOCKED = "Blocked"
    STATUS_DONE = "Done"
    STATUS_CHOICES = [
        (STATUS_TODO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_BLOCKED, "Blocked"),
        (STATUS_DONE, "Done"),
    ]
```

And fields:

```python
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
```

Then synchronize in `save()`:

```python
    def save(self, *args, **kwargs):
        self.completed = self.status == self.STATUS_DONE
        super().save(*args, **kwargs)
```

And keep helper methods:

```python
    def is_overdue(self):
        return not self.completed and self.due_date < timezone.localdate()

    def status_badge_class(self):
        return {
            self.STATUS_TODO: "todo",
            self.STATUS_IN_PROGRESS: "progress",
            self.STATUS_BLOCKED: "blocked",
            self.STATUS_DONE: "done",
        }.get(self.status, "todo")
```

- [ ] **Step 4: Generate and inspect the migration**

Run: `source .venv/bin/activate && python manage.py makemigrations tasks`
Expected: new migration adds `note` and `status`

Then edit the migration so existing rows map safely:

```python
def seed_task_status(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    for task in Task.objects.all():
        task.status = "Done" if task.completed else "To Do"
        task.save(update_fields=["status"])
```

- [ ] **Step 5: Re-run the model tests to verify they pass**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskModelTests`
Expected: PASS

### Task 2: Add form support for status and note

**Files:**
- Modify: `tasks/forms.py`
- Modify: `tasks/templates/tasks/create_task.html`
- Modify: `tasks/tests.py`

- [ ] **Step 1: Write a failing form test for status and note fields**

Add:

```python
from .forms import TaskForm


class TaskFormTests(TestCase):
    def test_task_form_exposes_note_and_status(self):
        form = TaskForm()
        self.assertIn("note", form.fields)
        self.assertIn("status", form.fields)
        self.assertEqual(form.fields["status"].initial or Task.STATUS_TODO, Task.STATUS_TODO)
```

- [ ] **Step 2: Run the form test to verify it fails first**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskFormTests`
Expected: FAIL because the form does not yet include `note` and `status`

- [ ] **Step 3: Update `tasks/forms.py` to expose the new workflow fields**

Set:

```python
        fields = ['title', 'description', 'note', 'due_date', 'assigned_to', 'priority', 'status']
```

And add widgets:

```python
            'note': forms.Textarea(attrs={
                'class': 'form-control focusflow-textarea',
                'rows': 3,
                'placeholder': 'Optional internal note'
            }),
            'status': forms.Select(attrs={'class': 'form-select focusflow-select'}),
```

- [ ] **Step 4: Update `create_task.html` to render note and status inputs**

Render `form.note` between description and due date, and `form.status` near priority using the existing `focusflow` card layout.

- [ ] **Step 5: Re-run the form test**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskFormTests`
Expected: PASS

### Task 3: Centralize filtering and task list behavior

**Files:**
- Modify: `tasks/views.py`
- Modify: `tasks/templates/tasks/task_list.html`
- Modify: `tasks/static/tasks/css/style.css.css`
- Modify: `tasks/tests.py`

- [ ] **Step 1: Write failing task board tests for search and filters**

Add view tests covering:

```python
class TaskListViewTests(TestCase):
    def test_admin_can_filter_by_status_priority_and_assignee(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        peker = User.objects.create_user("peker")
        matching = Task.objects.create(
            title="Fix blocker",
            description="Searchable task",
            due_date=date(2026, 5, 10),
            priority="High",
            status="Blocked",
            note="Needs backend review",
        )
        matching.assigned_to.add(peker)
        self.client.login(username="ozer", password="admin")
        response = self.client.get("/", {
            "q": "backend",
            "status": "Blocked",
            "priority": "High",
            "assignee": str(peker.id),
        })
        self.assertContains(response, "Fix blocker")

    def test_non_admin_only_sees_their_own_tasks_even_when_filtering(self):
        ozer = User.objects.create_user("ozer", password="admin")
        peker = User.objects.create_user("peker", password="admin")
        hidden = Task.objects.create(
            title="Hidden task",
            description="Should not appear",
            due_date=date(2026, 5, 10),
            status="To Do",
        )
        hidden.assigned_to.add(peker)
        self.client.login(username="ozer", password="admin")
        response = self.client.get("/", {"status": "To Do"})
        self.assertNotContains(response, "Hidden task")
```

- [ ] **Step 2: Run the task list view tests to verify failure**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskListViewTests`
Expected: FAIL because filter handling does not exist yet

- [ ] **Step 3: Refactor `task_list` filtering into a helper in `tasks/views.py`**

Add a helper like:

```python
from django.db.models import Q


def get_filtered_tasks(request):
    if request.user.is_superuser:
        queryset = Task.objects.all().prefetch_related("assigned_to")
    else:
        queryset = Task.objects.filter(assigned_to=request.user).prefetch_related("assigned_to")

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    priority = request.GET.get("priority", "").strip()
    assignee = request.GET.get("assignee", "").strip()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(note__icontains=query)
        )
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if assignee and request.user.is_superuser:
        queryset = queryset.filter(assigned_to__id=assignee)

    return queryset.distinct(), {
        "q": query,
        "status": status,
        "priority": priority,
        "assignee": assignee,
    }
```

Then group the filtered queryset by priority in `task_list`.

- [ ] **Step 4: Update `task_list.html` to render the search/filter bar and status/note display**

Add:

```html
<form method="get" class="focusflow-filter-bar ...">
```

with controls for `q`, `status`, `priority`, and `assignee`.

Each task card should also show:

```html
<span class="focusflow-status-badge focusflow-status-{{ task.status_badge_class }}">{{ task.status }}</span>
```

and note preview only when present:

```html
{% if task.note %}
    <div class="focusflow-note-preview">{{ task.note }}</div>
{% endif %}
```

Use an overdue treatment for tasks where `task.is_overdue`.

- [ ] **Step 5: Add CSS for filter controls, badges, note blocks, and overdue cards**

Extend `tasks/static/tasks/css/style.css.css` with classes for:

```css
.focusflow-filter-bar {}
.focusflow-status-badge {}
.focusflow-status-todo {}
.focusflow-status-progress {}
.focusflow-status-blocked {}
.focusflow-status-done {}
.focusflow-note-preview {}
.focusflow-overdue {}
```

- [ ] **Step 6: Re-run the task board view tests**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.TaskListViewTests`
Expected: PASS

### Task 4: Align completion/archive behavior with `Done`

**Files:**
- Modify: `tasks/views.py`
- Modify: `tasks/templates/tasks/completed_tasks.html`
- Modify: `tasks/tests.py`

- [ ] **Step 1: Write failing tests for completion and archive behavior**

Add:

```python
class CompletionFlowTests(TestCase):
    def test_complete_task_sets_done_status(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        task = Task.objects.create(
            title="Wrap release",
            description="Finish task",
            due_date=date(2026, 5, 10),
            status="To Do",
        )
        self.client.login(username="ozer", password="admin")
        self.client.get(f"/complete/{task.id}/")
        task.refresh_from_db()
        self.assertEqual(task.status, "Done")
        self.assertTrue(task.completed)

    def test_completed_page_only_shows_done_tasks(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        done = Task.objects.create(
            title="Done task",
            description="Shown",
            due_date=date(2026, 5, 10),
            status="Done",
        )
        open_task = Task.objects.create(
            title="Open task",
            description="Hidden",
            due_date=date(2026, 5, 10),
            status="Blocked",
        )
        self.client.login(username="ozer", password="admin")
        response = self.client.get("/completed/")
        self.assertContains(response, "Done task")
        self.assertNotContains(response, "Open task")
```

- [ ] **Step 2: Run the completion tests to verify failure**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.CompletionFlowTests`
Expected: FAIL because completion/archive logic still relies on the old boolean flow

- [ ] **Step 3: Update `complete_task`, `completed_tasks`, and `delete_task` logic in `tasks/views.py`**

Set:

```python
task.status = Task.STATUS_DONE
task.save()
```

and use `Task.objects.filter(status=Task.STATUS_DONE)` for the archive view and deletion lookup.

- [ ] **Step 4: Update `completed_tasks.html` to show status-aware metadata**

Keep the same page, but include note preview when present and a visible `Done` badge.

- [ ] **Step 5: Re-run the completion tests**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.CompletionFlowTests`
Expected: PASS

### Task 5: Upgrade the dashboard metrics and coverage

**Files:**
- Modify: `tasks/views.py`
- Modify: `tasks/templates/tasks/admin_dashboard.html`
- Modify: `tasks/tests.py`

- [ ] **Step 1: Write failing dashboard tests**

Add:

```python
class DashboardTests(TestCase):
    def test_dashboard_shows_workflow_counts(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        Task.objects.create(title="Todo", description="a", due_date=date(2026, 5, 10), status="To Do")
        Task.objects.create(title="Blocked", description="b", due_date=date(2026, 5, 10), status="Blocked")
        Task.objects.create(title="Done", description="c", due_date=date(2026, 5, 10), status="Done")
        self.client.login(username="ozer", password="admin")
        response = self.client.get("/dashboard/")
        self.assertContains(response, "Blocked Tasks")
        self.assertContains(response, "Tasks by Status")
```

- [ ] **Step 2: Run the dashboard tests to verify failure**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.DashboardTests`
Expected: FAIL because the dashboard does not yet expose workflow metrics

- [ ] **Step 3: Expand `admin_dashboard` context in `tasks/views.py`**

Add counts for:

```python
done_tasks = Task.objects.filter(status=Task.STATUS_DONE).count()
blocked_tasks = Task.objects.filter(status=Task.STATUS_BLOCKED).count()
open_tasks = Task.objects.exclude(status=Task.STATUS_DONE).count()
due_today = Task.objects.filter(due_date=timezone.localdate()).exclude(status=Task.STATUS_DONE).count()
overdue_tasks = Task.objects.filter(due_date__lt=timezone.localdate()).exclude(status=Task.STATUS_DONE).count()
status_counts = [
    (Task.STATUS_TODO, Task.objects.filter(status=Task.STATUS_TODO).count()),
    (Task.STATUS_IN_PROGRESS, Task.objects.filter(status=Task.STATUS_IN_PROGRESS).count()),
    (Task.STATUS_BLOCKED, Task.objects.filter(status=Task.STATUS_BLOCKED).count()),
    (Task.STATUS_DONE, Task.objects.filter(status=Task.STATUS_DONE).count()),
]
```

- [ ] **Step 4: Update `admin_dashboard.html` to display the new summaries**

Add summary cards for `Open Tasks` and `Blocked Tasks`, keep `Total Tasks`, and render a new `Tasks by Status` block plus `Due Today` and `Overdue` highlights.

- [ ] **Step 5: Re-run the dashboard tests**

Run: `source .venv/bin/activate && python manage.py test tasks.tests.DashboardTests`
Expected: PASS

### Task 6: Run the full verification pass

**Files:**
- Modify: `tasks/tests.py`
- Verify: relevant templates, model, and migration files

- [ ] **Step 1: Run the full app test suite**

Run: `source .venv/bin/activate && python manage.py test`
Expected: PASS

- [ ] **Step 2: Run migrations locally to verify schema compatibility**

Run: `source .venv/bin/activate && python manage.py migrate`
Expected: migration applies cleanly

- [ ] **Step 3: Manually verify the core flows in the browser**

Check:

```text
1. Create a task with a note and non-default status
2. Filter by search, status, priority, and assignee
3. Mark a task complete and confirm it appears in Completed Tasks
4. Open the dashboard and verify blocked/open/status counts
```

## Self-Review

- Spec coverage:
  - status workflow: Task 1 and Task 4
  - single note field: Task 2 and Task 3
  - search and filters: Task 3
  - dashboard metrics: Task 5
  - compatibility and migration: Task 1 and Task 6
- Placeholder scan:
  - no `TODO`, `TBD`, or deferred pseudo-steps remain
- Type consistency:
  - `status` values, helper names, and test expectations are consistent across all tasks

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-05-focusflow-workflow-upgrade.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
