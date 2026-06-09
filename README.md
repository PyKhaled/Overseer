# Overseer

Overseer is a lightweight project observability and control service for Docker Compose applications.

Drop Overseer into your existing Docker Compose stack and instantly gain visibility into the services that make up your project.

Unlike container management tools that focus on the entire Docker host, Overseer focuses on a single application stack and provides a project-centric view of your services.

---

## Features

### Service Discovery

Automatically discovers services running under the same Docker Compose project.

### Service Control

- Start services
- Stop services
- Restart services

### Service Visibility

View:

- Running services
- Stopped services
- Container status
- Images
- Container identifiers

### Project-Oriented

Overseer groups services by Docker Compose project, making it easier to understand and manage a complete application stack.

---

## Quick Start

Add Overseer to your existing `docker-compose.yml`.

```yaml
services:
  overseer:
    image: pykhaled/overseer:latest
    restart: unless-stopped
    ports:
      - "8000:5000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

Start your stack:

```bash
docker compose up -d
```

Open:

```text
http://localhost:8000
```

---

## Example

```yaml
services:
  overseer:
    image: pykhaled/overseer:latest

  frontend:
    image: my-frontend

  backend:
    image: my-backend

  mongo:
    image: mongo

  redis:
    image: redis
```

Overseer automatically discovers the services belonging to the project and provides a centralized view of their state.

---

## Why Overseer?

Most Docker tools are host-centric.

Overseer is project-centric.

Instead of showing every container on the machine, Overseer helps you understand:

- What services belong to this application
- Which services are healthy
- Which services are consuming resources
- How services relate to one another

---

## Roadmap

Planned features include:

- CPU and memory metrics
- Live logs
- Health checks
- Service dependency graph
- Docker events stream
- Project metadata
- Multi-host support
- User authentication
- Alerting and notifications

---

## Security

Overseer requires access to the Docker socket:

```text
/var/run/docker.sock
```

This allows Overseer to inspect and manage Docker containers on the host.

Deploy Overseer only in trusted environments.

---

## License

MIT