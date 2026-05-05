from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_TODO = "To Do"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_BLOCKED = "Blocked"
    STATUS_DONE = "Done"
    STATUS_CHOICES = [
        (STATUS_TODO, STATUS_TODO),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
        (STATUS_BLOCKED, STATUS_BLOCKED),
        (STATUS_DONE, STATUS_DONE),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    note = models.TextField(blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    assigned_to = models.ManyToManyField(User)  # 🔄 Multiple users can be assigned
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)

    def save(self, *args, **kwargs):
        self.completed = self.status == self.STATUS_DONE
        super().save(*args, **kwargs)

    def formatted_assignees(self):
        return ", ".join(user.username.capitalize() for user in self.assigned_to.all())

    def is_overdue(self):
        return not self.completed and self.due_date < timezone.localdate()

    def status_badge_class(self):
        return {
            self.STATUS_TODO: "todo",
            self.STATUS_IN_PROGRESS: "progress",
            self.STATUS_BLOCKED: "blocked",
            self.STATUS_DONE: "done",
        }.get(self.status, "todo")

    def __str__(self):
        return self.title
