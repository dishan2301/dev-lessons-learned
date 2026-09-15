#!/usr/bin/env bash
# Installs this repo's Claude Code skill and Codex global instructions.
# Safe to re-run any time — e.g. after moving the repo or on a new machine.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${LESSONS_LEARNED_HOME:-$HOME/dev-lessons-learned}"

echo "Repo location:          $REPO_DIR"
echo "LESSONS_LEARNED_HOME:   $TARGET"

if [ "$REPO_DIR" != "$TARGET" ]; then
  echo
  echo "Note: this repo is not at \$LESSONS_LEARNED_HOME ($TARGET)."
  echo "Either move/clone it there, or make this location permanent:"
  echo "  echo 'export LESSONS_LEARNED_HOME=\"$REPO_DIR\"' >> ~/.bashrc   # or ~/.zshrc"
  echo "  source ~/.bashrc"
fi

echo
mkdir -p "$HOME/.claude/skills"
rm -rf "$HOME/.claude/skills/lessons-learned"
cp -r "$REPO_DIR/claude-code/lessons-learned" "$HOME/.claude/skills/lessons-learned"
echo "Installed Claude Code skill -> $HOME/.claude/skills/lessons-learned"

echo
mkdir -p "$HOME/.codex"
if [ -f "$HOME/.codex/AGENTS.md" ] && ! grep -q "Lessons Learned — Cross-Project" "$HOME/.codex/AGENTS.md"; then
  echo "$HOME/.codex/AGENTS.md already exists with other content — not overwriting."
  echo "Append this section manually:"
  echo "  cat \"$REPO_DIR/codex/AGENTS.md\" >> \"$HOME/.codex/AGENTS.md\""
elif [ -f "$HOME/.codex/AGENTS.md" ]; then
  echo "$HOME/.codex/AGENTS.md already has this section — leaving it as-is."
else
  cp "$REPO_DIR/codex/AGENTS.md" "$HOME/.codex/AGENTS.md"
  echo "Installed Codex global instructions -> $HOME/.codex/AGENTS.md"
fi

echo
echo "Done."
