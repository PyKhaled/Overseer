#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_directory/.." && pwd)"
cd "$project_root"

release_tag="${1:-}"
semver_pattern='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-((0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?$'

if [[ ! "$release_tag" =~ $semver_pattern ]]; then
  printf 'Usage: %s vMAJOR.MINOR.PATCH\n' "$0" >&2
  exit 2
fi

for command_name in git gh docker; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Error: required command is not installed: %s\n' "$command_name" >&2
    exit 1
  fi
done

gh auth status >/dev/null
gh release view "$release_tag" >/dev/null

printf 'Fetching release tag %s...\n' "$release_tag"
git fetch origin tag "$release_tag"
release_commit="$(git rev-list -n 1 "$release_tag")"

run_details="$(
  gh run list \
    --workflow release.yml \
    --event release \
    --commit "$release_commit" \
    --limit 1 \
    --json databaseId,url \
    --jq '(.[0] // empty) | "\(.databaseId)|\(.url)"'
)"

if [[ -z "$run_details" ]]; then
  printf 'Error: no Release workflow run found for %s.\n' "$release_tag" >&2
  exit 1
fi

IFS='|' read -r run_id run_url <<< "$run_details"
printf 'Watching Release workflow: %s\n' "$run_url"
gh run watch "$run_id" --exit-status

repository="$(gh repo view --json nameWithOwner --jq .nameWithOwner | tr '[:upper:]' '[:lower:]')"
image_tag="${release_tag#v}"
image="ghcr.io/$repository:$image_tag"

printf '\nInspecting published multi-platform image %s...\n' "$image"
docker buildx imagetools inspect "$image"

release_url="$(gh release view "$release_tag" --json url --jq .url)"
printf '\nRelease verified: %s\n' "$release_url"
