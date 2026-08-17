# Deployment and Security

## Container Image

Build and run the image from the repository root:

```bash
docker build -t overseer .
docker run --rm -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  overseer
```

The image runs Gunicorn on port `8000` with two workers. Published images are built by `.github/workflows/docker-image.yml` for `release/**` branches and semantic-version tags such as `v1.0.0`. The publishing job runs the tests first. Tagged releases publish version, major/minor, and `latest` tags to `ghcr.io/<owner>/<repository>`.

## Compose Project Detection

When Overseer runs as part of a Compose application, it reads the `com.docker.compose.project` label from its own container and lists other containers with the same label. The Overseer container itself is excluded. Set `OVERSEER_COMPOSE_PROJECT` to override automatic detection:

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
- Put authentication and TLS at a trusted reverse proxy before allowing remote access.
- Do not expose port `8000` directly to the public internet.
- Avoid mounting the socket into unrelated containers.
- Review changes to lifecycle routes as security-sensitive code.

Overseer has no built-in authentication. It rejects state-changing requests without its custom CSRF header and restricts lifecycle actions to the detected Compose project, but this does not eliminate the host-level risk of mounting the Docker socket. Treat it as a trusted-administrator interface.
