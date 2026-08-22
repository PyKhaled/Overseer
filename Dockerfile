FROM python:3.14-slim@sha256:ce40764625a4ff50df3548277632e7f96c4e77fe75fa848aae9885476e7df5a4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/overseer

COPY pyproject.toml /opt/overseer/pyproject.toml

RUN python -m pip install --no-cache-dir --upgrade "pip==26.2.1"
RUN python -m pip install --no-cache-dir --group runtime
RUN python -m pip uninstall --yes setuptools

COPY overseer/ /opt/overseer/overseer

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "overseer:app"]
