# Repository Guidelines

## Project Structure & Module Organization

Overseer is a small Flask service for inspecting and controlling Docker containers. Backend routes and Docker SDK helpers live in `overseer/app.py`. The package entry point is `overseer/__main__.py`. The dashboard is the single Jinja template at `templates/index.html`, and static project images are under `assets/images/`. Deployment files are at the repository root: `Dockerfile`, `docker-compose.yml`, and `requirements.txt`. The image-publishing workflow is in `.github/workflows/docker-image.yml`.

Keep backend logic in focused functions in `overseer/app.py`; place additional templates in `templates/` and browser assets in `assets/`. If the application grows substantially, split routes and Docker helpers into separate modules rather than expanding one large file.

## Build, Test, and Development Commands

- `python -m venv .venv && source .venv/bin/activate` creates and activates a local environment.
- `pip install -r requirements.txt` installs Flask, the Docker SDK, and Gunicorn.
- `python -m overseer` runs the debug server at `http://localhost:8000`; Docker access must be available through the local environment.
- `docker compose up --build` builds and starts Overseer plus the example Grafana and MailHog services.
- `docker compose down` stops the development stack.
- `docker build -t overseer .` verifies the production image builds successfully.

## Coding Style & Naming Conventions

Use four-space indentation and follow PEP 8 for Python. Name functions and variables with `snake_case`, constants with `UPPER_SNAKE_CASE`, and keep route handlers short. Use descriptive helper names such as `inspect_container`. Preserve the existing HTML/CSS/JavaScript formatting in `templates/index.html`. No formatter or linter is configured, so review diffs for consistent imports, whitespace, and trailing spaces.

## Testing Guidelines

Tests use the standard-library `unittest` framework. Run them with `python -m unittest discover -s tests -v`. Add cases under `tests/` using names such as `test_services_returns_containers.py`. Mock the Docker client; tests must not start, stop, or restart real containers. There is no coverage threshold. Before submitting, exercise affected API endpoints locally and build the Docker image.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries such as `Enhance container inspection...` and `Add MIT License...`. Follow that style, keep each commit focused, and explain non-obvious behavior in the body. Pull requests should include a concise problem/solution description, verification steps, linked issues when applicable, and screenshots for dashboard changes. Call out Docker socket, port, dependency, or deployment changes explicitly.

## Security & Configuration

Mounting `/var/run/docker.sock` grants powerful host-level access. Never expose Overseer to an untrusted network, commit secrets, or add container-control endpoints without validating identifiers and considering authorization.
