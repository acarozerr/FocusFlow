from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

def is_admin(user):
    return user.is_superuser


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
    else:
        queryset = queryset.exclude(status=Task.STATUS_DONE)

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

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, status=Task.STATUS_DONE)

    # sadece admin veya kendi tamamladığı görevleri silebilir
    if request.user.is_superuser or task.assigned_to.filter(id=request.user.id).exists():
        task.delete()
        messages.success(request, "Task deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this task.")

    return redirect('completed_tasks')

@login_required
def task_list(request):
    base_tasks_query, active_filters = get_filtered_tasks(request)

    # Filter tasks by priority
    tasks_high = base_tasks_query.filter(priority='High')
    tasks_medium = base_tasks_query.filter(priority='Medium')
    tasks_low = base_tasks_query.filter(priority='Low')

    categorized_tasks = [
        {'category': 'High Priority', 'color': 'danger', 'tasks': tasks_high},
        {'category': 'Medium Priority', 'color': 'warning', 'tasks': tasks_medium},
        {'category': 'Low Priority', 'color': 'success', 'tasks': tasks_low},
    ]

    return render(request, 'tasks/task_list.html', {
        'categorized_tasks': categorized_tasks,
        'user': request.user,
        'active_filters': active_filters,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'assignees': User.objects.all().order_by('username') if request.user.is_superuser else [],
    })

@login_required
def complete_task(request, task_id):
    # Admins can complete any task, regular users only their own
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    task.status = Task.STATUS_DONE
    task.save()
    messages.success(request, "Task marked as completed.")
    return redirect('task_list')

@login_required
def completed_tasks(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(status=Task.STATUS_DONE).prefetch_related("assigned_to")
    else:
        tasks = Task.objects.filter(assigned_to=request.user, status=Task.STATUS_DONE).prefetch_related("assigned_to")

    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})

@user_passes_test(is_admin)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # görevi oluştur ama kaydetme
            task.save()  # kaydet (ID oluşturulsun)
            form.save_m2m()  # assigned_to gibi ManyToMany alanları kaydet
            messages.success(request, "New task successfully assigned.")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status=Task.STATUS_DONE).count()
    incomplete_tasks = Task.objects.exclude(status=Task.STATUS_DONE).count()
    blocked_tasks = Task.objects.filter(status=Task.STATUS_BLOCKED).count()
    open_tasks = Task.objects.exclude(status=Task.STATUS_DONE).count()
    today = timezone.localdate()
    due_today = Task.objects.filter(due_date=today).exclude(status=Task.STATUS_DONE).count()
    overdue_tasks = Task.objects.filter(due_date__lt=today).exclude(status=Task.STATUS_DONE).count()

    priority_high = Task.objects.filter(priority='High').count()
    priority_medium = Task.objects.filter(priority='Medium').count()
    priority_low = Task.objects.filter(priority='Low').count()

    user_task_counts = []
    for user in User.objects.all():
        user_tasks = Task.objects.filter(assigned_to=user).exclude(status=Task.STATUS_DONE).count()
        user_task_counts.append((user.username, user_tasks))

    status_counts = [
        (Task.STATUS_TODO, Task.objects.filter(status=Task.STATUS_TODO).count()),
        (Task.STATUS_IN_PROGRESS, Task.objects.filter(status=Task.STATUS_IN_PROGRESS).count()),
        (Task.STATUS_BLOCKED, Task.objects.filter(status=Task.STATUS_BLOCKED).count()),
        (Task.STATUS_DONE, Task.objects.filter(status=Task.STATUS_DONE).count()),
    ]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
        'blocked_tasks': blocked_tasks,
        'open_tasks': open_tasks,
        'due_today': due_today,
        'overdue_tasks': overdue_tasks,
        'priority_high': priority_high,
        'priority_medium': priority_medium,
        'priority_low': priority_low,
        'user_task_counts': user_task_counts,
        'status_counts': status_counts,
    }

    return render(request, 'tasks/admin_dashboard.html', context)

@user_passes_test(is_admin)
def incomplete_tasks(request):
    tasks = Task.objects.exclude(status=Task.STATUS_DONE).prefetch_related("assigned_to")
    return render(request, 'tasks/incomplete_tasks.html', {'tasks': tasks})


@user_passes_test(is_admin)
def all_tasks(request):
    tasks = Task.objects.all().prefetch_related("assigned_to")
    return render(request, 'tasks/all_tasks.html', {'tasks': tasks})

@user_passes_test(is_admin)
def calendar_view(request):
    tasks = Task.objects.all()
    events = []

    for task in tasks:
        events.append({
            'title': task.title,
            'start': str(task.due_date),
            'color': '#5f7a65' if task.status == Task.STATUS_DONE else '#b08949' if task.status == Task.STATUS_IN_PROGRESS else '#b8473b' if task.status == Task.STATUS_BLOCKED else '#7a8696',
        })

    return render(request, 'tasks/calendar_view.html', {'events': events})
