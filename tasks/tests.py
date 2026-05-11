from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import TaskForm
from .models import Task


class TaskModelTests(TestCase):
    def test_done_status_sets_completed_true(self):
        task = Task.objects.create(
            title="Ship release",
            description="Prepare release notes",
            due_date=date(2026, 5, 6),
            status=Task.STATUS_DONE,
        )
        self.assertTrue(task.completed)

    def test_non_done_status_sets_completed_false(self):
        task = Task.objects.create(
            title="Investigate issue",
            description="Check blocker",
            due_date=date(2026, 5, 6),
            completed=True,
            status=Task.STATUS_BLOCKED,
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


class TaskFormTests(TestCase):
    def test_task_form_exposes_note_and_status(self):
        form = TaskForm()
        self.assertIn("note", form.fields)
        self.assertIn("status", form.fields)
        self.assertEqual(form.fields["status"].initial or Task.STATUS_TODO, Task.STATUS_TODO)


class TaskListViewTests(TestCase):
    def test_admin_can_filter_by_status_priority_and_assignee(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        peker = User.objects.create_user("peker")
        other_user = User.objects.create_user("tugce")

        matching = Task.objects.create(
            title="Fix blocker",
            description="Searchable task",
            due_date=date(2026, 5, 10),
            priority="High",
            status=Task.STATUS_BLOCKED,
            note="Needs backend review",
        )
        matching.assigned_to.add(peker)

        non_matching = Task.objects.create(
            title="Routine update",
            description="Normal task",
            due_date=date(2026, 5, 10),
            priority="Low",
            status=Task.STATUS_TODO,
        )
        non_matching.assigned_to.add(other_user)

        self.client.login(username="ozer", password="admin")
        response = self.client.get("/", {
            "q": "backend",
            "status": Task.STATUS_BLOCKED,
            "priority": "High",
            "assignee": str(peker.id),
        })

        self.assertContains(response, "Fix blocker")
        self.assertNotContains(response, "Routine update")

    def test_non_admin_only_sees_their_own_tasks_even_when_filtering(self):
        ozer = User.objects.create_user("ozer", password="admin")
        peker = User.objects.create_user("peker", password="admin")

        visible = Task.objects.create(
            title="Visible task",
            description="Should appear",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_TODO,
        )
        visible.assigned_to.add(ozer)

        hidden = Task.objects.create(
            title="Hidden task",
            description="Should not appear",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_TODO,
        )
        hidden.assigned_to.add(peker)

        self.client.login(username="ozer", password="admin")
        response = self.client.get("/", {"status": Task.STATUS_TODO})

        self.assertContains(response, "Visible task")
        self.assertNotContains(response, "Hidden task")


class CompletionFlowTests(TestCase):
    def test_complete_task_sets_done_status(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        task = Task.objects.create(
            title="Wrap release",
            description="Finish task",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_TODO,
        )

        self.client.login(username="ozer", password="admin")
        self.client.get(f"/complete/{task.id}/")
        task.refresh_from_db()

        self.assertEqual(task.status, Task.STATUS_DONE)
        self.assertTrue(task.completed)

    def test_completed_page_only_shows_done_tasks(self):
        admin = User.objects.create_superuser("ozer", "", "admin")

        done = Task.objects.create(
            title="Done task",
            description="Shown",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_DONE,
        )
        done.assigned_to.add(admin)

        open_task = Task.objects.create(
            title="Open task",
            description="Hidden",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_BLOCKED,
        )
        open_task.assigned_to.add(admin)

        self.client.login(username="ozer", password="admin")
        response = self.client.get("/completed/")

        self.assertContains(response, "Done task")
        self.assertNotContains(response, "Open task")


class TaskEditViewTests(TestCase):
    def test_admin_can_update_a_task(self):
        admin = User.objects.create_superuser("ozer", "", "admin")
        assignee = User.objects.create_user("john.doe", password="user")
        task = Task.objects.create(
            title="Initial title",
            description="Initial description",
            note="Initial note",
            due_date=date(2026, 5, 10),
            priority="Medium",
            status=Task.STATUS_TODO,
        )
        task.assigned_to.add(admin)

        self.client.login(username="ozer", password="admin")
        response = self.client.post(
            f"/edit/{task.id}/",
            {
                "title": "Updated title",
                "description": "Updated description",
                "note": "Updated note",
                "due_date": "2026-05-12",
                "assigned_to": [str(assignee.id)],
                "priority": "High",
                "status": Task.STATUS_IN_PROGRESS,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated title")
        self.assertEqual(task.description, "Updated description")
        self.assertEqual(task.note, "Updated note")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.status, Task.STATUS_IN_PROGRESS)
        self.assertEqual(task.assigned_to.get().username, "john.doe")

    def test_non_admin_cannot_access_task_edit_page(self):
        user = User.objects.create_user("john.doe", password="user")
        task = Task.objects.create(
            title="Member task",
            description="Should stay protected",
            due_date=date(2026, 5, 10),
            status=Task.STATUS_TODO,
        )
        task.assigned_to.add(user)

        self.client.login(username="john.doe", password="user")
        response = self.client.get(f"/edit/{task.id}/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class DashboardTests(TestCase):
    def test_dashboard_shows_workflow_counts(self):
        User.objects.create_superuser("ozer", "", "admin")
        Task.objects.create(title="Todo", description="a", due_date=date(2026, 5, 10), status=Task.STATUS_TODO)
        Task.objects.create(title="Blocked", description="b", due_date=date(2026, 5, 10), status=Task.STATUS_BLOCKED)
        Task.objects.create(title="Done", description="c", due_date=date(2026, 5, 10), status=Task.STATUS_DONE)

        self.client.login(username="ozer", password="admin")
        response = self.client.get("/admin-dashboard/")

        self.assertContains(response, "Blocked Tasks")
        self.assertContains(response, "Tasks by Status")
