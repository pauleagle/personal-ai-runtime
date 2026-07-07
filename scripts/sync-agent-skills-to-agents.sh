#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: sync-agent-skills-to-agents.sh [options]

Symlink repo-local agent skills into each agent's skills directory
(Codex and Claude Code by default).

Options:
  --source-dir PATH  Source directory containing skill folders.
                     Default: <repo>/agent-skills
  --agents LIST      Comma-separated agents to sync (codex,claude).
                     Default: codex,claude
  --dry-run          Print planned actions without writing files.
  -h, --help         Show this help.

Environment:
  AGENT_SKILLS_DIR   Overrides the default source skills directory.
  CODEX_HOME         Overrides the default Codex home directory.
  CODEX_SKILLS_DIR   Overrides the default Codex skills directory.
  CLAUDE_HOME        Overrides the default Claude home directory.
  CLAUDE_SKILLS_DIR  Overrides the default Claude skills directory.
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
codex_skills_dir=${CODEX_SKILLS_DIR:-"$codex_home/skills"}
claude_home=${CLAUDE_HOME:-"$HOME/.claude"}
claude_skills_dir=${CLAUDE_SKILLS_DIR:-"$claude_home/skills"}
agents="codex,claude"
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-dir)
      [ "$#" -ge 2 ] || die "--source-dir requires a path"
      source_dir=$2
      shift 2
      ;;
    --agents)
      [ "$#" -ge 2 ] || die "--agents requires a comma-separated list"
      agents=$2
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

target_dir_for_agent() {
  case "$1" in
    codex) printf '%s\n' "$codex_skills_dir" ;;
    claude) printf '%s\n' "$claude_skills_dir" ;;
    *) die "unknown agent: $1 (expected codex or claude)" ;;
  esac
}

[ -d "$source_dir" ] || die "source directory does not exist: $source_dir"

source_dir=$(resolve_path "$source_dir")

total_conflicts=0
total_found=0

sync_to_target() {
  local agent=$1
  local target_dir=$2

  if [ "$dry_run" -eq 0 ]; then
    mkdir -p -- "$target_dir"
  fi

  local target_dir_abs=$target_dir
  if [ -d "$target_dir" ]; then
    target_dir_abs=$(resolve_path "$target_dir")
  fi

  log "== $agent =="
  log "Source: $source_dir"
  log "Target: $target_dir_abs"

  local created=0
  local kept=0
  local conflicts=0
  local found=0
  local skill_dir skill_name link_path existing_target

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

  log "Summary ($agent): found=$found created=$created kept=$kept conflicts=$conflicts"
  log ""

  total_conflicts=$((total_conflicts + conflicts))
  total_found=$found
}

IFS=',' read -r -a agent_list <<< "$agents"
[ "${#agent_list[@]}" -gt 0 ] || die "--agents list is empty"

for agent in "${agent_list[@]}"; do
  agent=$(printf '%s' "$agent" | tr -d '[:space:]')
  [ -n "$agent" ] || continue
  target_dir=$(target_dir_for_agent "$agent")
  sync_to_target "$agent" "$target_dir"
done

[ "$total_found" -gt 0 ] || die "no skills with SKILL.md found under: $source_dir"

if [ "$total_conflicts" -gt 0 ]; then
  die "resolve conflicts before agent skill sync can be considered complete"
fi

if [ "$dry_run" -eq 1 ]; then
  log "Dry run complete; no files were changed."
else
  log "Open a new agent session if the current session does not pick up new skills."
fi
