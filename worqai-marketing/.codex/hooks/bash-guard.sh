#!/bin/bash
# bash-guard.sh — PreToolUse hook on Bash tool
# Blocks dangerous commands before they execute
# Exit 2 = block with reason in stderr

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | grep -oP '"command"\s*:\s*"\K[^"]+' | head -1)

[ -z "$COMMAND" ] && exit 0

# Block destructive patterns
if echo "$COMMAND" | grep -qE 'rm -rf /|rm -rf \.|rm -rf \*|:(){ :|:& };:|dd if=|mkfs\.'; then
  echo "🚫 Blocked dangerous command: $COMMAND" >&2
  exit 2
fi

# Block secret exfiltration attempts
if echo "$COMMAND" | grep -qE 'cat.*\.env|echo.*API_KEY|echo.*SECRET|curl.*\|.*bash|wget.*\|.*sh'; then
  echo "🚫 Blocked potential secret exposure: $COMMAND" >&2
  exit 2
fi

exit 0
