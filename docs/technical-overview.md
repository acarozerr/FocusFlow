# FocusFlow Technical Overview

## 1. System Summary

FocusFlow is a Django web application built for task coordination, workflow visibility, and role-based collaboration. It is designed around a central `Task` model and separates responsibilities across Django's model, view, template, and form layers.

The application has two main user modes:

- **Admin users**: manage tasks, assign users, review all tasks, and access reporting views
- **Regular users**: access only tasks assigned to them and update their own workflow progress

## 2. Architecture

### Django MVT Pattern

The project follows Django's built-in MVT architecture:

- **Models** define the database schema and relationships
- **Views** contain application logic and query behavior
- **Templates** render the interface seen by the user

This separation keeps the project maintainable and makes each layer easier to test and reason about.

### Main Application Units

- `gorev_sistemi/settings.py`
  - project configuration
  - database connection
  - deployment-aware settings

- `gorev_sistemi/urls.py`
  - root routing
  - authentication URL inclusion

- `tasks/models.py`
  - task schema
  - workflow sync logic

- `tasks/views.py`
  - task listing, filtering, completion, dashboard metrics, and calendar data

- `tasks/forms.py`
  - `TaskForm` for controlled task creation

- `tasks/templates/tasks/`
  - task board, archive, dashboard, calendar, and task creation screens

## 3. Database Design

### Primary Model: `Task`

The `Task` model includes the following fields:

- `title`: short task name
- `description`: detailed task description
- `note`: internal note field
- `due_date`: deadline tracking
- `completed`: boolean completion state
- `priority`: `High`, `Medium`, `Low`
- `status`: `To Do`, `In Progress`, `Blocked`, `Done`
- `assigned_to`: relation to Django `User`

### Relationship Design

`assigned_to` is implemented as a `ManyToManyField(User)`.

This was chosen because:

- one task may belong to multiple users
- one user may be assigned to many tasks

This relationship is more flexible than a single-owner `ForeignKey` and fits collaborative task ownership.

### Data Integrity

The model keeps `status` and `completed` synchronized in `save()`. This ensures that:

- workflow status remains the primary source of truth
- older completion-based logic remains consistent
- completed archive behavior continues to work predictably

## 4. Request and View Flow

The request flow is:

`URL -> View -> ORM Query -> Template -> HTML Response`

### Examples

- `/`
  - renders the main task board
  - applies visibility and filter rules

- `/create/`
  - allows admins to create and assign tasks

- `/completed/`
  - shows archived completed tasks

- `/admin-dashboard/`
  - computes high-level workflow metrics

- `/calendar/`
  - prepares event data for calendar rendering

## 5. Authentication and Authorization

The project uses Django's built-in authentication system.

### Authentication

- login
- logout
- session-based user handling

### Authorization

Authorization is implemented with decorators and queryset scoping:

- `@login_required`
  - blocks anonymous access

- `@user_passes_test(is_admin)`
  - restricts admin-only views

- view-level queryset filtering
  - admins receive all tasks
  - regular users receive only their assigned tasks

This creates a clear distinction between user and admin interfaces without maintaining separate applications.

## 6. Filtering and Query Design

The task board uses a shared helper function to centralize filtering behavior.

Supported filters:

- text query
- status
- priority
- assignee

The implementation uses Django ORM tools such as:

- `filter()`
- `exclude()`
- `Q(...)`
- `distinct()`
- `prefetch_related("assigned_to")`

This improves maintainability and avoids duplicating filter logic across views.

## 7. Dashboard Logic

The admin dashboard is computed dynamically from ORM queries instead of storing derived counts in the database.

Tracked metrics include:

- total tasks
- open tasks
- completed tasks
- blocked tasks
- due today
- overdue tasks
- tasks by priority
- tasks by status
- tasks by user

This keeps the dashboard accurate with the current database state.

## 8. Forms and Validation

Task creation is handled through a Django `ModelForm`.

Benefits of this approach:

- model and form stay synchronized
- validation is applied automatically
- widgets can be customized for UI consistency

The task form exposes the workflow fields required by the admin interface while preserving Django's form validation pipeline.

## 9. Frontend Structure

The interface uses shared layout composition:

- `templates/base.html`
  - common navigation, layout, theme structure

- page-specific templates
  - task board
  - create task
  - completed tasks
  - admin dashboard
  - calendar view

Styling is centralized in the task app's static CSS file so the interface remains consistent across screens.

## 10. Testing Strategy

The current test suite covers:

- workflow status synchronization
- form structure
- admin filtering behavior
- user visibility rules
- completion flow
- dashboard output

These tests provide confidence that the most important business rules still work after changes.

## 11. Deployment Strategy

The application is deployed on Render using a blueprint configuration.

### Deployment Stack

- GitHub for source control
- Render for hosting
- Gunicorn as WSGI server
- WhiteNoise for static files

### Deployment Configuration

- install dependencies
- run `collectstatic`
- run migrations
- start `gunicorn gorev_sistemi.wsgi:application`

Environment-based settings are used so the same codebase works in both development and production.

## 12. Design Decisions

### Why SQLite?

SQLite was selected for local development and project demonstration because it is simple to configure, portable, and appropriate for a course-scale application.

### Why keep both `status` and `completed`?

The project originally relied on a boolean completion state. When richer workflow tracking was added, the boolean field was preserved for compatibility while `status` became the richer workflow model.

### Why build a custom admin interface if Django Admin already exists?

Django Admin remains useful for backend management, but it is not ideal as the main product experience. FocusFlow therefore includes both:

- Django Admin for built-in management
- a custom in-app admin interface for the actual task management workflow

## 13. Conclusion

FocusFlow is not only a functional task board but also a structured Django application that demonstrates:

- sound relational modeling
- view-layer business logic
- role-based access control
- UI separation between admin and regular users
- practical deployment to the web

This makes it a strong fit for a Django term project that is expected to combine architecture, usability, testing, and deployment.
