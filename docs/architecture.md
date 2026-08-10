# Architecture

## Components

The `overseer` Python package contains the application:

- `overseer/__init__.py` exports the Flask application and `create_app()` factory.
- `overseer/__main__.py` provides the `python -m overseer` development entry point.
- `overseer/app.py` defines routes and translates Docker SDK objects into JSON-safe data.
- `templates/index.html` is the dashboard UI. It polls the services endpoint every five seconds and sends lifecycle actions.

Gunicorn imports `overseer:app` in the production container. Flask renders the dashboard, while the Docker SDK connects using `docker.from_env()`—normally through a mounted Unix socket.

## Request Flow

1. The browser requests `/` and receives the dashboard.
2. The dashboard requests `GET /api/services`.
3. Overseer queries Docker and serializes container identity, state, image, ports, start time, and uptime.
4. A lifecycle button sends a `POST` request; Overseer invokes the corresponding Docker SDK operation.

## Current Boundaries

The current implementation lists all containers visible to the connected Docker daemon. It does not yet filter by Compose project, authenticate users, stream events, or normalize Docker errors into API responses. Keep Docker-specific behavior in helper functions so routes remain straightforward to test.
