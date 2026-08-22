# Releasing

Overseer releases are published from GitHub Releases. Publishing a release
whose tag is a valid semantic version starts `.github/workflows/release.yml`.
The workflow reruns CI and, if verification succeeds, publishes the container
image to the GitHub Container Registry (GHCR).

## Prerequisites

- You can create releases in `PyKhaled/Overseer` and publish packages for the
  repository.
- The release commit has been merged into `main`.
- The CI workflow is passing for that commit.
- The tag is unused and follows `vMAJOR.MINOR.PATCH`, for example `v1.4.0`.
  SemVer prerelease and build suffixes are also accepted, such as
  `v1.4.0-rc.1`.

The Git tag is the project's version; there is no separate version field to
update in the Python package.

## Prepare the Release

1. Confirm that all changes intended for the release are merged into `main`.
2. Choose the next version according to [Semantic Versioning](https://semver.org/):
   increment the major version for incompatible changes, the minor version for
   backward-compatible features, or the patch version for fixes.
3. Check the CI run for the exact commit being released. You can also run the
   local quality gate described in [Development](development.md#test).
4. Review the commits since the previous release and write release notes that
   call out user-visible changes, breaking changes, and required migration or
   deployment steps.

## Publish from GitHub

1. Open the repository's **Releases** page and select **Draft a new release**.
2. Create a new tag using the chosen version and target the exact commit on
   `main` that passed CI. Do not select a release branch or an unmerged commit.
3. Use the tag as the title, generate or enter the release notes, and edit them
   as needed.
4. For a release candidate or other prerelease, select **Set as a pre-release**.
5. Review the draft, then select **Publish release**.

Publishing—not merely saving a draft—starts the release workflow. The same
operation can be performed with GitHub CLI. Fetch the current remote state,
then replace the sample version with an unused version:

```bash
git fetch origin main --tags
RELEASE_COMMIT="$(git rev-parse origin/main)"
gh release create v1.4.0 \
  --target "$RELEASE_COMMIT" \
  --title "v1.4.0" \
  --generate-notes \
  --fail-on-no-commits
```

Add `--prerelease` for a prerelease. If the release notes need manual editing,
create and review a draft first by adding `--draft`, then publish it from the
GitHub Releases page.

## What the Workflow Publishes

The release workflow first validates the tag and confirms that its commit is
contained in `main`. It then runs the complete CI workflow. Only after those
checks pass does it build and push one image manifest supporting `linux/amd64`
and `linux/arm64`.

For a stable `v1.4.2` release, GHCR receives these tags:

- `1.4.2`
- `1.4`
- `1` (major tags are omitted for `v0.x.y` releases)
- `sha-<full-commit-sha>`
- `latest`

Prereleases never update `latest`. Published images also include an SBOM,
build provenance, and a GitHub artifact attestation.

## Verify the Release

1. Open the **Release** workflow run and confirm that both the verification and
   publishing jobs passed.
2. Confirm that the release appears on the repository's Releases page with the
   intended tag and notes.
3. Inspect the published multi-platform manifest:

   ```bash
   docker buildx imagetools inspect ghcr.io/pykhaled/overseer:1.4.2
   ```

4. Pull the immutable version tag on a supported machine before announcing the
   release:

   ```bash
   docker pull ghcr.io/pykhaled/overseer:1.4.2
   ```

Use the exact version tag for this check rather than `latest`, especially when
verifying a prerelease.

## If a Release Fails

- For an intermittent GitHub, registry, or runner failure, rerun all failed
  jobs from the release workflow run.
- For an invalid tag or a tag whose commit is not on `main`, create a correctly
  targeted release with a new version.
- For a code, dependency, or workflow failure, merge the fix into `main`, wait
  for CI to pass, and publish a new patch release.

Do not move or reuse a published version tag. Consumers may already have pulled
that tag, and changing it would make the release non-reproducible. If a
published image is defective, document the problem in its release notes and
supersede it with a new patch version.
