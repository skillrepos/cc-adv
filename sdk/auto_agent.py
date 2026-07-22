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


async def gatekeeper(input_data, tool_use_id, context):
    """PreToolUse gate: deny destructive Bash, allow everything else. Never asks a human."""
    # GATEKEEPER (TODO 1) -- merge this body from extra/auto_agent.txt:
    #   read tool_name and tool_input["command"]; if it's a Bash command
    #   containing "rm " or "sudo", print a DENIED note and return a
    #   permissionDecision of "deny"; otherwise print an "allowing" note and
    #   return a permissionDecision of "allow".
    raise NotImplementedError("gatekeeper: merge extra/auto_agent.txt, then save")


async def prompt_stream():
    yield {"type": "user", "message": {"role": "user", "content": TASK}}


async def main() -> None:
    # ------------------------------------------------------------------
    # SKELETON BODY (TODO 2) -- merge this whole body from
    # extra/auto_agent.txt, then SAVE. It builds ClaudeAgentOptions with
    # allowed_tools, max_turns, and the PreToolUse gatekeeper hook, then
    # reads the ResultMessage.
    # ------------------------------------------------------------------
    raise SystemExit("auto_agent.py is still the skeleton -- merge BOTH highlighted regions from the left (the finished file) into the right, SAVE, then run again.")


asyncio.run(main())
