# Contributing

Thank you for improving Overseer.

## Before You Start

- Use GitHub Discussions for design questions and support.
- Open an issue before beginning a large or behavior-changing contribution.
- Report security vulnerabilities privately as described in
  [`SECURITY.md`](SECURITY.md), not in a public issue.

## Development

Create a virtual environment with Python 3.11 or newer and install the
development dependency group:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade "pip>=25.1"
python -m pip install --group dev
python -m pip uninstall --yes setuptools
```

Run the complete quality gate before submitting a pull request:

```bash
ruff check .
ruff format --check .
coverage run -m unittest discover -s tests -v
coverage report
python -m pip_audit
docker compose --env-file /dev/null config --quiet
docker build -t overseer:contributor .
```

Tests must mock the Docker client and must not modify real containers.

## Pull Requests

1. Create a focused branch from the latest `main`.
2. Include tests and documentation for behavior changes.
3. Describe user-visible and security implications in the pull request.
4. Keep commits reviewable and do not include generated files, environments,
   credentials, or unrelated formatting changes.
5. Wait for every required check to pass before merging.

Contributions are accepted under the repository's MIT License.
