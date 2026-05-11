# Task Edit Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an admin-only task editing flow so the project clearly supports the update portion of CRUD.

**Architecture:** Reuse the existing `TaskForm` and FocusFlow form styling instead of creating a second editing form. Add one admin-only route and view, one dedicated template, and expose edit actions from the admin-facing task lists.

**Tech Stack:** Django views, URLs, templates, ModelForm, Django test client

---

### Task 1: Cover the edit flow with tests

**Files:**
- Modify: `tasks/tests.py`

- [ ] Add a test proving an admin can submit updated task data through an edit route.
- [ ] Add a test proving a non-admin user cannot access the edit route.

### Task 2: Add the route and view

**Files:**
- Modify: `tasks/urls.py`
- Modify: `tasks/views.py`

- [ ] Add an `edit_task` URL pattern with a task id parameter.
- [ ] Implement an admin-only edit view that loads an existing task instance into `TaskForm` and saves updates.

### Task 3: Add the edit template and entry points

**Files:**
- Create: `tasks/templates/tasks/edit_task.html`
- Modify: `tasks/templates/tasks/task_list.html`
- Modify: `tasks/templates/tasks/all_tasks.html`
- Modify: `tasks/templates/tasks/incomplete_tasks.html`
- Modify: `tasks/templates/tasks/completed_tasks.html`

- [ ] Create a dedicated edit page consistent with the existing create page styling.
- [ ] Add visible edit actions on admin-facing task lists.

### Task 4: Verify the feature

**Files:**
- Test: `tasks/tests.py`

- [ ] Run the new focused tests first.
- [ ] Run the full Django test suite after implementation.
