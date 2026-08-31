#!/usr/bin/env bash
# reset-lab3.sh - put this repo back to how it should look at the START of Lab 3.
#
# Undoes the /goal fix to app/ and clears Lab 3's leftovers, while KEEPING
# everything Labs 1 and 2 created: CLAUDE.md, .claude/commands, .claude/skills,
# .claude/agents, .claude/hooks, .claude/settings.json and config.json.
#
# Usage:
#   bash extra/reset-lab3.sh [--dry-run] [--force]
#     --dry-run   show what would happen, change nothing
#     --force     run even if a Claude session looks like it is still open
#
# Never take the user's shell down with us: if this file was sourced, say so
# and return instead of exiting.
if [ "${BASH_SOURCE[0]-$0}" != "$0" ]; then
  printf '%s\n' "Run this as a script, not with 'source':" \
                 "    bash extra/reset-lab3.sh" >&2
  return 1
fi

set -uo pipefail

DRY=0; FORCE=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --force)   FORCE=1 ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

say()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY" = 1 ]; then say "  [dry-run] $*"; else eval "$@"; fi; }

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { say "ERROR: not inside a git repo"; exit 1; }
cd "$ROOT" || exit 1
say "repo: $ROOT"
[ "$DRY" = 1 ] && say "(dry run - nothing will be changed)"

# ---------------------------------------------------------------- 1. no live agent
# A finished /goal leaves "treat the condition as your directive" in the session's
# context. Restore files while that session is open and it will put its fix back.
CLAUDE_RE='(^|[/[:space:]])claude([[:space:]]|$)|claude-code/cli\.js'
LIVE=$(pgrep -af "$CLAUDE_RE" 2>/dev/null | grep -v 'reset-lab3' | grep -v 'grep' || true)
if [ -n "$LIVE" ] && [ "$FORCE" = 0 ]; then
  say ""
  say "REFUSING: a Claude process still looks alive:"
  say "$LIVE" | sed 's/^/  /'
  say ""
  say "Exit it (/exit) first - a session that ran /goal will undo this reset."
  say "Then re-run, or pass --force if you know those processes are unrelated."
  exit 1
fi

# ---------------------------------------------------------------- 2. branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
  say "on branch '$BRANCH' -> switching to main"
  run "git switch main"
else
  say "on branch main"
fi

# ---------------------------------------------------------------- 3. undo the /goal fix
# origin/main is the authority when it exists, so this works even if the old
# lab flow committed the fix somewhere.
if git rev-parse --verify -q origin/main >/dev/null; then SRC=origin/main; else SRC=HEAD; fi
say "restoring app/ from $SRC"
run "git restore --source=$SRC --staged --worktree -- app/ 2>/dev/null || git restore --source=$SRC -- app/"

# ---------------------------------------------------------------- 4. Lab 3 leftovers
for f in beat.md health.md .claude/loop.md; do
  if [ -e "$f" ]; then say "removing $f"; run "rm -f '$f'"; else say "absent (ok): $f"; fi
done

# the throwaway branch from the retired flow
if git show-ref --verify -q refs/heads/loop-lab; then
  say "deleting leftover branch loop-lab"
  run "git branch -D loop-lab"
fi

# ---------------------------------------------------------------- 5. keep Lab 1 + 2 work
say ""
say "Labs 1-2 material (should all be present):"
for f in CLAUDE.md config.json .claude/settings.json .claude/hooks/protect-config.sh; do
  if [ -e "$f" ]; then say "  ok      $f"; else say "  MISSING $f"; fi
done
ls -d .claude/commands .claude/skills .claude/agents 2>/dev/null | sed 's/^/  ok      /'

# ---------------------------------------------------------------- 6. prove it
say ""
if [ "$DRY" = 1 ]; then
  say "dry run complete - nothing changed."
  exit 0
fi
say "verifying:"
OUT=$(python3 app/test_app.py 2>&1 | tail -1)
say "  python3 app/test_app.py -> $OUT"
case "$OUT" in
  *"10 passed, 4 failed"*)
    say ""
    say "READY: start Lab 3 at step 1 (claude --verbose)."
    ;;
  *passed*failed*)
    say ""
    say "UNEXPECTED counts: wanted '10 passed, 4 failed'."
    say "Check 'git status' - something outside app/ was changed, or a Claude"
    say "session re-applied its fix while this script ran."
    exit 1
    ;;
  *)
    say ""
    say "The suite did not run at all. This is an environment problem, not a"
    say "reset problem - the files are back the way Lab 3 wants them."
    say "In a Codespace: source .venv/bin/activate  (then re-run this script)."
    exit 1
    ;;
esac
git status --short | sed 's/^/  /'
