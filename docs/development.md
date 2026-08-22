# Development

## Set Up

Python 3.14 is used by the production image, and CI tests Python 3.11 through
3.14. Dependencies are defined in `pyproject.toml`. Create a virtual
environment with a supported Python version, ensure pip 25.1 or newer is
installed, and install the development dependency group:

```bash
make setup PYTHON=python3.14
```

Setuptools is removed after installation because Overseer does not need it at
runtime and the newest available release is affected by a known vulnerability.
Set `PYTHON` to the command for any supported Python 3.11–3.14 interpreter.
The Make targets call `.venv/bin/python` directly, so activating the virtual
environment is optional.

Use `python -m pip install --group runtime` when only the production dependencies are needed.

The app needs access to a Docker daemon. `docker.from_env()` honors standard Docker environment variables and commonly connects to the local socket.

## Run Locally

```bash
make run
```

Open `http://localhost:8000`. The development server binds to `127.0.0.1` with debug mode disabled by default. Set `OVERSEER_DEBUG=1` or `OVERSEER_HOST` only when you explicitly need different local-development behavior.

To exercise the production server locally:

```bash
make serve
```

## Test

Run the complete suite with:

```bash
make test
```

Run the same quality and security checks used by CI:

```bash
make check
```

Tests use `unittest.mock` to replace the Docker client. New tests must not operate on real containers. Name test modules `test_*.py` and cover both the response and the expected Docker SDK call.

Before opening a pull request, run the checks and verify the image builds:

```bash
make image
make smoke
```

## Command Reference

Run `make help` for the current command list. The main targets are:

| Target | Purpose |
| --- | --- |
| `setup` | Create `.venv` and install the development dependency group. |
| `run` / `serve` | Start the Flask development server or Gunicorn. |
| `test` / `coverage` | Run unit tests, optionally enforcing coverage. |
| `lint` / `format-check` | Run the non-mutating source checks. |
| `format` | Apply Ruff's safe lint fixes and formatter. |
| `audit` / `compose-check` | Check dependencies and Compose configuration. |
| `check` | Run the complete local quality gate used by CI. |
| `image` / `smoke` | Build and verify the production container. |
| `compose-up` / `compose-down` / `compose-logs` | Operate the example stack. |
| `clean` | Remove generated caches and coverage output; it preserves `.venv`. |

`IMAGE`, `SMOKE_CONTAINER`, and `SMOKE_PORT` can override the container defaults.
For example, use `make smoke SMOKE_PORT=8088` when port 8000 is occupied.

GitHub Actions runs quality checks, dependency auditing, tests on Python
3.11–3.14, a container vulnerability scan, and a live container smoke test on
pull requests and pushes to `main`. Published GitHub Releases rerun the same
workflow before publishing a multi-platform image. A scheduled workflow runs
CodeQL, dependency auditing, and container scanning every Monday.
