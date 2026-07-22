#!/usr/bin/env python3
"""Lab 4: Your first programmatic agent loop.

This is the SAME agent loop that powers the Claude Code CLI --
we are just driving it from Python instead of a terminal.

[Lab 4 - Advanced Claude Code - Rev 1.0 - 07/07/26]
"""
import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)


async def run_agent(prompt: str) -> None:
    """Send one prompt through the agent loop and print what happens."""
    # ------------------------------------------------------------------
    # SKELETON BODY -- replace everything between these dashed lines by
    # merging from extra/agent_loop.txt (see the lab's diff-merge step),
    # then SAVE this file. Two pieces turn this script into an agent:
    #   1. the OPTIONS -- which tools are pre-approved, plus a turn cap
    #   2. the LOOP    -- read each message query() streams back: Claude's
    #                     text replies and the tool calls it makes
    # ------------------------------------------------------------------
    raise SystemExit("agent_loop.py is still the skeleton -- merge the finished file (left side of the diff) into this body, SAVE, then run again.")


if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]) or (
        "What files are in this directory? Answer in one sentence."
    )
    asyncio.run(run_agent(user_prompt))
