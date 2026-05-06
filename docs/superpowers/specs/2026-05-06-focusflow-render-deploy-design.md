# FocusFlow Render Deploy Design

## Goal

Prepare FocusFlow to run reliably on the public internet through Render with a minimal but safe deployment configuration.

## Scope

This work is limited to making the existing Django app deployable and stable enough for public access.

It includes:

- Fixing Render service configuration
- Making Django settings environment-aware for deployment
- Ensuring static files are collected and served in production
- Running deployment-oriented checks before release

It does not include:

- Migrating from SQLite to Postgres
- Splitting settings into multiple files
- Full production hardening across every Django security option
- Media upload persistence strategy

## Deployment Target

The immediate target is a single Render web service using the existing GitHub repository.

The app will run with:

- Python runtime on Render
- Gunicorn as the WSGI server
- WhiteNoise for static file serving
- SQLite retained for now

This is acceptable for a first public deployment and demos, but not the final long-term production architecture.

## Current Risks

The current project has a few concrete deployment blockers:

### Incorrect WSGI module path

The current `render.yaml` start command points to `todo_list.wsgi:application`, but the actual Django project module is `gorev_sistemi.wsgi:application`.

If left unchanged, the service will fail to boot.

### Debug mode is hardcoded on

`settings.py` currently sets `DEBUG = True` directly.

That means even if Render provides `DEBUG=False` as an environment variable, the app will still behave like a development build unless the code is changed to read from the environment.

### Static build step is incomplete

The current build command only installs requirements.

For a Django production deployment using WhiteNoise, the build should also run:

- `python manage.py collectstatic --noinput`
- `python manage.py migrate`

### Static directory warning

`STATICFILES_DIRS` currently points to a `static` folder that does not exist in the repository.

This is already generating warnings locally and should be cleaned up before deployment.

## Recommended Configuration

### Render

The Render configuration should use:

- `buildCommand`: install dependencies, collect static files, apply migrations
- `startCommand`: run Gunicorn against `gorev_sistemi.wsgi:application`

The web service should continue using environment variables for:

- `SECRET_KEY`
- `DEBUG`
- `PYTHON_VERSION`

## Django Settings Strategy

The settings should stay in one file for now, but become deployment-aware.

### Debug

`DEBUG` should be read from an environment variable rather than hardcoded.

Expected behavior:

- local development can still default to debug on if no env var is present
- Render can force production behavior with `DEBUG=False`

### Allowed hosts

`ALLOWED_HOSTS` should support:

- local development
- the Render hostname
- optional custom domain entries

It should remain simple and explicit rather than overly dynamic.

### Static files

WhiteNoise should remain in use.

Static settings should support:

- local template/CSS development
- production `collectstatic`
- serving from `STATIC_ROOT`

The invalid `STATICFILES_DIRS` entry should be removed or made conditional so Django does not warn about a missing directory.

## Verification

Before saying the app is deployment-ready, the following checks should pass locally:

- `python manage.py test`
- `python manage.py check --deploy`
- `python manage.py collectstatic --noinput`

This gives confidence that:

- code still works
- production settings are sane
- static assets build correctly

## Tradeoff Note

SQLite is being kept temporarily because the goal is to get the app publicly reachable with minimal rework.

That is fine for:

- demos
- early project reviews
- light traffic

But later, a stronger deployment version should move to Postgres and a persistent data strategy.

## Implementation Shape

Expected files include:

- `render.yaml`
- `gorev_sistemi/settings.py`
- small supporting changes only if deployment checks reveal concrete blocking warnings

The safest order is:

1. Fix Render commands
2. Make settings deployment-aware
3. Clean static settings
4. Run deploy checks
5. Push and deploy on Render
