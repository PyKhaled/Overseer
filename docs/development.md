# Development

## Set Up

Python 3.14 is used by the production image, and CI tests Python 3.11 through
3.14. Dependencies are defined in `pyproject.toml`. Create a virtual
environment with a supported Python version, ensure pip 25.1 or newer is
installed, and install the development dependency group:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade "pip>=25.1"
python -m pip install --group dev
python -m pip uninstall --yes setuptools
```

Setuptools is removed after installation because Overseer does not need it at
runtime and the newest available release is affected by a known vulnerability.

Use `python -m pip install --group runtime` when only the production dependencies are needed.

The app needs access to a Docker daemon. `docker.from_env()` honors standard Docker environment variables and commonly connects to the local socket.

## Run Locally

```bash
python -m overseer
```

Open `http://localhost:8000`. The development server binds to `127.0.0.1` with debug mode disabled by default. Set `OVERSEER_DEBUG=1` or `OVERSEER_HOST` only when you explicitly need different local-development behavior.

To exercise the production server locally:

```bash
gunicorn --bind 0.0.0.0:8000 --workers 2 overseer:app
```

## Test

Run the complete suite with:

```bash
python -m unittest discover -s tests -v
```

Run the same quality and security checks used by CI:

```bash
ruff check .
ruff format --check .
coverage run -m unittest discover -s tests -v
coverage report
python -m pip_audit
docker compose --env-file /dev/null config --quiet
```

Tests use `unittest.mock` to replace the Docker client. New tests must not operate on real containers. Name test modules `test_*.py` and cover both the response and the expected Docker SDK call.

Before opening a pull request, run the checks and verify the image builds:

```bash
docker build -t overseer .
```

GitHub Actions runs quality checks, dependency auditing, tests on Python
3.11–3.14, a container vulnerability scan, and a live container smoke test on
pull requests and pushes to `main`. Published GitHub Releases rerun the same
workflow before publishing a multi-platform image. A scheduled workflow runs
CodeQL, dependency auditing, and container scanning every Monday.
