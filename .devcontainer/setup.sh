#!/usr/bin/env bash
# Workshop environment setup. Invoked from postCreateCommand and postAttachCommand.
#
# This lives in a script rather than inline in devcontainer.json because Codespaces
# echoes the hook command verbatim into the startup terminal -- a long inline command
# means a wall of text is the first thing a student sees.
#
# Safe to run repeatedly: every step is guarded.

set -u

# Workshop Claude Code settings, only if the student has none yet.
cp -n extra/.claude.json ~/ 2>/dev/null || true

# Convenience alias used where the labs allow skipping permission checks.
if ! grep -qs claude-yolo ~/.bash_aliases 2>/dev/null; then
    echo 'alias claude-yolo="claude --dangerously-skip-permissions"' >> ~/.bash_aliases
fi

# VS Code diff-view support. See extra/claude-ide-port.sh for why this is needed.
# The source line is guarded so a missing script degrades to a no-op instead of
# printing an error in every single shell.
if [ -f extra/claude-ide-port.sh ]; then
    cp -f extra/claude-ide-port.sh ~/.claude-ide-port.sh
fi
if ! grep -qs claude-ide-port ~/.bashrc 2>/dev/null; then
    echo 'if [ -f ~/.claude-ide-port.sh ]; then . ~/.claude-ide-port.sh; fi' >> ~/.bashrc
fi

exit 0
