# Deployment and Security

## Container Image

Build and run the image from the repository root:

```bash
docker build -t overseer .
docker run --rm -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  overseer
```

The image runs Gunicorn on port `8000` with two workers. Published images are built by `.github/workflows/docker-image.yml` when changes reach the `release` branch.

## Docker Socket Access

Access to `/var/run/docker.sock` is effectively administrative access to the Docker host. A process with socket access can inspect containers, mount host paths, and create privileged workloads.

- Deploy Overseer only on trusted networks.
- Put authentication and TLS at a reverse proxy before allowing remote access.
- Do not expose port `8000` directly to the public internet.
- Avoid mounting the socket into unrelated containers.
- Review changes to lifecycle routes as security-sensitive code.

Overseer currently has no built-in authentication, authorization, or CSRF protection. Its control endpoints should therefore be considered trusted-administrator interfaces.
