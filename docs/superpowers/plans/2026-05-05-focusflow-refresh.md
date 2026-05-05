# FocusFlow Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the existing Django task manager into a warmer, more polished `FocusFlow` experience without changing its core task workflows.

**Architecture:** Keep the refresh template-first and CSS-driven. Establish the new brand and shared visual language in `templates/base.html` and the shared stylesheet, then align the login page and the highest-traffic task pages to that system with minimal markup changes.

**Tech Stack:** Django templates, Bootstrap 5, app-scoped CSS, existing Django auth/task views

---

## File Structure

- Modify: `templates/base.html`
  Responsibility: shared app shell, navbar branding, global utility classes, dark mode hook placement
- Modify: `templates/registration/login.html`
  Responsibility: login-specific hero, form card, and brand presentation
- Modify: `tasks/static/tasks/css/style.css.css`
  Responsibility: FocusFlow design tokens, shared component styling, responsive polish, dark mode adjustments
- Modify: `tasks/templates/tasks/task_list.html`
  Responsibility: main task dashboard layout, page heading, action button hierarchy, category presentation
- Modify: `tasks/templates/tasks/create_task.html`
  Responsibility: aligned card layout and button treatment for the create form
- Modify: `tasks/templates/tasks/all_tasks.html`
  Responsibility: consistency with refreshed list/card styling
- Modify: `tasks/templates/tasks/completed_tasks.html`
  Responsibility: consistency with refreshed list/card styling and destructive action presentation

### Task 1: Refresh the shared shell and brand

**Files:**
- Modify: `templates/base.html`
- Modify: `tasks/static/tasks/css/style.css.css`

- [ ] **Step 1: Inspect the current shared shell before editing**

Run: `sed -n '1,220p' templates/base.html`
Expected: existing `To-Do List` brand, dark navbar, inline dark-mode CSS and script

- [ ] **Step 2: Replace the base template markup with a lighter FocusFlow shell**

Use this `templates/base.html` structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FocusFlow</title>
    {% load static %}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{% static 'tasks/css/style.css' %}">
</head>
<body class="focusflow-body">

<nav class="navbar navbar-expand-lg focusflow-navbar">
    <div class="container">
        <a class="navbar-brand focusflow-brand" href="/">
            <span class="focusflow-brand-mark"><i class="fas fa-compass"></i></span>
            <span>
                <strong>FocusFlow</strong>
                <small>Task workspace</small>
            </span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-lg-center">
                {% if user.is_authenticated %}
                    <li class="nav-item me-lg-3">
                        <span class="focusflow-user-chip">
                            <i class="fas fa-user-circle"></i>
                            {{ user.username }}
                        </span>
                    </li>
                    <li class="nav-item me-lg-2">
                        <button id="darkModeToggle" class="btn focusflow-icon-button" type="button" aria-label="Toggle dark mode">
                            <i class="fas fa-moon"></i>
                        </button>
                    </li>
                    <li class="nav-item">
                        <form method="post" action="{% url 'logout' %}" class="d-inline">
                            {% csrf_token %}
                            <button type="submit" class="btn focusflow-secondary-button btn-sm">
                                <i class="fas fa-sign-out-alt"></i> Log out
                            </button>
                        </form>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="btn focusflow-secondary-button btn-sm" href="{% url 'login' %}">
                            <i class="fas fa-sign-in-alt"></i> Log in
                        </a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

<main class="focusflow-main py-4 py-lg-5">
    {% if messages %}
    <div class="container mb-4">
        {% for message in messages %}
        <div class="alert focusflow-alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    {% block content %}{% endblock %}
</main>

<script>
    const toggleBtn = document.getElementById('darkModeToggle');
    const body = document.body;

    if (localStorage.getItem("darkMode") === "true") {
        body.classList.add('dark-mode');
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }

    toggleBtn?.addEventListener('click', function () {
        body.classList.toggle('dark-mode');
        const isDark = body.classList.contains('dark-mode');
        toggleBtn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        localStorage.setItem("darkMode", isDark);
    });
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

- [ ] **Step 3: Replace the stylesheet with shared FocusFlow tokens and components**

Use this `tasks/static/tasks/css/style.css.css` content:

```css
:root {
    --ff-bg: #f4efe6;
    --ff-bg-soft: #efe7d8;
    --ff-surface: #fffdf8;
    --ff-surface-strong: #ffffff;
    --ff-border: #dccfb6;
    --ff-text: #24303a;
    --ff-text-soft: #6b7280;
    --ff-accent: #8b6f3d;
    --ff-accent-strong: #6f572c;
    --ff-success: #5f7a65;
    --ff-shadow: 0 18px 45px rgba(69, 48, 21, 0.08);
    --ff-radius-lg: 24px;
    --ff-radius-md: 16px;
}

body.focusflow-body {
    font-family: "Manrope", sans-serif;
    background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.8), transparent 30%),
        linear-gradient(180deg, #f8f4ec 0%, var(--ff-bg) 100%);
    color: var(--ff-text);
    min-height: 100vh;
}

.focusflow-navbar {
    background: rgba(255, 251, 244, 0.9);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(140, 111, 61, 0.12);
}

.focusflow-brand {
    display: inline-flex;
    align-items: center;
    gap: 0.9rem;
    text-decoration: none;
    color: var(--ff-text);
}

.focusflow-brand:hover {
    color: var(--ff-text);
}

.focusflow-brand strong {
    display: block;
    line-height: 1.1;
    font-size: 1.05rem;
}

.focusflow-brand small {
    display: block;
    color: var(--ff-text-soft);
    font-size: 0.74rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.focusflow-brand-mark {
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 0.95rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #8b6f3d, #b59a63);
    color: #fffaf2;
    box-shadow: 0 10px 24px rgba(139, 111, 61, 0.25);
}

.focusflow-user-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 0.9rem;
    border-radius: 999px;
    background: rgba(139, 111, 61, 0.09);
    color: var(--ff-text);
    font-weight: 600;
}

.focusflow-icon-button,
.focusflow-secondary-button,
.focusflow-primary-button,
.focusflow-chip-button {
    border-radius: 999px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.focusflow-icon-button {
    width: 2.6rem;
    height: 2.6rem;
    border: 1px solid var(--ff-border);
    color: var(--ff-text);
    background: rgba(255, 255, 255, 0.65);
}

.focusflow-secondary-button {
    background: transparent;
    border: 1px solid var(--ff-border);
    color: var(--ff-text);
}

.focusflow-secondary-button:hover,
.focusflow-icon-button:hover {
    background: rgba(139, 111, 61, 0.08);
    border-color: rgba(139, 111, 61, 0.35);
    color: var(--ff-text);
}

.focusflow-primary-button {
    background: linear-gradient(135deg, var(--ff-accent), #b08b4f);
    border: none;
    color: #fffdf8;
    box-shadow: 0 12px 28px rgba(139, 111, 61, 0.24);
}

.focusflow-primary-button:hover {
    background: linear-gradient(135deg, var(--ff-accent-strong), #9e7f48);
    color: #fffdf8;
    transform: translateY(-1px);
}

.focusflow-main .container,
.focusflow-shell {
    position: relative;
}

.focusflow-page-card,
.card,
.list-group-item,
.alert,
.focusflow-panel {
    border-radius: var(--ff-radius-md);
    border: 1px solid rgba(220, 207, 182, 0.9);
    box-shadow: var(--ff-shadow);
}

.focusflow-page-card,
.card,
.list-group-item,
.focusflow-panel {
    background: rgba(255, 253, 248, 0.92);
}

.list-group {
    gap: 0.95rem;
    display: grid;
}

.list-group-item {
    padding: 1.1rem 1.2rem;
}

.focusflow-page-header h1,
.focusflow-page-header h2 {
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.35rem;
}

.focusflow-page-header p {
    color: var(--ff-text-soft);
    margin-bottom: 0;
}

.focusflow-section-label {
    color: var(--ff-accent-strong);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
}

.focusflow-task-meta,
.focusflow-muted {
    color: var(--ff-text-soft);
}

.focusflow-alert {
    background: rgba(255, 253, 248, 0.92);
}

.focusflow-empty {
    border-radius: var(--ff-radius-lg);
    background: rgba(255, 253, 248, 0.82);
    border: 1px dashed rgba(139, 111, 61, 0.35);
    color: var(--ff-text-soft);
}

.focusflow-form-card {
    max-width: 760px;
    margin: 0 auto;
    padding: 2rem;
}

.focusflow-login-shell {
    min-height: 100vh;
    background:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.65), transparent 28%),
        linear-gradient(180deg, #f8f4ec 0%, #efe4d0 100%);
}

.focusflow-login-panel {
    max-width: 460px;
    width: 100%;
    border-radius: 28px;
    border: 1px solid rgba(220, 207, 182, 0.95);
    background: rgba(255, 252, 247, 0.95);
    box-shadow: 0 24px 55px rgba(68, 48, 23, 0.12);
}

.focusflow-login-brand {
    text-align: center;
    margin-bottom: 1.75rem;
}

.focusflow-login-brand h1 {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.focusflow-login-brand p {
    color: var(--ff-text-soft);
}

.focusflow-input,
.focusflow-select,
.focusflow-textarea {
    border-radius: 14px;
    border: 1px solid var(--ff-border);
    padding: 0.82rem 0.95rem;
    background: rgba(255, 255, 255, 0.96);
}

.focusflow-input:focus,
.focusflow-select:focus,
.focusflow-textarea:focus {
    border-color: rgba(139, 111, 61, 0.7);
    box-shadow: 0 0 0 0.2rem rgba(139, 111, 61, 0.12);
}

.dark-mode {
    --ff-bg: #1d1a17;
    --ff-bg-soft: #292420;
    --ff-surface: #2b2621;
    --ff-surface-strong: #352f29;
    --ff-border: #55483b;
    --ff-text: #f3ede3;
    --ff-text-soft: #d0c4b3;
    --ff-accent: #c0a26a;
    --ff-accent-strong: #d7b87b;
    --ff-success: #81a28b;
    --ff-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
}

.dark-mode.focusflow-body {
    background: linear-gradient(180deg, #191614 0%, #241f1b 100%);
}

.dark-mode .focusflow-navbar,
.dark-mode .focusflow-page-card,
.dark-mode .card,
.dark-mode .list-group-item,
.dark-mode .focusflow-panel,
.dark-mode .focusflow-alert,
.dark-mode .focusflow-login-panel {
    background: rgba(43, 38, 33, 0.95);
    color: var(--ff-text);
}

.dark-mode .focusflow-empty {
    background: rgba(43, 38, 33, 0.85);
}

@media (max-width: 767.98px) {
    .focusflow-page-header {
        gap: 1rem;
    }

    .focusflow-form-card {
        padding: 1.4rem;
    }

    .focusflow-login-brand h1 {
        font-size: 2rem;
    }
}
```

- [ ] **Step 4: Run the Django test suite to ensure no template syntax regressions**

Run: `source .venv/bin/activate && python manage.py test`
Expected: existing tests pass or report zero failures

- [ ] **Step 5: Commit the shared shell refresh**

```bash
git add templates/base.html tasks/static/tasks/css/style.css.css
git commit -m "feat: refresh focusflow shared shell"
```

### Task 2: Align the login page with the new brand

**Files:**
- Modify: `templates/registration/login.html`
- Modify: `tasks/static/tasks/css/style.css.css`

- [ ] **Step 1: Inspect the existing login template**

Run: `sed -n '1,220p' templates/registration/login.html`
Expected: standalone page with `To-Do Task Management` branding and inline purple-accent styling

- [ ] **Step 2: Replace the login template with FocusFlow-branded markup**

Use this `templates/registration/login.html` content:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FocusFlow | Log In</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{% static 'tasks/css/style.css' %}">
</head>
<body class="focusflow-login-shell d-flex align-items-center justify-content-center p-4">

<div>
    <div class="focusflow-login-brand">
        <div class="focusflow-brand-mark mx-auto mb-3">
            <i class="fas fa-compass"></i>
        </div>
        <h1>FocusFlow</h1>
        <p>Keep your team aligned with a calmer task workspace.</p>
    </div>

    <div class="focusflow-login-panel p-4 p-lg-5">
        <div class="mb-4 text-center">
            <div class="focusflow-section-label mb-2">Welcome back</div>
            <h2 class="mb-2">Log in to your workspace</h2>
            <p class="focusflow-muted mb-0">Use your account to review tasks, assignments, and progress.</p>
        </div>

        <form method="post" action="{% url 'login' %}">
            {% csrf_token %}

            <div class="mb-3">
                <label for="id_username" class="form-label fw-semibold">Username</label>
                <div class="input-group">
                    <span class="input-group-text bg-white border-end-0 rounded-start-4"><i class="fas fa-user"></i></span>
                    <input type="text" name="username" id="id_username" class="form-control focusflow-input border-start-0" placeholder="Enter your username" required>
                </div>
            </div>

            <div class="mb-4">
                <label for="id_password" class="form-label fw-semibold">Password</label>
                <div class="input-group">
                    <span class="input-group-text bg-white border-end-0 rounded-start-4"><i class="fas fa-lock"></i></span>
                    <input type="password" name="password" id="id_password" class="form-control focusflow-input border-start-0" placeholder="Enter your password" required>
                </div>
            </div>

            <button type="submit" class="btn focusflow-primary-button w-100 py-3">Log In</button>
        </form>
    </div>
</div>

</body>
</html>
```

- [ ] **Step 3: Reload the login page locally and visually verify the new hierarchy**

Run: `source .venv/bin/activate && python manage.py runserver`
Expected: login page shows `FocusFlow`, warm neutral background, unified button and card language

- [ ] **Step 4: Commit the login refresh**

```bash
git add templates/registration/login.html tasks/static/tasks/css/style.css.css
git commit -m "feat: refresh focusflow login experience"
```

### Task 3: Polish the primary task dashboard and create form

**Files:**
- Modify: `tasks/templates/tasks/task_list.html`
- Modify: `tasks/templates/tasks/create_task.html`
- Modify: `tasks/static/tasks/css/style.css.css`

- [ ] **Step 1: Inspect the main task templates**

Run: `sed -n '1,240p' tasks/templates/tasks/task_list.html && sed -n '1,220p' tasks/templates/tasks/create_task.html`
Expected: plain bootstrap spacing, generic headings, default button treatments

- [ ] **Step 2: Replace the main task list template with a branded dashboard layout**

Use this `tasks/templates/tasks/task_list.html` content:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="focusflow-page-card p-4 p-lg-5 mb-4">
        <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 focusflow-page-header">
            <div>
                <div class="focusflow-section-label mb-2">Workspace Overview</div>
                <h2 class="mb-2">Task Board</h2>
                <p>Track open work, stay on top of deadlines, and keep assignments visible.</p>
            </div>

            {% if user.is_superuser %}
                <div class="d-flex flex-wrap gap-2">
                    <a href="{% url 'admin_dashboard' %}" class="btn focusflow-secondary-button btn-sm">
                        <i class="fas fa-chart-bar"></i> Dashboard
                    </a>
                    <a href="{% url 'calendar_view' %}" class="btn focusflow-secondary-button btn-sm">
                        <i class="fas fa-calendar-alt"></i> Calendar
                    </a>
                    <a href="{% url 'create_task' %}" class="btn focusflow-primary-button btn-sm">
                        <i class="fas fa-plus"></i> New Task
                    </a>
                </div>
            {% else %}
                <a href="{% url 'completed_tasks' %}" class="btn focusflow-secondary-button btn-sm">
                    <i class="fas fa-check-circle"></i> Completed Tasks
                </a>
            {% endif %}
        </div>
    </div>

    {% for category_obj in categorized_tasks %}
        <section class="mb-4">
            <div class="d-flex align-items-center justify-content-between mb-3">
                <h4 class="mb-0">{{ category_obj.category }}</h4>
                <span class="focusflow-muted">{{ category_obj.tasks|length }} task{{ category_obj.tasks|length|pluralize }}</span>
            </div>

            {% if category_obj.tasks %}
                <ul class="list-group">
                    {% for task in category_obj.tasks %}
                        <li class="list-group-item d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 {% if task.completed %}list-group-item-success{% endif %}">
                            <div>
                                <strong class="d-block fs-5 mb-1">{{ task.title }}</strong>
                                <p class="mb-2 focusflow-task-meta">{{ task.description }}</p>
                                <div class="focusflow-task-meta small">
                                    Due {{ task.due_date|date:"d M Y" }} · Assigned to {{ task.assigned_to.all|join:", " }}
                                </div>
                            </div>
                            <div class="text-lg-end">
                                {% if not task.completed %}
                                    <a href="{% url 'complete_task' task.id %}" class="btn focusflow-primary-button btn-sm mt-1">Mark Complete</a>
                                {% else %}
                                    <span class="badge rounded-pill text-bg-success mt-1 px-3 py-2"><i class="fas fa-check-circle"></i> Completed</span>
                                {% endif %}
                            </div>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <div class="focusflow-empty p-4">No tasks in this category yet.</div>
            {% endif %}
        </section>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 3: Replace the create form template with a card-based form layout**

Use this `tasks/templates/tasks/create_task.html` content:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="focusflow-page-card focusflow-form-card">
        <div class="focusflow-page-header mb-4">
            <div class="focusflow-section-label mb-2">Planning</div>
            <h2>Create a New Task</h2>
            <p>Capture the task clearly, set its due date, and assign the right teammates.</p>
        </div>

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">
                <label class="form-label fw-semibold">{{ form.title.label }}</label>
                {{ form.title }}
            </div>

            <div class="mb-3">
                <label class="form-label fw-semibold">{{ form.description.label }}</label>
                {{ form.description }}
            </div>

            <div class="mb-3">
                <label class="form-label fw-semibold">{{ form.due_date.label }}</label>
                {{ form.due_date }}
            </div>

            <div class="mb-3">
                <label class="form-label fw-semibold">{{ form.assigned_to.label }}</label>
                <div class="focusflow-page-card p-3">
                    {% for user in form.assigned_to %}
                        <div class="form-check mb-2">
                            {{ user.tag }}
                            <label class="form-check-label" for="{{ user.id_for_label }}">{{ user.choice_label }}</label>
                        </div>
                    {% endfor %}
                </div>
            </div>

            <div class="mb-4">
                <label class="form-label fw-semibold">{{ form.priority.label }}</label>
                {{ form.priority }}
            </div>

            <div class="d-flex flex-wrap gap-2">
                <button type="submit" class="btn focusflow-primary-button">Save Task</button>
                <a href="{% url 'task_list' %}" class="btn focusflow-secondary-button">Cancel</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Ensure the form controls receive the refreshed classes in `tasks/forms.py`**

Update the widget definitions in `tasks/forms.py` so each control includes the new classes:

```python
widgets = {
    'title': forms.TextInput(attrs={'class': 'form-control focusflow-input', 'placeholder': 'Task title'}),
    'description': forms.Textarea(attrs={'class': 'form-control focusflow-textarea', 'rows': 4, 'placeholder': 'Add a short task description'}),
    'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control focusflow-input'}),
    'priority': forms.Select(attrs={'class': 'form-select focusflow-select'}),
}
```

- [ ] **Step 5: Reload the authenticated task pages and verify layout stability**

Run: `source .venv/bin/activate && python manage.py runserver`
Expected: task board and create form match FocusFlow styling without broken template output

- [ ] **Step 6: Commit the task board polish**

```bash
git add tasks/templates/tasks/task_list.html tasks/templates/tasks/create_task.html tasks/forms.py tasks/static/tasks/css/style.css.css
git commit -m "feat: polish focusflow task workspace"
```

### Task 4: Bring supporting task pages into the same visual system

**Files:**
- Modify: `tasks/templates/tasks/all_tasks.html`
- Modify: `tasks/templates/tasks/completed_tasks.html`

- [ ] **Step 1: Inspect the supporting list templates**

Run: `sed -n '1,220p' tasks/templates/tasks/all_tasks.html && sed -n '1,220p' tasks/templates/tasks/completed_tasks.html`
Expected: basic list markup with generic headings and bootstrap defaults

- [ ] **Step 2: Replace `all_tasks.html` with a consistent page-card layout**

Use this `tasks/templates/tasks/all_tasks.html` content:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="focusflow-page-card p-4 p-lg-5">
        <div class="focusflow-page-header mb-4">
            <div class="focusflow-section-label mb-2">Overview</div>
            <h2>All Tasks</h2>
            <p>A complete view of every assignment currently in the workspace.</p>
        </div>

        {% if tasks %}
            <ul class="list-group">
                {% for task in tasks %}
                    <li class="list-group-item {% if task.completed %}list-group-item-success{% endif %}">
                        <strong class="d-block fs-5 mb-1">{{ task.title }}</strong>
                        <p class="mb-2 focusflow-task-meta">{{ task.description }}</p>
                        <div class="small focusflow-task-meta">
                            Due {{ task.due_date|date:"d M Y" }} · Assigned to {{ task.assigned_to.all|join:", " }} ·
                            {% if task.completed %}Completed{% else %}Incomplete{% endif %}
                        </div>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="focusflow-empty p-4">No tasks found.</div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: Replace `completed_tasks.html` with a consistent page-card layout**

Use this `tasks/templates/tasks/completed_tasks.html` content:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="focusflow-page-card p-4 p-lg-5">
        <div class="focusflow-page-header mb-4">
            <div class="focusflow-section-label mb-2">Archive</div>
            <h2>Completed Tasks</h2>
            <p>Review finished work and remove items that no longer need to stay visible.</p>
        </div>

        {% if tasks %}
            <ul class="list-group">
                {% for task in tasks %}
                    <li class="list-group-item d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 list-group-item-success">
                        <div>
                            <strong class="d-block fs-5 mb-1">{{ task.title }}</strong>
                            <p class="mb-2 focusflow-task-meta">{{ task.description }}</p>
                            <div class="small focusflow-task-meta">Completed on {{ task.updated_at|date:"d M Y H:i" }}</div>
                        </div>
                        <form method="post" action="{% url 'delete_task' task.id %}" onsubmit="return confirm('Are you sure you want to delete this task?');">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-outline-danger rounded-pill">
                                <i class="fas fa-times"></i> Delete
                            </button>
                        </form>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="focusflow-empty p-4">You have not completed any tasks yet.</div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Verify the core task pages on desktop and mobile-width viewport**

Run: `source .venv/bin/activate && python manage.py test`
Expected: tests pass after supporting template updates

- [ ] **Step 5: Commit the supporting page polish**

```bash
git add tasks/templates/tasks/all_tasks.html tasks/templates/tasks/completed_tasks.html
git commit -m "feat: unify focusflow supporting task pages"
```

## Self-Review

- Spec coverage check:
  - Branding to `FocusFlow`: covered in Tasks 1 and 2
  - Shared style system: covered in Task 1
  - Login alignment: covered in Task 2
  - Main task page polish: covered in Task 3
  - Supporting task page polish: covered in Task 4
  - Desktop/mobile verification: covered in Tasks 1, 3, and 4
- Placeholder scan:
  - No `TODO`, `TBD`, or deferred implementation markers remain
- Type consistency:
  - Shared CSS class names are reused consistently across all template tasks

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-05-focusflow-refresh.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
