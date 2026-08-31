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
    # --- 1 of 2: the run's guardrails ---------------------------------
    # MERGE BLOCK 1: the settings this run works under -- which tools are
    # pre-approved, and the cap on how many turns the loop may take.

    # --- 2 of 2: the message loop -------------------------------------
    # MERGE BLOCK 2: read what query() streams back -- Claude's text, each
    # tool call it makes, and the final stats.
    raise SystemExit("agent_loop.py is still the skeleton -- merge BOTH blocks from the left, SAVE, then run again.")


if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]) or (
        "What files are in this directory? Answer in one sentence."
    )
    asyncio.run(run_agent(user_prompt))
