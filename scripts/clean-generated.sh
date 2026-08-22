#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_directory/.." && pwd)"
cd "$project_root"

printf 'This removes generated caches and coverage output from:\n  %s\n' \
  "$project_root"
printf 'The virtual environment and source files are preserved.\n\n'
printf 'Type CLEAN to continue: '
read -r confirmation

if [[ "$confirmation" != "CLEAN" ]]; then
  printf 'Cleanup cancelled.\n'
  exit 0
fi

make clean
printf 'Generated files removed.\n'
