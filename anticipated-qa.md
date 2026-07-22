# Anticipated Q&A: Advanced Claude Code: True AI Productivity
**Generated**: 2026-07-07 (updated 2026-07-22)
**Course version**: 1.2 (labs.md Rev 1.2, deck v1.2)

Instructor prep for likely attendee questions, organized by section. Weighted toward the newer/denser material (hooks, SDK, MCP capstone).

---

## Section: Advanced Context, Commands & Extended Thinking (Lab 1)

**Q: What's the difference between CLAUDE.md, AGENTS.md, and # memories?**
A: CLAUDE.md is Claude Code's project context file, read at session start; AGENTS.md is the cross-tool open standard many agents (not just Claude) read; # memories are quick persistent facts saved to a memory file without editing CLAUDE.md. In practice: durable team knowledge goes in CLAUDE.md/AGENTS.md (committed), quick personal rules go in memories.

**Q: When should something be a custom command vs. a skill vs. a subagent?**
A: Command = a reusable prompt you invoke explicitly (`/triage`), runs inline. Skill = expertise Claude picks up automatically when context matches. Subagent = a specialist with its own context window and tool restrictions. Rule of thumb: you trigger commands, context triggers skills, delegation needs subagents.

**Q: Does the `` !`git status` `` in a command file run every time?**
A: Yes — at invocation time, before the prompt is sent. That's the point: the command self-loads *current* state. It only works for commands allowed by the command's `allowed-tools`.

**Q: Does extended thinking / ultrathink cost extra?**
A: More thinking = more generated tokens, so more usage and latency. The effort dial in `/model` is the main control; starting a prompt with `ultrathink` requests the maximum budget for that prompt. (Note: older "think"/"think hard" phrase triggers no longer do anything — only `ultrathink` is a trigger.) Guidance: hard planning tasks yes, routine edits no.

**Q: How do I make a subagent run on a cheaper model?**
A: Set `model:` in the agent's frontmatter (`.claude/agents/test-scout.md` uses `model: haiku` in Lab 1). Valid values: aliases (`haiku`, `sonnet`, `opus`, `fable`), a full model string, or `inherit` (default — use the main session's model). The same field works in command frontmatter; `--model` covers headless/CI; `ClaudeAgentOptions(model=...)` covers the SDK.

**Q: Doesn't the "subagents cost ~7x" warning contradict delegating to save money?**
A: Two different levers. The 7x figure is about context rebuilding — a subagent re-reads the repo, so *tokens* go up. Pinning `model: haiku` makes each of those tokens far cheaper ($1/$5 vs Sonnet's $3/$15 per M). Delegate for context isolation first; pin a cheap model so the isolation doesn't cost you.

**Q: Is the thinking Claude shows the "real" reasoning?**
A: It's the model's actual generated deliberation and is genuinely useful for verifying the approach, but treat it as a working trace, not a guarantee — you still verify the final output.

**Q: What's the difference between `$ARGUMENTS` and `$1`/`$2`?**
A: `$ARGUMENTS` is everything after the command name as one string; `$1`, `$2` split it positionally. Use positional when the command needs distinct parameters (e.g., `/compare fileA fileB`).

**Q: Why did /init pick up the failing tests?**
A: It scans the repo (docs, configs, code) to synthesize context. It found `app/test_app.py` and the run command the same way it finds build tools — that's why a good repo layout gives you a good CLAUDE.md for free.

---

## Section: Hooks (Lab 2)

**Q: If hooks fire even in bypass mode, what's the point of the permission system?**
A: Permissions are interactive, per-user consent; hooks are policy, enforced in code. Permissions protect *you* from surprises; hooks protect the *project* from anyone's session, including automation with permissions disabled.

**Q: Can Claude edit or delete the hook files to get around the policy?**
A: In this lab's setup, yes in principle — `.claude/settings.json` is just a file (and our guard only protects config.json). Real deployments protect hook files too (add them to the guard, use managed/enterprise settings, or enforce via CI). Good discussion point: policy is only as strong as what protects the policy.

**Q: Why exit code 2 specifically?**
A: The hooks contract: 0 = no objection, 2 = block (stderr fed back to Claude as the reason). Other nonzero codes are treated as hook errors, not vetoes.

**Q: What's the loophole the lab mentions?**
A: The matcher only guards `Edit|Write`, so Claude could modify the file via Bash (`sed`, `>>`). Production guards add a Bash matcher or permission-rule `if` conditions. The takeaway: enumerate the ways to do the thing you're blocking.

**Q: Can PostToolUse modify or roll back what happened?**
A: No — the tool already ran. PostToolUse is for auditing, logging, formatting, notifications. If you need to prevent, it must be PreToolUse.

**Q: Are hooks per-project or global?**
A: Both — `.claude/settings.json` (project, committable), `~/.claude/settings.json` (user), and enterprise-managed settings. Same hierarchy idea as memory. `/hooks` shows the source of each.

**Q: What other events exist besides PreToolUse/PostToolUse?**
A: SessionStart, Stop, UserPromptSubmit, and more; handler types beyond shell commands include prompt, agent, http, and mcp_tool. Point students at code.claude.com/docs/en/hooks.

---

## Section: Headless & CI (Lab 3)

**Q: How is `claude -p` billed / metered?**
A: On subscription plans, headless and Agent SDK usage draw from a separate monthly agent/SDK allowance distinct from interactive limits (rolled out mid-2026); with an API key it's normal API billing. Check your plan's usage page — this changes.

**Q: Why not just one big prompt: "summarize all my files"?**
A: It can work, but a loop gives you bounded, repeatable, independently-retryable calls — one failure doesn't poison the batch, and each call has a small, predictable context. That predictability is what automation needs.

**Q: My loop hung on one file. Why?**
A: Usually a permission wall — the run needed an unapproved action and had no human to ask. That's the Step-6 lesson: declare permissions up front (`--permission-mode acceptEdits` or `--allowedTools`).

**Q: Does the GitHub Action need a paid Claude account?**
A: It needs an `ANTHROPIC_API_KEY` secret (API billing), or OAuth token setup for subscription auth. The lab authors the workflow without running it, so no key is needed in class.

**Q: Is it safe to let Claude push commits from CI?**
A: Treat it like any contributor: scoped app permissions (Contents/Issues/PRs only), `--max-turns` plus `timeout-minutes` bounds, secrets only from the secrets store, and human review on PRs. The slide's security baseline is the checklist.

**Q: What's the difference between the two workflows we wrote?**
A: No `prompt:` = interactive mode (responds to @claude mentions); explicit `prompt:` = automation mode (runs on the trigger, e.g. cron). Same action, auto-detected mode.

**Q: Can CLAUDE.md and my custom commands be used in CI?**
A: Yes — the action respects repo CLAUDE.md, and `prompt:` can invoke skills/commands. Your Lab 1 assets work on the runner.

---

## Section: Agent SDK (Lab 4)

**Q: Do I need an API key for the SDK?**
A: No — it drives the bundled CLI, so your existing `claude` login carries over. (API key auth also works, e.g. for servers/CI.)

**Q: Why did the write silently fail in the read-only agent?**
A: The write wasn't blocked — it just wasn't pre-approved (`allowed_tools` had only Read/Glob/Grep), and unattended runs can't ask. Undecided = denied-by-default when nobody's there.

**Q: Why is `can_use_tool` not good enough as a gate?**
A: The CLI only consults it for calls that resolve to "ask." Anything already permitted by `allowed_tools`, `permission_mode`, or settings skips it. A PreToolUse hook sees every call — that's the property an unattended gate needs.

**Q: Is the Python `gatekeeper()` the same mechanism as Lab 2's shell hook?**
A: Same event (PreToolUse), same decision vocabulary (allow/deny + reason) — different packaging. Lab 2 registered a shell script in settings.json; Lab 4 passes a Python function in `ClaudeAgentOptions`. One mental model, two surfaces.

**Q: The deny test printed "Result: DONE" — did it fail?**
A: No — the task *told* Claude to say DONE, so the result string proves nothing. Evidence of the block is the `[gatekeeper] DENIED` line plus the file still existing. Teach "verify by artifact, not by the model's claim."

**Q: What is SDK memory (beta) and should we use it?**
A: Opt-in persistence of what an agent learns across runs — useful for recurring jobs so run 2 doesn't rediscover run 1's findings. It's beta: check the current Agent SDK docs before building on it, and note it doesn't bypass permissions or hooks.

**Q: Is there a TypeScript SDK?**
A: Yes — the Agent SDK ships for Python and TypeScript with equivalent concepts (query, options, hooks). We use Python to match the repo.

**Q: My run is slow / seems stuck.**
A: Each turn is a full model call plus tool execution; multi-turn tasks take tens of seconds. Watch the `[tool]` lines for progress; `max_turns` bounds the worst case.

---

## Section: Capstone MCP Server (Lab 5)

**Q: Why did running the server print nothing? Is it broken?**
A: Silence is success for a stdio server — it's waiting for a client to speak JSON-RPC on stdin. Claude Code starts/stops it and does the talking. If you see the skeleton message instead, the merge didn't save.

**Q: How does Claude know when to call my tool?**
A: From the tool's name, docstring, and input schema (generated from your function signature). That's why the lab stresses docstrings-as-interface — a vague docstring means wrong or missed tool calls.

**Q: MCP server vs. skill vs. command — when do I build which?**
A: MCP server = capability that needs *code execution or external systems* (databases, APIs, test runners), callable from any MCP client. Skill = knowledge/procedure for Claude itself. Command = a reusable prompt. The capstone's run_tests could only be a server or a script-backed skill; the server version is shareable across tools and teams.

**Q: How do I add parameters to a tool?**
A: Type-hinted function parameters: `def run_tests(pattern: str) -> str:` — FastMCP builds the input schema from the signature. Document each parameter in the docstring.

**Q: How would teammates get my server?**
A: Commit `.mcp.json` (project scope) — they approve it on first session. For wider distribution: plugin packaging, or host it as a remote HTTP server (`claude mcp add --transport http <url>`), which is how claude.ai connectors work.

**Q: What about secrets (API keys my server needs)?**
A: Never in `.mcp.json`. Use `--env` at add time, environment variables, or remote servers with OAuth. `.mcp.json` is committed and must stay secret-free.

**Q: `claude mcp list` shows "✗ Failed to connect."**
A: Run the server by hand (`python3 mcpserver/project_server.py`) and read the traceback — usually a missing `mcp` package (install requirements into the active venv) or a syntax slip from the merge. You're the maintainer now; the debugging loop is run-by-hand → fix → `claude mcp list`.

**Q: Can hooks govern my own server's tools?**
A: Yes — tools are named `mcp__project-health__run_tests`, so a PreToolUse matcher like `mcp__project-health__.*` works exactly like `Edit|Write` did in Lab 2.

---

## General / Cross-Cutting

**Q: Why do 4 tests in app/ fail? Should we fix them?**
A: They fail by design (500s where the contract wants 400/404) — they're the raw material for /triage, extended thinking, the SDK report, and the capstone's run_tests. Don't fix them during the workshop; fixing them is a great take-home exercise.

**Q: Everything today was Sonnet — when would I use Opus/other models?**
A: Sonnet is the workshop default for speed/cost. Bigger models (Opus, and Fable/Mythos at the frontier tier) earn their cost on the hardest planning/review steps; commands and agents can pin `model:` per task — mix deliberately.

**Q: I heard chat and Cowork Projects merged — what does that mean for us?**
A: Yes — Projects are now one unified interface across claude.ai chat and Cowork (one project object, both surfaces). For this course it's context, not lab material: the point of the basics slide is that project-level files/instructions/memory on those surfaces play the same role CLAUDE.md plays in a repo, and things you build here (MCP servers, skills) surface there too.

**Q: In what order should I adopt these techniques at work?**
A: Follow the course ladder: CLAUDE.md + commands (day one, zero risk) → hooks for real policies → headless loops for batch chores → CI once loops are trusted → SDK/MCP when you need custom integration. Each rung reuses the previous one's concepts.

**Q: A skeleton file says "still the skeleton" after I merged.**
A: The diff didn't fully land or the file wasn't saved. Re-open the `code -d` view, confirm nothing is highlighted, save the right-hand file (Cmd/Ctrl+S), close, re-run.

**Q: pip / flask / mcp module not found?**
A: Use `python3 -m pip install -r requirements.txt` from the repo root; in the Codespace, new terminals auto-activate the `.venv` (existing terminals from before a rebuild may not).

---

## Appendix: Timing & Break Plan

| Segment | Est. |
|---|---|
| Lab 1 | 10-12 min |
| Lab 2 | 10-12 min |
| Break (after Lab 2) | ~8 min |
| Lab 3 | 10-12 min (loop step is the long pole — ~30-60s per headless call) |
| Lab 4 | 10-12 min (SDK runs take 20-60s each; warn students to be patient) |
| Lab 5 | 10-12 min |

Buffer tips: Lab 3's per-file loop and Lab 4's unattended run are the two spots where slow runs stack up — have students read the next step while waiting. If running short on time, Lab 3 steps 10-11 and Lab 5 step 11 are read-only and can be assigned as homework.

<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
