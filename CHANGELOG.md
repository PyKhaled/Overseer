# Changelog

All notable changes to Overseer are documented here. Releases follow
[Semantic Versioning](https://semver.org/).

## Unreleased

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

[2.0.0]: https://github.com/PyKhaled/Overseer/compare/v1.0.2...v2.0.0
[1.0.2]: https://github.com/PyKhaled/Overseer/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/PyKhaled/Overseer/compare/v0.1.0...v1.0.1
[0.1.0]: https://github.com/PyKhaled/Overseer/releases/tag/v0.1.0
