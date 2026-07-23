#!/bin/bash
# format-check.sh — PostToolUse hook
# Fires after Write/Edit/MultiEdit. Checks the edited file for AI slop.
# Exit 0 = allow, Exit 1 = warn (non-blocking), Exit 2 = block (we use warn)

# Read JSON payload from stdin (Claude Code hook spec)
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | grep -oP '"file_path"\s*:\s*"\K[^"]+' | head -1)

# Exit cleanly if no file path (nothing to check)
[ -z "$FILE_PATH" ] && exit 0

# Only check text-ish files
case "$FILE_PATH" in
  *.md|*.html|*.txt|*.json|*.py) ;;
  *) exit 0 ;;
esac

# Banned slop words/phrases
SLOP_EN="unlock|unleash|elevate|leverage|game-changer|cutting-edge|dive into|deep dive|empower|transform|revolutionize|supercharge|seamless|robust|streamlined|holistic"
SLOP_ES="libera tu potencial|transforma tu carrera|desbloquea|potencia tu|en la era digital|en el mundo de hoy"

FOUND=0
if grep -iE "$SLOP_EN" "$FILE_PATH" > /dev/null 2>&1; then
  echo "⚠️  Slop detected in $FILE_PATH:" >&2
  grep -inE "$SLOP_EN" "$FILE_PATH" >&2
  FOUND=1
fi

if grep -iE "$SLOP_ES" "$FILE_PATH" > /dev/null 2>&1; then
  echo "⚠️  Slop ES detected in $FILE_PATH:" >&2
  grep -inE "$SLOP_ES" "$FILE_PATH" >&2
  FOUND=1
fi

if [ $FOUND -eq 1 ]; then
  echo "See .claude/rules/anti-slop.md for replacements." >&2
  exit 1  # Warn, don't block (exit 2 would block)
fi

exit 0
