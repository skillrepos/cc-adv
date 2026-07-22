# Advanced Claude Code: True AI Productivity
## Half-Day Workshop Outline (3 hours, 5 labs)
### Revision 1.2 - 07/22/26

**Positioning:** Successor to the introductory *AI-Powered Coding with Claude Code* workshop (ccode). Less extensive than the 1.5-day extended edition (cc-se). Picks up where the intro leaves off: participants already know the CLI, modes, context commands, skills, subagents, and plugin packaging.

**Prerequisite:** Completion of the introductory Claude Code workshop or equivalent hands-on experience. Active paid Claude account. Comfort with terminal-based workflows.

**Format:** Instructor-led, hands-on. GitHub Codespace (zero-install) or local VS Code + devcontainer. Each lab is 10-12 steps and 10-12 minutes.

---

## Schedule at a Glance

| Time | Segment | Type |
|------|---------|------|
| 0:00 - 0:12 | Welcome, why this matters, setup check, intro-course recap | Lecture |
| 0:12 - 0:32 | **Section 1:** Project configuration power-ups — CLAUDE.md deep-dive, custom slash commands (arguments, frontmatter, inline bash), extended thinking | Lecture |
| 0:32 - 0:44 | **Lab 1:** Advanced Context, Custom Commands & Extended Thinking | Lab |
| 0:44 - 1:02 | **Section 2:** Hooks — policy at the tool boundary; lifecycle, anatomy, real-world hooks | Lecture |
| 1:02 - 1:14 | **Lab 2:** Hooks — Enforcing Policy at the Tool Boundary | Lab |
| 1:14 - 1:22 | Break | — |
| 1:22 - 1:42 | **Section 3:** Headless mode as a pipeline building block; CI/CD with `claude-code-action@v1` | Lecture |
| 1:42 - 1:54 | **Lab 3:** Headless Mode & CI Automation | Lab |
| 1:54 - 2:12 | **Section 4:** The Claude Agent SDK — same loop, your program; unattended permissions engineering; memory (beta) | Lecture |
| 2:12 - 2:24 | **Lab 4:** Agent SDK — Programmatic and Unattended Loops | Lab |
| 2:24 - 2:40 | **Section 5:** From MCP consumer to MCP producer — building your own server with FastMCP | Lecture |
| 2:40 - 2:52 | **Lab 5 (Capstone):** Build a Custom MCP Server | Lab |
| 2:52 - 3:00 | Wrap-up: ecosystem, where to go next, Q&A | Lecture |

---

## Section Detail

### Welcome & Recap (12 min)
- Why this matters: AI coding tools cut routine-coding time ~46% (McKinsey, Feb 2026); Claude Code now the most-used AI coding tool
- Claude basics level-set (3 slides): models & cost (Haiku/Sonnet/Opus/Fable, token pricing), surfaces & Projects (chat + Cowork Projects now unified in one interface), and the agent loop
- Where the intro course left off: modes (manual/plan/accept-edits/bypass), context commands, CLAUDE.md basics, skills, subagents, commands, plugins (one recap slide)
- Environment check: Codespace up, `claude` authenticated, model set to Sonnet

### Section 1 — Project Configuration Power-Ups (20 min + Lab 1)
- CLAUDE.md / AGENTS.md / auto memory — quick remedial, then what production teams actually put in them
- Global vs. local configuration files
- Custom slash commands beyond the basics: `$ARGUMENTS` and positional `$1/$2`, frontmatter (`description`, `argument-hint`, `allowed-tools`, `model`), inline bash context with `` !`cmd` ``, `@file` references, namespacing
- Right-sizing models: `model:` frontmatter for subagents and commands (haiku/sonnet/opus/fable, full strings, inherit), `--model` for headless/CI, `ClaudeAgentOptions(model=...)` — cheap scouts, smart supervisor
- Extended thinking: `ultrathink` max-budget trigger, thinking effort via `/model`, watching thinking with `ctrl+o`
- **Lab 1:** `/init` on a real Flask codebase → memory hierarchy → build a `/triage` command with arguments + live git context → run it → delegate test runs to a `model: haiku` test-scout subagent → extended thinking on a refactor plan → `/context` cost check

### Section 2 — Hooks (18 min + Lab 2)
- The constraint hierarchy: prompt constraints → tool constraints (`disallowedTools`) → hooks
- Hook lifecycle: PreToolUse, PostToolUse, SessionStart, Stop, and friends
- Anatomy of `settings.json` hooks: matchers, exec form vs. shell form, exit codes (0 / 2), stderr as feedback to Claude
- Hooks people actually ship: guard files, audit logs, auto-format, context injection
- **Lab 2:** PreToolUse guard that blocks edits to `config.json` + PostToolUse bash audit log — proven to fire even in bypass-permissions mode

### Section 3 — Headless Mode & CI Automation (20 min + Lab 3)
- `claude -p` as a Unix tool: stdin/stdout contract, `--output-format json` / `stream-json`, jq extraction
- The loop pattern: one bounded call per item beats one giant prompt
- Pre-approving permissions for unattended writes: `--permission-mode`, `--allowedTools`
- CI: `anthropics/claude-code-action@v1` — @claude responder mode vs. automation mode with `prompt:`, `claude_args` passthrough, security baseline
- **Lab 3:** pipe → JSON → jq → per-file loop → acceptEdits write → author both workflow files → have headless Claude review your own workflow

### Section 4 — Claude Agent SDK (18 min + Lab 4)
- The SDK in plain English: `claude -p` as a Python library; `query()`, `ClaudeAgentOptions`
- CLI-to-SDK mapping: `allowed_tools` = `--allowedTools`, `max_turns` = `--max-turns`, message stream = `stream-json`
- Unattended means permissions, engineered: why `can_use_tool` is not a universal gate and a PreToolUse hook is
- Memory (beta): persistent agent memory across SDK runs — what it is, when to reach for it
- **Lab 4:** diff-merge a read-only `query()` loop → run it → watch the blocked write → diff-merge the gatekeeper agent → run unattended → trigger the deny path

### Section 5 — Capstone: Build a Custom MCP Server (16 min + Lab 5)
- MCP recap in one slide: servers, tools, scopes, `mcp__<server>__<tool>` naming
- From consumer to producer: what a server is (a process speaking JSON-RPC over stdio), what FastMCP hides
- Tool design: docstrings are the model's documentation; return strings the model can reason over
- **Lab 5 (Capstone):** diff-merge a `project-health` FastMCP server (run_tests / count_todos / project_stats) → register at project scope → inspect with `/mcp` → drive it from natural-language prompts → tie back to hooks matchers and team distribution via `.mcp.json`

### Wrap-Up (8 min)
- The extension ladder you just climbed: commands → hooks → headless/CI → SDK → MCP server
- Public ecosystems, plugin marketplaces, where to go next
- Q&A

---

## Lab Inventory

| Lab | Title | Style | Key assets |
|-----|-------|-------|-----------|
| 1 | Advanced Context, Custom Commands & Extended Thinking | build | `app/` Flask to-do API, `.claude/commands/triage.md` + `.claude/agents/test-scout.md` (model: haiku) created in lab |
| 2 | Hooks: Enforcing Policy at the Tool Boundary | build | `.claude/hooks/protect-config.sh`, `.claude/settings.json` (created in lab) |
| 3 | Headless Mode & CI Automation | guided | `.github/workflows/claude.yml`, `daily-report.yml` (created in lab) |
| 4 | Agent SDK: Programmatic and Unattended Loops | skeleton + diff-merge | `sdk/agent_loop.py`, `sdk/auto_agent.py` ↔ `extra/*.txt` |
| 5 | Capstone: Build a Custom MCP Server | skeleton + diff-merge | `mcpserver/project_server.py` ↔ `extra/project_server.txt` |

## Repo Layout

```
cc-adv/
├── .devcontainer/devcontainer.json   # Codespace/devcontainer setup
├── app/                              # Flask to-do API (analysis target; 4 tests fail by design)
├── sdk/                              # Agent SDK skeletons (Lab 4)
├── mcpserver/                        # MCP server skeleton (Lab 5)
├── extra/                            # Completed versions for diff-merge labs + env config
├── images/                           # Lab screenshots
├── labs.md                           # The lab document
├── outline.md                        # This outline
├── README.md                         # Setup instructions
├── STARTUP.md                        # Claude Code start/auth walkthrough
└── requirements.txt                  # flask, claude-agent-sdk, mcp
```

## Description Alignment Notes

The published description mentions "orchestrating multi-file refactors" and "strategies for managing complex agentic coding sessions" — these are covered inside Sections 1 and 4 (extended thinking on a refactor plan; turn caps, permission engineering, and gatekeeper patterns) rather than as standalone labs. "97M monthly SDK downloads / 10,000+ servers" and the McKinsey stats appear on the "Why This Matters" slide. Everything else in the description maps 1:1 to a section above.

<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
