# FocusFlow Render Deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make FocusFlow deployable to Render with correct Gunicorn startup, environment-aware Django settings, and production static file handling.

**Architecture:** Keep the deployment setup lightweight and repo-local. Fix the Render service definition, make `settings.py` interpret production environment variables correctly, and verify the build with Django’s deployment checks and static collection flow.

**Tech Stack:** Django 5, Gunicorn, WhiteNoise, Render web service, SQLite

---

## File Structure

- Modify: `render.yaml`
  Responsibility: define the correct Render build and startup commands
- Modify: `gorev_sistemi/settings.py`
  Responsibility: make deployment settings environment-aware and remove static-file warnings
- Verify: `requirements.txt`
  Responsibility: confirm Gunicorn and WhiteNoise dependencies already exist

### Task 1: Fix Render service commands

**Files:**
- Modify: `render.yaml`

- [ ] **Step 1: Correct the build command**

Set:

```yaml
buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
```

- [ ] **Step 2: Correct the Gunicorn startup path**

Set:

```yaml
startCommand: "gunicorn gorev_sistemi.wsgi:application"
```

### Task 2: Make Django settings deployment-aware

**Files:**
- Modify: `gorev_sistemi/settings.py`

- [ ] **Step 1: Read `DEBUG` from the environment**

Use logic like:

```python
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
```

- [ ] **Step 2: Clean `ALLOWED_HOSTS` handling**

Keep local hosts and current public hosts, but also support Render hostname via environment if present. A simple pattern is:

```python
ALLOWED_HOSTS = [
    "127.0.0.1",
    ".localhost",
    "[::1]",
    "www.tasklist.site",
    "todo-list-y3em.onrender.com",
]
render_external_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)
```

- [ ] **Step 3: Remove the invalid static directory warning**

Replace the current unconditional `STATICFILES_DIRS` with a conditional check:

```python
STATICFILES_DIRS = []
static_dir = BASE_DIR / "static"
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)
```

### Task 3: Verify deployment behavior locally

**Files:**
- Verify only

- [ ] **Step 1: Run the test suite**

Run: `source .venv/bin/activate && python manage.py test`
Expected: PASS

- [ ] **Step 2: Run Django deployment checks**

Run: `source .venv/bin/activate && python manage.py check --deploy`
Expected: warnings only for production-hardening items we intentionally deferred, but no blocking misconfiguration

- [ ] **Step 3: Run static collection**

Run: `source .venv/bin/activate && python manage.py collectstatic --noinput`
Expected: static assets copy into `staticfiles/` successfully

## Self-Review

- Spec coverage:
  - Render command fixes: Task 1
  - env-driven debug: Task 2
  - allowed hosts: Task 2
  - static cleanup and build verification: Tasks 2 and 3
- Placeholder scan:
  - no `TODO`, `TBD`, or vague pseudo-steps remain
- Type consistency:
  - the same WSGI module and env variable names are used throughout

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-06-focusflow-render-deploy.md`. Execution will continue inline in this session.
