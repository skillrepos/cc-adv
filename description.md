# Advanced Claude Code: True AI Productivity — half-day workshop

Go beyond the basics — custom commands, hooks, CI automation, the Agent SDK, and your own MCP server.

**NOTE: This is a hands-on workshop — bring a personal laptop (corporate ones may not allow the labs to work).**

Claude Code has overtaken GitHub Copilot as the most-used AI coding tool in 2026, and McKinsey's February 2026 study (n=4,500 devs) shows AI coding tools cut routine-coding time by 46%, with senior devs reporting an 81% productivity boost. This half-day workshop picks up where the introductory Claude Code course leaves off and climbs the "extension ladder" one hands-on lab at a time.

You'll deepen project configuration (CLAUDE.md, memory hierarchy) and build production-grade custom slash commands with arguments, live git context, and scoped tool permissions — plus extended thinking for hard planning tasks. You'll enforce policy Claude *cannot* talk its way around with PreToolUse/PostToolUse hooks, proven to fire even in bypass-permissions mode. You'll turn Claude into a pipeline building block with headless mode (JSON output, per-file loops, pre-approved permissions) and integrate it into CI/CD with GitHub Actions via claude-code-action@v1. You'll drive the same agent loop from Python with the Claude Agent SDK (including memory beta) — building an unattended agent with a programmatic safety gate. The capstone: build your own MCP server (the protocol now has 97M monthly SDK downloads and 10,000+ servers) — a Python FastMCP "project-health" server with real tools, registered and shared at project scope, driven from natural-language prompts.

All five labs work one real codebase — a small Flask API whose test suite fails in exactly the ways your automation will find, triage, and report.

**Prerequisite:** Completion of the introductory Claude Code workshop or equivalent hands-on experience. Participants need an active paid Claude account and comfort with terminal-based workflows.

**Topics:** CLAUDE.md and the memory hierarchy; custom slash commands ($ARGUMENTS, frontmatter, inline bash context); extended thinking and thinking-effort control; hook-based automation and the constraint hierarchy; headless mode and structured output; CI/CD integration with GitHub Actions; the Claude Agent SDK (with memory beta) and permission engineering for unattended runs; and a capstone building a custom MCP server for a real-world use case.
