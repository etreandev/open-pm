#!/usr/bin/env bash
# Install OpenPM skills by symlinking them into each agent's global skills dir.
# Usage: ./install.sh [--uninstall] [claude|antigravity|all]   (default: all)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTION="install"
[[ "${1:-}" == "--uninstall" ]] && { ACTION="uninstall"; shift; }
TARGET="${1:-all}"

declare -a DIRS=()
case "$TARGET" in
  claude)      DIRS=("$HOME/.claude/skills") ;;
  antigravity) DIRS=("$HOME/.gemini/config/skills") ;;
  all)         DIRS=("$HOME/.claude/skills" "$HOME/.gemini/config/skills") ;;
  *) echo "Unknown target: $TARGET (use claude | antigravity | all)" >&2; exit 2 ;;
esac

for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
  for skill in "$REPO"/skills/*/; do
    name="$(basename "$skill")"
    link="$dir/$name"
    if [[ "$ACTION" == "uninstall" ]]; then
      if [[ -L "$link" ]]; then rm "$link" && echo "removed  $link"; fi
      continue
    fi
    if [[ -e "$link" && ! -L "$link" ]]; then
      echo "skip     $link (exists and is not a symlink; remove it manually)" >&2
      continue
    fi
    ln -sfn "${skill%/}" "$link" && echo "linked   $link -> ${skill%/}"
  done
done

if [[ "$ACTION" == "install" ]]; then
  echo
  echo "Done. Next: open your agent and run pm-init (Claude Code: /pm-init)."
fi
