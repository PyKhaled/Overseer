# Deployment and Security

## Container Image

Build and run the image from the repository root:

```bash
docker build -t overseer .
docker run --rm -p 8000:8000 \
  -e OVERSEER_USERNAME=admin \
  -e OVERSEER_PASSWORD='replace-with-a-strong-password' \
  -v /var/run/docker.sock:/var/run/docker.sock \
  overseer
```

The image runs Gunicorn on port `8000` with two workers. Published images are built by `.github/workflows/docker-image.yml` for `release/**` branches and semantic-version tags such as `v1.0.0`. The publishing job runs the tests first. Tagged releases publish version, major/minor, and `latest` tags to `ghcr.io/<owner>/<repository>`.

## Authentication

Set both `OVERSEER_USERNAME` and `OVERSEER_PASSWORD`. Overseer returns HTTP `503` without them and requires HTTP Basic authentication for the dashboard and API. Use a long, unique password and terminate TLS at a trusted reverse proxy before allowing network access; Basic authentication does not encrypt credentials.

## Compose Project Detection

When Overseer runs as part of a Compose application, it reads the `com.docker.compose.project` label from its own container and lists only containers with the same label. Set `OVERSEER_COMPOSE_PROJECT` to override automatic detection:

```yaml
services:
  overseer:
    image: ghcr.io/pykhaled/overseer:latest
    environment:
      OVERSEER_COMPOSE_PROJECT: my-application
```

When no project can be detected, Overseer lists every container visible through the configured Docker daemon.

## Docker Socket Access

Access to `/var/run/docker.sock` is effectively administrative access to the Docker host. A process with socket access can inspect containers, mount host paths, and create privileged workloads.

- Deploy Overseer only on trusted networks.
- Put TLS at a trusted reverse proxy before allowing remote access.
- Do not expose port `8000` directly to the public internet.
- Avoid mounting the socket into unrelated containers.
- Review changes to lifecycle routes as security-sensitive code.

Overseer provides one administrator credential pair, rejects state-changing requests without its custom CSRF header, and restricts lifecycle actions to the detected Compose project. It does not provide per-user roles or eliminate the host-level risk of mounting the Docker socket, so it should still be treated as a trusted-administrator interface.
