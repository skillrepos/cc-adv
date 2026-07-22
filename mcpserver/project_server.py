#!/usr/bin/env python3
"""Lab 5 (Capstone): Your own MCP server -- "project-health".

An MCP server is just a process that speaks the Model Context Protocol over
stdin/stdout. FastMCP (from the official Python MCP SDK) hides the protocol:
you write plain Python functions, decorate them with @mcp.tool(), and the
docstring + type hints become the tool's documentation and input schema --
exactly what Claude reads when it decides which tool to call.

This server gives Claude Code three "project health" tools for THIS repo:
  run_tests()     -- run the app/ test suite and report what passed/failed
  count_todos()   -- count TODO/FIXME comments across the project's code
  project_stats() -- file and line counts by language

[Lab 5 - Advanced Claude Code - Rev 1.0 - 07/07/26]
"""
import pathlib
import subprocess
import sys

from mcp.server.fastmcp import FastMCP

# The repo root, resolved relative to this file -- so the tools work no matter
# which directory the server process is started from.
ROOT = pathlib.Path(__file__).resolve().parent.parent

mcp = FastMCP("project-health")

# ----------------------------------------------------------------------
# SKELETON BODY -- replace everything between these dashed lines by
# merging the three @mcp.tool() functions from extra/project_server.txt
# (see the lab's diff-merge step), then SAVE this file.
# Until you merge, running this file just prints the message below.
# ----------------------------------------------------------------------
raise SystemExit("project_server.py is still the skeleton -- merge the finished file (left side of the diff) into this body, SAVE, then run again.")

if __name__ == "__main__":
    # stdio is the default transport: Claude Code starts this process and
    # talks to it over stdin/stdout -- the same kind of server you added
    # with `claude mcp add` as a consumer. Now you're the producer.
    mcp.run()
