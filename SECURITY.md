# Security Policy

## Supported Versions

The most recent stable release receives security fixes. Older releases and
development snapshots are not supported.

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub's
**Security** tab and select **Report a vulnerability** to send a private report
to the maintainers:

https://github.com/PyKhaled/Overseer/security/advisories/new

Include the affected version or commit, reproduction steps, impact, and any
suggested mitigation. Reports should receive an acknowledgement within three
business days and a status update within seven business days.

Please allow time for a fix and coordinated disclosure before publishing
details. If the report is accepted, the maintainers will prepare a patched
release and credit the reporter unless anonymity is requested.

## Deployment Boundary

Overseer mounts the Docker socket and has no built-in authentication. Docker
socket access is effectively administrative access to the host. Deploy
Overseer only on trusted networks and place authentication and TLS at a trusted
reverse proxy before allowing remote access.
