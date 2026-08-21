# Changelog — cc-adv (Advanced Claude Code workshop)

## labs 1.10 — 08/21/26 — Carry over the ccode Codespace + auto-mode fixes

Propagated from the `ccode` QA run of 08/20/26. **Deck unchanged at v1.7** — the deck was checked
and needed nothing (see "Checked and NOT changed" below).

### Codespace: the VS Code diff view never opened

`ccode` shipped with a bug that silently disabled Claude Code's side-by-side diff view in the
Codespace, and cc-adv had the identical devcontainer shape. The VS Code extension publishes its
port by stamping `CLAUDE_CODE_SSE_PORT` into terminals at *creation* time; the terminal a Codespace
opens for you can be created before the extension activates, so it never receives the variable.
Without it the CLI cannot match its IDE lock file — no diff, and no **Diff tool** entry in `/config`.

- **New `extra/claude-ide-port.sh`** — defines a `claude` shell function that resolves the port from
  the newest *live* `~/.claude/ide/*.lock` when the variable is unset. It resolves at *launch* time,
  not shell-start time, because the lock file does not exist yet when the startup terminal's
  `.bashrc` runs.
- **New `.devcontainer/setup.sh`** — copies that script to `~/.claude-ide-port.sh` and appends a
  **guarded** source line to `.bashrc`: `if [ -f ~/.claude-ide-port.sh ]; then . ~/.claude-ide-port.sh; fi`.
  The guard is not optional: an unguarded source line makes *every shell* error when the file is
  missing.
- **`devcontainer.json`** — both hooks now call `bash .devcontainer/setup.sh`. The venv/pip build
  work stays in `postCreateCommand`. Side benefit: Codespaces echoes the hook verbatim into the
  startup terminal, so students now see one short line instead of a wall of text.

Verified: `setup.sh` runs silently, is idempotent (one guard line after two runs), and
`. ~/.bashrc` then yields `claude is a function`.

### STARTUP.md

- Step 1 now says to open a **new** terminal, with a one-line reason. The port race is
  nondeterministic — the startup terminal sometimes does get the variable — so the wrapper above is
  the real fix and this is the fallback.
- Documents the new first-run prompt **"Try the new fullscreen renderer?"** → choose **2. Not now**,
  since "Yes" produces a UI matching none of the course screenshots.

### labs.md — auto-mode drift (Revision 1.10)

Two steps told students to answer a permission prompt that **auto mode never raises**. Both were
observed live during the ccode run: `/init` wrote `CLAUDE.md` with no prompt, and a skill loaded
with `Successfully loaded skill` and no approval.

- **Lab 1 `/init`** — the "Do you want to create CLAUDE.md?" prompt is now marked as manual-mode only.
- **Lab 1 `/triage`** — the "Use skill 'triage'?" approval is now marked as manual-mode only.

A whole-file sweep for `option 1|option 3|choose option|approve it|select option` confirms no other
unconditional prompt claims remain.

### Checked and NOT changed (verified negatives, recorded so the next pass can skip them)

- **Deck cycle order.** ccode deck slide 30 had `Plan → back to Manual`, which is wrong. cc-adv's
  deck does **not** carry that error — slide 10 lists the modes correctly.
- **`ctrl+t` / todo tools, "subagents nest 5 levels", `/terminal-setup`** — none appear in cc-adv labs.
- **`ctrl+g` plan-open, `/permissions` deny rules, `/rewind`, "Recently denied"** — none appear in
  cc-adv labs, so those ccode fixes have no counterpart here.
- **`/agents`** — the two hits are `.claude/agents` paths, not the removed `/agents` command.
- **Slide 40 "research preview"** — refers to `claude ultrareview`, not auto mode. Out of scope.

### Prose trim (same revision)

Prose cut **8035 -> 5262 words (-35%)**, code blocks and image lines excluded:

| Lab | Before | After | Reading time |
|---|---|---|---|
| 1 | 2070 | 1193 | 10.4 -> 6.0 min |
| 2 | 1477 | 961 | 7.4 -> 4.8 min |
| 3 | 1150 | 763 | 5.8 -> 3.8 min |
| 4 | 1976 | 1362 | 9.9 -> 6.8 min |
| 5 | 1362 | 983 | 6.8 -> 4.9 min |

Cut: "What we're doing / Why" preambles, editorializing, and prose restating code the student just
merged. Kept: every instruction, every gotcha and troubleshooting note, all flags/env vars/API
names, the `(recap)` markers, and both auto/manual sentences above.

Verified mechanically against the pre-trim backup (`labs.md.bak-1.10-pretrim`): **68 fenced code
blocks byte-identical**, 40 image refs identical and in order, 84 headings identical, 56 step
headings identical, `code -d` count unchanged at 4. The one pre-existing retrospective phrase
("they used to be triggers") is gone; the fact it carried is kept.

**Still above the 400-600 target** — every lab lands between 763 and 1362. The floor is structural:
headings, separators and `**Action:**` lines alone are 150-320 words per lab, and what remains is
mostly reference-dense material (`setting_sources` semantics, `can_use_tool` vs PreToolUse,
`--permission-mode dontAsk`, prompt-cache invalidation, skill-folder options). Going lower means
deleting facts rather than compressing prose. Roughly another 600-800 words are available across
the five labs by dropping the enrichment blockquotes outright — a content decision, deliberately
left to the author.

## labs 1.9 / deck v1.7 — 08/20/26 — Gap-fill slides, paid for by trimming four

Deck **workshop-claude-code-adv_v1.7.pptx** — 63 slides total, **55 visible (unchanged)**, 8 hidden. labs.md → **Revision 1.9**. Four gap-fill slides added and four existing slides **hidden, not deleted**, so the course still fits 3 hours.

### Four new slides

| # | Slide | Sits after | Why |
|---|---|---|---|
| 28 | **The Sandbox — Enforcement, Not Judgement** | Hook Rules of Thumb | The deck cited "sandbox" twice as the strongest defence tier and never explained it. Lands the hook-vs-sandbox distinction: a hook is a *decision*, the sandbox is a *boundary* the OS enforces on every child process — which closes the Lab 2 loophole class (blocking Edit doesn't stop `sed` via Bash). |
| 35 | **What a Loop Actually Pays For — the Prompt Cache** | The Loop Pattern | Model and effort are part of the cache key without being part of the prompt. In a per-file loop that's a rebuild per iteration. Placed in the automation section where cost-per-iteration becomes real. |
| 56 | **Agent Teams — Peers, Not Subagents** | Lab 5 intro | The *intro* deck defers agent teams to "an advanced course"; this is that course and it didn't cover them. Honest about the caveats: experimental, off by default, CLI-only, unavailable under `-p`, ~7x tokens. |
| 57 | **Dynamic Workflows — Script Holds the Loop** | Agent Teams | The closing rung of "own every arrow in the loop": Claude writes a JavaScript orchestration script and the runtime runs it, so control flow is deterministic and agents are workers inside it. Three distinct answers to "more than one agent" now sit together: subagents → teams → workflows. |

Each carries a full `[NEW SLIDE - 2026-08-20]` speaker note with sources and the nuances likely to come up as questions.

### Four slides hidden (reversible — each has a [TRIMMED] note saying why and when to unhide)

- **13 AGENTS.md — The Universal Standard.** The intro deck already carries this slide and this audience is required to have taken the intro.
- **44 Same Loop, Three Wrappers.** The two slides before it already make the same-loop point twice.
- **50 MCP: Connecting Claude Code to External Tools.** Consumer recap the intro covers; its `claude mcp add` block duplicates the "Adding Servers — Scope Decides" slide two along, and Lab 5 opens with its own MCP recap.
- **58 Public Ecosystems.** Browse-y closer with counts that date fast; its slot now carries Agent Teams and Dynamic Workflows.

**Net: visible slide count unchanged at 55, so the lecture budget is flat.** Roughly 11–12 minutes of new material offset by roughly 10 minutes of trims.

### labs.md Rev 1.9 — Lab 1 restructured, still 11 steps

Lab 1 had **four** `*(recap)*` steps in a course that requires the intro workshop. Merged the old step 4 (`/memory` hierarchy — a pure "open this menu" step) into step 3, which freed a slot for:

- **NEW step 6: "Turn the Command Into a Skill — Without Restarting."** Students `mv .claude/commands/triage.md .claude/skills/triage/SKILL.md` and re-run `/triage` **with no restart**. The payoff lands because they felt the opposite two steps earlier: a new *command* file forced an exit-and-restart, and so did the new agent. Skills hot-reload; commands and agents don't.
- **Watcher caveat handled:** Claude Code only watches skill directories that existed at session start, so step 4 now runs `mkdir -p .claude/commands .claude/skills` — the restart in step 5 establishes the watch before step 6 needs it. A fallback line tells students to restart once if `/triage` isn't found.
- Step 3 retitled "Persist a Rule, a Memory — and See the Hierarchy"; step 9 "Session-Level Thinking Effort" → "Session-Level Effort" (the dial is *effort*, not "thinking effort"); Lab 1 summary updated.

**Step counts: 11 / 12 / 11 / 10 / 12 — every lab still inside the 10–12 target, and Lab 1 did not grow.** Labs 2–5 are untouched; the other three additions are deliberately slide-only because agent teams is experimental and CLI-only, `ultracode` has unpredictable wall-clock, and `/sandbox` on Linux needs packages a Codespace may not carry — all three would make flaky labs.

## labs 1.8 / deck v1.6 — 08/20/26 — August currency pass (aligned with ccode Rev 6.21)

Deck saved as NEW file **workshop-claude-code-adv_v1.6.pptx** (59 slides, was 58). labs.md → **Revision 1.8**. Every fact below verified against code.claude.com / platform.claude.com on 2026-08-20 (changelog head v2.1.236; npm latest 2.1.237). Unlike `ccode`, the v1.5 deck was a genuine file — the August auto-mode pass did land here.

### ⚠️ Regression found: the June-15 metering claim was never fully removed

The 07/10/26 entry below records "June 15 metering CANCELLED — corrected on deck s27 and s29". It was **still present on three slides** in v1.5: slide 32 (The Loop Pattern), slide 34 (CI Automation), and slide 44 (SDK vs -p). The July fix caught two instances and missed the third, and slide numbering had shifted since. Now removed from all three and confirmed absent by a whole-deck regex sweep. `code.claude.com/docs/en/costs` describes a single per-seat allowance shared across Claude chat, Cowork and Claude Code — there is no separate automation pool.

**Lesson:** when retiring a claim, grep the whole deck for it rather than fixing the slides you happen to remember.

### Deck v1.6

- **NEW slide 18 — "Custom Commands Are Skills Now."** The biggest content gap. Custom commands have merged into skills: `.claude/commands/triage.md` and `.claude/skills/triage/SKILL.md` both create `/triage`, existing files keep working, and the skill form adds a supporting-files directory, invocation control (`disable-model-invocation`), and execution control (`context: fork`, `background`, `allowed-tools`). Lab 1 builds a command and the deck never said any of this. Speaker notes carry precedence rules and the sharpest contrast: **skills hot-reload, while `.claude/commands/` files and agents need a restart** — which is exactly why Lab 1 makes students restart twice.
- **Slide 20 — ultrathink semantics corrected.** It was titled "More Budget on Demand" and claimed ultrathink is a "max-budget trigger". It is not: Claude Code recognizes the keyword and adds an in-context instruction for that turn, and **the effort level sent to the API is unchanged**. Retitled "Two Dials, Not One". Notes also record that "think" / "think hard" / "think more" are no longer keywords.
- **Slide 7 (Models & Cost)** — Sonnet $3/$15 → **Sonnet 5 $2/$10**; added Fable 5 $10/$50 and named Opus 5. Added the point that context stopped being the tier differentiator (Sonnet 5 / Opus 5 / Fable 5 all carry 1M at standard rates; Haiku 4.5 is 200k). Notes carry the cutoff inversion: **Opus 5 is May 2026 against Jan 2026 for Sonnet 5 and Fable 5.**
- **Slide 56 (hidden, Token & Cost)** — every price was stale. Now Sonnet 5 $2/$10, Opus 5 $5/$25, Haiku 4.5 $1/$5, Fable 5 $10/$50 (replacing the Agent-Teams row; the ~7x figure survives on the Subagent Cost Awareness slide).
- **Slide 45 — "Memory (beta)" reframed to "Memory Across Runs."** There is no separate beta memory capability: the SDK loads the same auto-memory the CLI uses. Added the trap that matters for Lab 4 — the agent saves memories with the ordinary `Write`/`Edit` tools, so an unattended agent whose `allowed_tools` omits `Write` silently cannot save anything.
- **Slide 37 (ultrareview)** — verified still current and extended: `--json`, `--timeout <minutes>` (30-min default), and `--post` to comment findings on a GitHub PR (v2.1.227+, `--no-post` is the default).
- **Slide 5** — setup URL `docs.claude.com/en/docs/claude-code/setup` → `code.claude.com/docs/en/setup`.
- **Slide 53** — added the "as of mid-2026" qualifier to the ecosystem counts, matching `ccode`.
- Every touched slide carries an `[Update - 2026-08-20]` speaker note. Visual QA passed; `validate.py --original` passes.

### labs.md Rev 1.8

- **Intro** — dropped the brittle "Sonnet is option 4, option 2 is Opus" positional claim (the picker now also carries Opus 5 and Fable 5 and shows a price per row); "thinking effort" → **effort level**; added the price ladder plus the 1M-context and knowledge-cutoff points.
- **Lab 1 step 8** — ultrathink corrected as above, with the dead "think"/"think hard" phrases called out.
- **Lab 1 step 9** — named the levels (low/med/high/xhigh/max, `high` default), added `/effort` and `/effort ultracode`, and **the prompt-cache warning: the cache is keyed by model AND effort, so changing effort mid-session invalidates it** (Claude Code now asks you to confirm).
- **Lab 1 step 10** — added `/usage` alongside `/context`, including its new **attribution breakdown** (usage by skill, subagent, plugin, and individual MCP server) with a forward pointer to Lab 5.
- **Lab 3 step 6** — added `--permission-mode dontAsk` and `--bare` for reproducible CI runs.
- **Lab 4 step 6** — added what the SDK *does* read from disk. **Omitting `setting_sources` is equivalent to `["user","project","local"]`**, so the SDK loads CLAUDE.md, skills, agents and settings exactly like the CLI. Two consequences: **the hook students wrote in Lab 2 is still armed and fires inside their Lab 4 agent**, alongside the Python gatekeeper; and `setting_sources=[]` is the isolation switch (with the multi-tenant caveat that managed policy, `~/.claude.json` and auto-memory are read regardless).
- **Lab 4 step 10** — replaced the stale "memory (beta)" note and fixed a dead `docs.claude.com/en/api/agent-sdk/overview` link.
- Step counts unchanged: 11 / 12 / 11 / 10 / 12. No new steps, no added lab time.

### Code and config verified, no changes needed

Installed the current libraries in a clean environment and checked every API the labs use. `claude-agent-sdk` **0.1.73**: `query`, `ClaudeAgentOptions(allowed_tools, max_turns, hooks, permission_mode, setting_sources, model, agents, can_use_tool, fallback_model)`, `HookMatcher(matcher, hooks, timeout)`, `ResultMessage.num_turns/.duration_ms/.result`, plus `tool`, `create_sdk_mcp_server` and `ClaudeSDKClient` all present. `mcp` **1.27.0**: `from mcp.server.fastmcp import FastMCP` imports, with `.tool()` and `.run()`. `sdk/agent_loop.py`, `sdk/auto_agent.py`, `mcpserver/project_server.py` and all three `extra/*.txt` completed files are structurally current. `requirements.txt`, `extra/settings.local.json` and the devcontainer need no changes.

### Deliberately not added

Sandboxing (`/sandbox` is real and the deck name-drops it twice as the "enforcement" layer without explaining it), a prompt-cache slide angled at CI/SDK, and agent teams / dynamic workflows (`ultracode`) as first-class topics. All are advanced-appropriate and recorded in HANDOFF.md as candidates; none earned slide time in a 3-hour course this pass.

## labs 1.1 / deck v1.2 — 07/10/26 — Product-currency fixes ported from intro course

Deck saved as NEW file **workshop-claude-code-adv_v1.2.pptx** (v1.1 superseded — delete after review). labs.md → Revision 1.1.

- **June 15 metering CANCELLED** — corrected on deck s27 (headless/CI) and s29 (Agent SDK credit); the separate metering never took effect
- Model indicator note loosened for the Sonnet 5 era + /model persistence note (labs intro)
- `--model claude-sonnet-4-6` → `--model sonnet` in the GitHub Actions workflow (Lab 3) and its claude_args table
- Lab 2 step 10 (`! cat` audit log): added the suggested-path-line tip — while the subtle suggestion line is showing, Enter is silently ignored (Esc clears it)

Most intro-course fixes (# memory, /agents wizard, manual-mode rename, rewind, skill triggering, reviewer format) don't apply here — this course has no labs covering those flows and was authored post-rename. If a modes/memory recap slide is ever added, pull wording from ccode deck v6.18+.
