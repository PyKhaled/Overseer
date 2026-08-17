# Development

## Set Up

Python 3.11 is used by the production image. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The app needs access to a Docker daemon. `docker.from_env()` honors standard Docker environment variables and commonly connects to the local socket.

## Run Locally

```bash
export OVERSEER_USERNAME=admin
export OVERSEER_PASSWORD='replace-with-a-strong-password'
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

Tests use `unittest.mock` to replace the Docker client. New tests must not operate on real containers. Name test modules `test_*.py` and cover both the response and the expected Docker SDK call.

Before opening a pull request, run the tests and verify the image builds:

```bash
docker build -t overseer .
```

GitHub Actions repeats these checks on pushes to `main`, `release/**`, and semantic-version tags, on pull requests, and when manually dispatched. The test job covers Python 3.11, 3.12, and 3.13; a separate job builds the production image. The package-publishing workflow also runs tests before pushing an image.
