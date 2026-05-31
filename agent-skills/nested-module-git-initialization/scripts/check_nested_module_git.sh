#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_script="$script_dir/check_nested_module_git.py"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$python_script" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$python_script" "$@"
fi

printf '%s\n' 'Python 3 is required to run check_nested_module_git.sh.' >&2
exit 127
