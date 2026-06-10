FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/overseer

COPY requirements.txt /opt/overseer/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/overseer/requirements.txt

COPY . /opt/overseer/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
