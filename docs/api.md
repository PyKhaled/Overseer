# HTTP API

The API currently has no authentication. Run it only in a trusted environment.

## Dashboard

### `GET /`

Returns the HTML dashboard.

## List Containers

### `GET /api/services`

Returns every container visible to the configured Docker daemon.

```json
[
  {
    "id": "1234567890ab",
    "name": "web",
    "status": "running",
    "image": "example/web:latest",
    "ports": {"80/tcp": ["0.0.0.0:8080"]},
    "started_at": "2026-08-10T10:00:00+00:00",
    "uptime": "1:05:12.345678"
  }
]
```

Exposed but unpublished ports have a `null` value.

## Container Actions

The following endpoints accept `POST` requests:

- `/api/service/<container_id>/start`
- `/api/service/<container_id>/stop`
- `/api/service/<container_id>/restart`

On success, each returns:

```json
{"success": true}
```

`container_id` may be any identifier accepted by the Docker SDK, including a container ID or name. The application currently allows Docker exceptions to propagate as server errors; clients should treat non-2xx responses as failed actions.
