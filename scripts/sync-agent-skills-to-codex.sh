#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: sync-agent-skills-to-codex.sh [options]

Symlink repo-local agent skills into the Codex skills directory.

Options:
  --source-dir PATH  Source directory containing skill folders.
                     Default: <repo>/agent-skills
  --target-dir PATH  Target Codex skills directory.
                     Default: ${CODEX_HOME:-$HOME/.codex}/skills
  --dry-run          Print planned actions without writing files.
  -h, --help         Show this help.

Environment:
  CODEX_HOME         Overrides the default Codex home directory.
  CODEX_SKILLS_DIR   Overrides the default target skills directory.
  AGENT_SKILLS_DIR   Overrides the default source skills directory.
USAGE
}

log() {
  printf '%s\n' "$*"
}

warn() {
  printf 'warning: %s\n' "$*" >&2
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

resolve_path() {
  local path=$1

  if command -v realpath >/dev/null 2>&1; then
    realpath -- "$path"
    return
  fi

  if [ -d "$path" ]; then
    (cd -- "$path" && pwd -P)
    return
  fi

  local dir
  dir=$(dirname -- "$path")
  local base
  base=$(basename -- "$path")
  (cd -- "$dir" && printf '%s/%s\n' "$(pwd -P)" "$base")
}

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
repo_root=$(cd -- "$script_dir/.." && pwd -P)

source_dir=${AGENT_SKILLS_DIR:-"$repo_root/agent-skills"}
codex_home=${CODEX_HOME:-"$HOME/.codex"}
target_dir=${CODEX_SKILLS_DIR:-"$codex_home/skills"}
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-dir)
      [ "$#" -ge 2 ] || die "--source-dir requires a path"
      source_dir=$2
      shift 2
      ;;
    --target-dir)
      [ "$#" -ge 2 ] || die "--target-dir requires a path"
      target_dir=$2
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

[ -d "$source_dir" ] || die "source directory does not exist: $source_dir"

source_dir=$(resolve_path "$source_dir")

if [ "$dry_run" -eq 0 ]; then
  mkdir -p -- "$target_dir"
fi

target_parent=$(dirname -- "$target_dir")
if [ "$dry_run" -eq 0 ]; then
  [ -d "$target_parent" ] || die "target parent directory does not exist: $target_parent"
fi

target_dir_abs=$target_dir
if [ -d "$target_dir" ]; then
  target_dir_abs=$(resolve_path "$target_dir")
fi

log "Source: $source_dir"
log "Target: $target_dir_abs"

created=0
kept=0
skipped=0
conflicts=0
found=0

while IFS= read -r -d '' skill_dir; do
  [ -f "$skill_dir/SKILL.md" ] || continue

  found=$((found + 1))
  skill_name=$(basename -- "$skill_dir")
  skill_dir=$(resolve_path "$skill_dir")
  link_path="$target_dir/$skill_name"

  if [ -L "$link_path" ]; then
    existing_target=$(resolve_path "$link_path" 2>/dev/null || true)
    if [ "$existing_target" = "$skill_dir" ]; then
      log "keep: $skill_name -> $skill_dir"
      kept=$((kept + 1))
      continue
    fi

    warn "conflict: $link_path is a symlink to ${existing_target:-an unresolved target}"
    conflicts=$((conflicts + 1))
    continue
  fi

  if [ -e "$link_path" ]; then
    warn "conflict: $link_path already exists and is not a symlink"
    conflicts=$((conflicts + 1))
    continue
  fi

  if [ "$dry_run" -eq 1 ]; then
    log "would link: $skill_name -> $skill_dir"
  else
    ln -s -- "$skill_dir" "$link_path"
    log "linked: $skill_name -> $skill_dir"
  fi
  created=$((created + 1))
done < <(find "$source_dir" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

[ "$found" -gt 0 ] || die "no skills with SKILL.md found under: $source_dir"

log ""
log "Summary: found=$found created=$created kept=$kept skipped=$skipped conflicts=$conflicts"

if [ "$conflicts" -gt 0 ]; then
  die "resolve conflicts before Codex skill sync can be considered complete"
fi

if [ "$dry_run" -eq 1 ]; then
  log "Dry run complete; no files were changed."
else
  log ""
  log "Visible skill manifests:"
  find -L "$target_dir" -maxdepth 2 -name SKILL.md -print | sort
  log ""
  log "Open a new Codex session if the current session does not pick up new skills."
fi
