# Changelog

All notable changes to Overseer are documented here. Releases follow
[Semantic Versioning](https://semver.org/).

## Unreleased

## [3.0.0] - 2026-08-22

### Added

- Redesigned operational dashboard and service controls with improved
  accessibility, responsive layouts, clearer status information, and safer
  action feedback.
- Sentinel Lens branding, including light and dark logos, favicons, and app
  icons.
- A hosted MkDocs documentation site published through GitHub Pages.
- A Make-based development workflow for environment setup, quality checks,
  local serving, image builds, and container smoke tests.

### Changed

- **Breaking:** The application now listens on port `8765` by default instead
  of `8000`. Update Compose port mappings, reverse-proxy targets, health checks,
  and `OVERSEER_PORT` overrides as needed.
- The repository now focuses on integrating Overseer into an existing Compose
  project and no longer ships the example application stack.

## [2.0.0] - 2026-08-22

### Added

- Project dashboard with aggregate CPU and memory usage.
- Interactive Docker Compose dependency graph.
- Dedicated service-control view and project-aware lifecycle operations.
- Health endpoint, container smoke tests, dependency auditing, CodeQL, and
  container vulnerability scanning.
- Multi-platform release workflow with SBOMs, provenance, and attestations.

### Changed

- Dependencies are managed through `pyproject.toml` dependency groups.
- The production image now uses pinned Python 3.14 and dependency versions.
- Release publishing is triggered by semantic-versioned GitHub Releases.

### Removed

- Built-in authentication. Deployments must provide authentication and TLS at
  a trusted reverse proxy before exposing Overseer remotely.

## [1.0.2] - 2026-08-17

- Published release-branch images for AMD64 and ARM64 under the historical
  `release-1.0.2` GHCR tag.

## [1.0.1] - 2026-08-17

- Added ARM64 support to the container build.

This version was tagged but did not have a corresponding GitHub Release.

## [0.1.0] - 2026-08-10

- Packaged the Flask application.
- Added initial project documentation, tests, and continuous integration.

[3.0.0]: https://github.com/PyKhaled/Overseer/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/PyKhaled/Overseer/compare/v1.0.2...v2.0.0
[1.0.2]: https://github.com/PyKhaled/Overseer/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/PyKhaled/Overseer/compare/v0.1.0...v1.0.1
[0.1.0]: https://github.com/PyKhaled/Overseer/releases/tag/v0.1.0
