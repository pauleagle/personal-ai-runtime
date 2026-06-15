#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: render-mermaid-figures.sh [options]

Render Mermaid source drafts with a repo-local Mermaid CLI install.

Options:
  --input-dir PATH   Directory containing .mmd files.
                     Default: current working directory.
  --output-dir PATH  Directory for rendered SVG files.
                     Default: /tmp/mermaid-render-check
  --file PATH        Render one .mmd file instead of all files in input-dir.
  -h, --help         Show this help.

Expected local tools:
  .tools/node-v22.16.0-linux-x64/bin/node
  .tools/mermaid-cli/node_modules/.bin/mmdc
  .tools/chrome-libs/usr/lib/x86_64-linux-gnu
  .tools/mermaid-puppeteer-config.json

This script does not install dependencies and does not write rendered figures
into the repository by default.
USAGE
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
repo_root=$(cd -- "$script_dir/.." && pwd -P)

input_dir=$PWD
output_dir=/tmp/mermaid-render-check
single_file=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --input-dir)
      [ "$#" -ge 2 ] || die "--input-dir requires a path"
      input_dir=$2
      shift 2
      ;;
    --output-dir)
      [ "$#" -ge 2 ] || die "--output-dir requires a path"
      output_dir=$2
      shift 2
      ;;
    --file)
      [ "$#" -ge 2 ] || die "--file requires a path"
      single_file=$2
      shift 2
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

node_bin="$repo_root/.tools/node-v22.16.0-linux-x64/bin"
mmdc="$repo_root/.tools/mermaid-cli/node_modules/.bin/mmdc"
chrome_libs="$repo_root/.tools/chrome-libs/usr/lib/x86_64-linux-gnu"
puppeteer_config="$repo_root/.tools/mermaid-puppeteer-config.json"

[ -x "$node_bin/node" ] || die "missing local Node install: $node_bin/node"
[ -x "$mmdc" ] || die "missing Mermaid CLI: $mmdc"
[ -d "$chrome_libs" ] || die "missing Chrome runtime libs: $chrome_libs"
[ -f "$puppeteer_config" ] || die "missing Puppeteer config: $puppeteer_config"

mkdir -p -- "$output_dir"

render_one() {
  local file=$1
  [ -f "$file" ] || die "input file does not exist: $file"

  local base
  base=$(basename -- "$file" .mmd)
  printf 'render %s\n' "$base"
  env PATH="$node_bin:$PATH" \
    LD_LIBRARY_PATH="$chrome_libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    "$mmdc" \
    -p "$puppeteer_config" \
    -i "$file" \
    -o "$output_dir/$base.svg"
}

if [ -n "$single_file" ]; then
  render_one "$single_file"
else
  [ -d "$input_dir" ] || die "input directory does not exist: $input_dir"
  found=0
  while IFS= read -r -d '' file; do
    found=$((found + 1))
    render_one "$file"
  done < <(find "$input_dir" -maxdepth 1 -type f -name '*.mmd' -print0 | sort -z)
  [ "$found" -gt 0 ] || die "no .mmd files found in: $input_dir"
fi

printf 'Rendered SVG files in: %s\n' "$output_dir"
