#!/usr/bin/env python3
"""Lab 4 (Part 2): Unattended agent runs that never hang.

For an unattended run, policy has to be enforced on EVERY tool call. The right
tool for that is a PreToolUse hook: the CLI runs it before each tool executes,
no matter what, and the hook allows or denies the call by returning a
permissionDecision.

(ClaudeAgentOptions also has a can_use_tool callback, but the CLI only calls it
for tools that resolve to "ask" -- it is skipped for anything already permitted
by allowed_tools, permission_mode, or your settings. So can_use_tool is NOT a
reliable universal gate for an unattended agent. The PreToolUse hook is.)

[Lab 4 - Advanced Claude Code - Rev 1.0 - 07/07/26]
"""
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, HookMatcher, ResultMessage, query

TASK = (
    "Create a file named agent_report.md that lists every .py file in the app "
    "directory with a one-line description of each. Then say DONE."
)

# Lab step 9 uses this one to exercise the gatekeeper's deny path.
TASK_DENY = "Use a Bash rm command to delete agent_report.md. Then say DONE."

# Which task this run sends. Step 9: change TASK to TASK_DENY.
ACTIVE_TASK = TASK


async def gatekeeper(input_data, tool_use_id, context):
    """PreToolUse gate: deny destructive Bash, allow everything else. Never asks a human."""
    # --- 1 of 4: what is about to run ----------------------------------
    # MERGE BLOCK 1: pull out what the CLI is asking to run -- the tool's
    # name, and (for Bash) the command string itself.

    # --- 2 of 4: the one refusal --------------------------------------
    # MERGE BLOCK 2: the policy. A Bash command carrying "rm " or "sudo" is
    # refused: say so on the console, and answer "deny".

    # --- 3 of 4: the default answer -----------------------------------
    # MERGE BLOCK 3: everything else is fine -- note it and answer "allow".
    # Note what is NOT here: no "ask". Nobody is watching to answer one.
    raise NotImplementedError("gatekeeper: merge blocks 1-3 from the left, then save")


async def prompt_stream():
    yield {"type": "user", "message": {"role": "user", "content": ACTIVE_TASK}}


async def main() -> None:
    # --- 4 of 4: the run itself ---------------------------------------
    # MERGE BLOCK 4: the settings -- the tools this job needs, a turn cap,
    # and gatekeeper() wired in as a PreToolUse hook on every tool -- then
    # run the task and print the final stats.
    raise SystemExit("auto_agent.py is still the skeleton -- merge all four blocks from the left, SAVE, then run again.")


asyncio.run(main())
