# FocusFlow

FocusFlow is a Django-based task management and workflow tracking system designed for small teams. It provides role-based access for administrators and regular users, supports task assignment to multiple people, and includes workflow status tracking, filtering, dashboard reporting, and a calendar view.

## Live Demo

- Application: [https://focusflow-nodq.onrender.com](https://focusflow-nodq.onrender.com)
- Django Admin: [https://focusflow-nodq.onrender.com/admin/](https://focusflow-nodq.onrender.com/admin/)

## Demo Accounts

### Admin Users

- Username: `ozer` | Password: `admin`
- Username: `peker` | Password: `admin`
- Username: `tugce` | Password: `admin`

### Regular Users

- Username: `john.doe` | Password: `user`
- Username: `jane.smith` | Password: `user`
- Username: `alex.lee` | Password: `user`

## Project Goals

The project was built to solve common coordination problems in small teams:

- unclear task ownership
- difficulty tracking progress
- lack of visibility into blocked or overdue work
- weak separation between administrative and member-level workflows

FocusFlow addresses these issues with a single web application built on Django's model-view-template architecture.

## Core Features

### Task Management

- Create tasks through a dedicated admin workflow
- Edit existing tasks through an admin-only update screen
- View active and completed tasks
- Assign tasks to one or more users
- Mark tasks as completed
- Delete completed tasks
- Track priority and due dates

### Workflow Tracking

Each task supports a workflow-aware status model:

- `To Do`
- `In Progress`
- `Blocked`
- `Done`

Tasks also support:

- title
- description
- internal note
- due date
- priority
- multiple assignees

### Role-Based Access

- Admin users can create tasks, assign users, access dashboards, and review all tasks
- Regular users can only access tasks assigned to them
- Protected views use Django authentication and permission checks

### Search and Filtering

The task board supports filtering by:

- search query
- task status
- priority
- assignee

### Reporting and Views

- Admin dashboard with summary metrics
- Calendar view for due dates
- Incomplete task view
- Completed task archive

## Advanced Features Included

This project includes the following advanced features from the grading rubric:

- Authentication (`login` / `logout`)
- Authorization and permissions
- Search and filtering

These features satisfy the `3+ advanced features` category.

## Tech Stack

- Python 3.11
- Django 4.2.7
- SQLite
- Gunicorn
- WhiteNoise
- Jazzmin
- Bootstrap-based templates with custom CSS
- Render for deployment

## Architecture Overview

FocusFlow follows Django's standard MVT pattern:

- `Model`: defines the data structure and relationships
- `View`: handles business logic, permissions, filtering, and rendering
- `Template`: renders the user interface

The primary application is the `tasks` app, while project-level configuration lives under `gorev_sistemi`.

### Main Model

The core model is `Task`, which stores:

- `title`
- `description`
- `note`
- `due_date`
- `completed`
- `priority`
- `status`
- `assigned_to`

The relationship between `Task` and Django's built-in `User` model is `ManyToMany`, which allows:

- one task to be assigned to multiple users
- one user to be assigned to multiple tasks

### Business Logic Highlights

- `status` and `completed` are synchronized so the workflow system stays compatible with legacy completion logic
- admins and regular users receive different querysets in the task board
- filtering is centralized in a dedicated helper in the views layer
- dashboard counts are computed dynamically from ORM queries

For a deeper technical explanation, see [docs/technical-overview.md](/Users/ozeracar/Desktop/todo-list/docs/technical-overview.md).

## Project Structure

```text
todo-list/
├── gorev_sistemi/          # Project settings, root URLs, WSGI/ASGI
├── tasks/                  # Main application: models, views, forms, templates, tests
├── templates/              # Shared base and authentication templates
├── docs/                   # Technical and planning documents
├── render.yaml             # Render deployment configuration
├── requirements.txt        # Python dependencies
└── manage.py               # Django management entry point
```

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/acarozerr/FocusFlow.git
cd FocusFlow
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open the project at:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Running Tests

Run the Django test suite with:

```bash
python manage.py test
```

The current project includes tests for:

- task status synchronization
- form field exposure
- filtering behavior
- user visibility rules
- completion flow
- task editing permissions and update flow
- dashboard workflow counts

## Deployment

The application is deployed on Render.

Deployment configuration includes:

- `gunicorn gorev_sistemi.wsgi:application` as the start command
- `collectstatic` during build
- automatic migrations during deployment
- `WhiteNoise` for static asset serving
- environment-based production settings in Django

The live deployment is publicly accessible and runs independently from the local machine.

## Validation and Error Handling

The project relies on Django's built-in validation and defensive patterns:

- `ModelForm` validation for task creation
- `login_required` for protected routes
- `user_passes_test` for admin-only actions
- `get_object_or_404` for safe object access
- conditional delete permissions for completed tasks

## Current Scope Notes

The current release focuses on a strong, stable workflow experience. It includes task creation, viewing, editing, completion, filtering, reporting, and deployment.

## Team Presentation Notes

If this repository is being used for a course presentation, the most important technical topics to explain are:

- Django MVT architecture
- `Task` to `User` many-to-many relationship
- workflow status system and completion sync
- role-based permissions
- full CRUD support through create, read, update, and delete flows
- search and filtering logic
- Render deployment pipeline

## License

This project is intended for educational use as a Django term project.
