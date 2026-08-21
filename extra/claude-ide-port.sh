# Claude Code IDE integration recovery for Codespaces / devcontainers.
#
# The Claude Code VS Code extension publishes its port by stamping
# CLAUDE_CODE_SSE_PORT into terminals, but VS Code applies environment
# collections only at terminal *creation* time. The terminal a Codespace
# opens for you is created before the extension finishes activating, so it
# never receives the variable and VS Code cannot retrofit it.
#
# Without the variable the CLI falls back to matching its IDE lock file by
# PID ancestry. The lock file's pid is the extension host, and a terminal is
# a child of the pty host -- a sibling, never an ancestor -- so the match can
# never succeed. Result: no diff view, and no "Diff tool" entry in /config.
#
# This wrapper resolves the port when you launch Claude (by which time the
# extension has activated) rather than when the shell starts (when the lock
# file may not exist yet). It picks the newest lock file whose port is
# actually accepting connections, so stale locks from closed windows are
# skipped.

claude() {
    if [ -z "$CLAUDE_CODE_SSE_PORT" ]; then
        local lock port
        for lock in $(ls -t "$HOME/.claude/ide"/*.lock 2>/dev/null); do
            port="$(basename "$lock" .lock)"
            if (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
                exec 3>&-
                export CLAUDE_CODE_SSE_PORT="$port"
                break
            fi
        done
    fi
    command claude "$@"
}
