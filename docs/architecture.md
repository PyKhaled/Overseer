# Architecture

## Components

The `overseer` Python package contains the application:

- `overseer/__init__.py` exports the Flask application and `create_app()` factory.
- `overseer/__main__.py` provides the `python -m overseer` development entry point.
- `overseer/app.py` defines routes and translates Docker SDK objects into JSON-safe data.
- `overseer/templates/index.html` is the dashboard UI. It polls the services endpoint every five seconds and sends lifecycle actions.

Gunicorn imports `overseer:app` in the production container. Flask renders the dashboard, while the Docker SDK connects using `docker.from_env()`—normally through a mounted Unix socket.

## Request Flow

1. The browser requests `/` and receives the dashboard.
2. The dashboard requests `GET /api/services`.
3. Overseer detects its Compose project, queries matching containers, and serializes container identity, state, image, ports, start time, and uptime.
4. A lifecycle button sends an authenticated, CSRF-protected `POST` request; Overseer verifies that the target belongs to the detected Compose project before invoking the Docker SDK operation.

## Current Boundaries

The current implementation filters by the `com.docker.compose.project` label when it can detect a project from its own container or from `OVERSEER_COMPOSE_PROJECT`. It falls back to all visible containers for local, non-Compose development. HTTP Basic authentication protects all endpoints, and a custom request header protects lifecycle actions from cross-site form submissions. The application does not yet provide multiple users, roles, or event streaming. Keep Docker-specific behavior in helper functions so routes remain straightforward to test.
