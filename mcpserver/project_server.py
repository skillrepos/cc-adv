#!/usr/bin/env python3
"""Lab 5 (Capstone): Your own MCP server -- "project-health".

An MCP server is just a process that speaks the Model Context Protocol over
stdin/stdout. MCPServer (from the official Python MCP SDK) hides the protocol:
you write plain Python functions, decorate them with @mcp.tool(), and the
docstring + type hints become the tool's documentation and input schema --
exactly what Claude reads when it decides which tool to call.

This server gives Claude Code three "project health" tools for THIS repo:
  run_tests()     -- run the app/ test suite and report what passed/failed
  count_todos()   -- count TODO/FIXME comments across the project's code
  project_stats() -- file and line counts by language

[Lab 5 - Advanced Claude Code - Rev 1.1 - 08/25/26]
"""
import pathlib
import subprocess
import sys

from mcp.server import MCPServer

# The repo root, resolved relative to this file -- so the tools work no matter
# which directory the server process is started from.
ROOT = pathlib.Path(__file__).resolve().parent.parent

mcp = MCPServer("project-health")


# --- Tool 1 of 3: run_tests -- is the app meeting its contract? -------
# MERGE BLOCK 1: runs app/test_app.py and hands back the pass/fail output.
# The docstring is not decoration -- it is what Claude reads to decide
# whether to call this tool.


# --- Tool 2 of 3: count_todos -- how much unfinished work is here? ----
# MERGE BLOCK 2: counts TODO/FIXME across the repo's source files.


# --- Tool 3 of 3: project_stats -- how big is this codebase? ----------
# MERGE BLOCK 3: file and line counts per file type.
raise SystemExit("project_server.py is still the skeleton -- merge all three tools from the left, SAVE, then run again.")

if __name__ == "__main__":
    # stdio is the default transport: Claude Code starts this process and
    # talks to it over stdin/stdout -- the same kind of server you added
    # with `claude mcp add` as a consumer. Now you're the producer.
    mcp.run()
