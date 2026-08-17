# HTTP API

All endpoints require HTTP Basic authentication. Configure credentials with `OVERSEER_USERNAME` and `OVERSEER_PASSWORD`. Requests fail closed with HTTP `503` when either value is missing. Use HTTPS whenever requests leave the local machine because Basic credentials are encoded, not encrypted.

For example:

```bash
curl --user "$OVERSEER_USERNAME:$OVERSEER_PASSWORD" \
  http://localhost:8000/api/services
```

## Dashboard

### `GET /`

Returns the HTML dashboard.

## List Containers

### `GET /api/services`

Returns containers in Overseer's Docker Compose project. Overseer detects the project from its own container label or the `OVERSEER_COMPOSE_PROJECT` environment variable. When neither is available, such as during local development outside Compose, it falls back to every container visible to the configured Docker daemon.

```json
[
  {
    "id": "1234567890ab",
    "name": "web",
    "status": "running",
    "image": "example/web:latest",
    "ports": {
      "80/tcp": [
        {"host_ip": "0.0.0.0", "host_port": "8080"}
      ]
    },
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

In addition to Basic authentication, action requests must include the following CSRF-protection header:

```text
X-Overseer-CSRF: 1
```

```bash
curl --user "$OVERSEER_USERNAME:$OVERSEER_PASSWORD" \
  --header "X-Overseer-CSRF: 1" \
  --request POST \
  http://localhost:8000/api/service/container-id/restart
```

On success, each returns:

```json
{"success": true}
```

`container_id` may be any identifier accepted by the Docker SDK, including a container ID or name. Missing containers return HTTP `404`; other Docker daemon failures return HTTP `502`. API errors use the following JSON shape:

```json
{"error": "Docker operation failed"}
```
