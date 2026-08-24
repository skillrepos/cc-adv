# Changelog — cc-adv (Advanced Claude Code workshop)

## labs 1.15 — 08/24/26 — Reconciled after a pull replaced the working tree with the remote lineage

A `git pull` on 08/24 brought down remote commits `38d808f`/`650150b` (Brent's GitHub edits of
08/23 15:24-15:57 EDT, made against the pre-loops lineage and self-stamped "Rev 1.12 - 08/22") plus
`087e08f` (six new `ccadv10-15.png` Lab 1 screenshots). That overwrote the local, never-committed
Rev 1.12/1.13/1.14 labs.md and the full CHANGELOG. **Rev 1.15 = the complete 1.14 content restored,
with every remote hand edit folded in:**

- Preamble: "Today's ladder" pricing paragraph removed; the intro NOTE trimmed to end at
  "kept quick" (auto-mode explainer dropped).
- "Estimated time" sentence removed from Lab 1 and Lab 2 purposes (remote did exactly these two;
  Labs 3-5 still carry it — flag if uniformity wanted).
- Lab 1: manual-mode branches removed from steps 1/3/7; the rule-may-already-exist note added;
  `/exit` phrasing; "This file demonstrates…", "separate/other terminal tab" phrasings;
  "the folder also buys you" aside and the general-purpose-fallback warning paragraph removed;
  the `/usage` proof pointer dropped; **subagent step split** into create (6) + restart-and-run (7)
  — Lab 1 is now **12 steps**; new screenshots wired in: `ccadv12` (init), `ccadv14` (rule),
  `ccadv15` (triage command).
- Lab 2: "We are working to implement this policy…" wording; the "No connection_timeout" line
  removed from step 8.
- **Screenshot collision resolved:** the uploaded `ccadv10-15.png` are Lab 1 captures, but the
  loops Lab 3 (Rev 1.12) had reserved those numbers for its pending shots — Lab 3's six
  references renumbered to **`ccadv19-24.png`** (still to capture, with `ccadv16-18` from 1.13).
  `ccadv10/11/13.png` are on disk but currently unreferenced (their anchor steps don't exist in
  the 1.13 structure).
- Everything from 1.12/1.13/1.14 below is back in: loops Lab 3, delegation-ladder Lab 1 (+
  worktrees callout, decision rule), CI-as-reading, Lab 4 auth aside.

**Lesson: the 08/23 evening work and 1.14 were never committed to git — a pull could and did
erase them. Commit labs/CHANGELOG revisions promptly after each revision lands.**

Step counts now **12/12/11/10/12** (57 total).

## labs 1.14 — 08/24/26 — External AI review triaged: worktrees in, CI authoring demoted to reading

Brent had a second AI review labs.md against the beginner course. Each recommendation was
verified before acting (docs research + a line-by-line beginner/advanced cross-check).

**Rejected (with evidence):**

- *"Remove the command→skill migration — it re-teaches beginner Labs 4-5."* Refuted: the beginner
  course's frontmatter ceiling is a bare `description:`; `$ARGUMENTS`, `` !`bash` `` injection,
  `@file` in a command file, `allowed-tools` scoping, hot-reload, and `context: fork` appear
  nowhere in it. The `mv` step is also the vehicle for teaching fork (per the 1.13 audit decision,
  after `/subtask` failed live verification), and `/triage` is referenced by Labs 3 and 5.
- *Lab 2 changes.* The hook taxonomy and the five handler types it proposed adding are already in
  step 11; the logger→formatter swap was optional per the reviewer and would orphan verified
  screenshots.
- *"Revalidate SDK auth."* Validated: the docs warning is scoped to third-party distribution of
  claude.ai login, not local dev — and the 08-21 live QA ran Lab 4 on subscription auth in the
  classroom Codespace.

**Accepted and applied:**

- **Lab 1 step 9: worktrees callout** (the review's best catch — a real gap). Doc-confirmed on
  code.claude.com: `claude -w/--worktree <name>` → `.claude/worktrees/<name>/` on branch
  `worktree-<name>`; subagent frontmatter `isolation: worktree`; auto-cleanup when unchanged.
  Kept as a taught aside, NOT a hands-on step — unverified in the Codespace. ⚠ Docs also claim
  `--bg` auto-isolates edits into a worktree, which would conflict with step 9's
  `cat bg_report.md` at repo root (our 08-23 sandbox run found the file at root) — check
  `worktree.bgIsolation` behavior on the next Codespace QA run.
- **Lab 1 summary: the delegation decision rule** — subagent / fork / background / worktree /
  cheaper model, one line each.
- **Lab 3: CI authoring demoted to reading.** Old steps 10-11 (typing two workflow YAMLs that
  can never execute — the repo isn't the students') merged into one reading-only step 10 carrying
  both YAMLs and the `claude_args` table; "Know the Bounds" renumbered 12→11. Lab 3 is now 11
  steps, all hands-on minutes on `/goal` + `/loop`. Images `cc-se76/77.png` are now orphans.
- **Lab 4 step 1: auth aside** — dev loop (CLI login carries over, as this lab runs) vs
  distribution (`ANTHROPIC_API_KEY` / Bedrock / Vertex / Foundry; claude.ai login may not be
  offered in shipped products), tied back to Lab 3's CI secret.

Step counts now **11/12/11/10/12** (56 total). Deck v1.10 unchanged — its CI slides already carry
the demoted content.

## labs 1.13 / deck v1.10 — 08/23/26 — The advanced-course audit: delegation ladder

Brent's challenge: with all the *(recap)* steps, is this truly an advanced course that builds on
ccode? Full audit run: ccode labs re-read step by step (its 56 steps already cover commands,
skills, subagents, plugins, /rewind, /context and basic headless pipe), every cc-adv lab and all
67 slides cataloged, and the Aug-2026 capability surface researched against code.claude.com and
verified against a live 2.1.241 install.

**Verdict:** Labs 2-5 (hooks, loops, SDK, MCP server) hold up as advanced. The problem was Lab 1 —
4 of its 11 steps were recaps, and its topics (commands/skills/subagents) are ccode's Labs 4-5
with better frontmatter. Meanwhile the actual advanced delegation surface — forks, background
agents, agent teams, dynamic workflows — was two flyby slides after the last lab, and background
agents appeared nowhere.

### Verified live before writing (Claude Code 2.1.241)

- **`claude --bg`** works: prints `backgrounded · <id>` plus the four management commands
  (`claude agents` / `attach` / `logs` / `stop`); the detached session created its file ~45s later.
- **`context: fork` in SKILL.md frontmatter** works: the skill loaded and ran forked (headless
  sandbox test — flagged for Codespace QA).
- `--json-schema`, `--max-budget-usd`, `--bare`, `--teleport`, `--cloud`, `claude agents`,
  agent-teams env gate, `/subtask`, workflows — all confirmed present in the CLI.
- **`/subtask` did NOT resolve in a session with custom agent types configured** — kept OUT of the
  lab; fork is taught through the skill frontmatter instead.

### labs.md Revision 1.13 — Lab 1 rebuilt as "Advanced Delegation — Right Model, Right Context, Right Worker"

11 steps, all ≤12 min:

1. **Set Up in One Pass** *(recap — the only full recap left)*: `/init` + the standing test rule.
   The old steps 1-3 (scout, /init walkthrough, rule + auto-memory + /memory hierarchy) collapsed
   into it; auto-memory now a one-line pointer back to ccode.
2-4. Command → run → skill hot-reload (unchanged — the frontmatter content is advanced and QA'd).
5. **NEW — Fork the Skill**: add `context: fork`, rerun `/triage`, watch the run leave the main
   context; fork vs background framed as the execution dials.
6. Haiku subagent (unchanged).
7. **Two Dials of Thinking** — old steps 8 (ultrathink) + 9 (/effort) merged.
8. **NEW — Send a Worker to the Background**: `claude --bg` with `--permission-mode acceptEdits`,
   tied back to Lab 3's unattended-permissions rule.
9. **NEW — Manage the Fleet**: `claude agents`, `logs`, `stop`, `cat bg_report.md`; closes with the
   ladder up to teams/workflows (deliberately not hands-on — token cost on class accounts).
10. `/context` cost *(recap kept per Brent)* — now also shows what the step-5 fork kept out.
11. Exit.

Recap steps: 4 → 2 tagged (one is the 30-second setup, one the /context closer).
New screenshots needed: `ccadv16-18.png` (fork run, --bg output, agent view).

### Deck v1.10 — the delegation section rebuilt, 69 slides / 58 visible

- **NEW "The Delegation Ladder"** (pos 19) — the section's framing slide: inline → subagent →
  fork → --bg → team/workflow, with the trade named at each rung (isolation buys focus, paid in
  tokens).
- **NEW "Background Agents — a Fleet, Not Tabs"** (pos 23) — the panel is the real `--bg` output
  captured live.
- **Agent Teams and Dynamic Workflows moved up** from the closing flyby (old pos 60-61) into the
  delegation section (pos 24-25), each with a scripted INSTRUCTOR DEMO speaker note (run on your
  own account — ~7x tokens for teams, fleet-scale for workflows — not on class accounts).
- **"Commands vs Agents" hidden** (`[TRIMMED]`) — its rule of thumb now lives on the ladder slide.
- **Slide 10 panel corrected** — it still said "Lab 1 commands, context, thinking / Lab 3
  headless + CI"; drift from two revisions of lab changes. Now "the delegation ladder" / "loops + CI".
- **Lab 1 title slide** retitled + purpose rewritten.
- **JSON Out slide**: added `--json-schema` / `--max-budget-usd` / `--bare` bullet.
- **"Claude Code on the Web" rewritten as "Beyond the Terminal"** (closing): cloud sessions,
  `--teleport`, Remote Control (GA), Channels (research preview) — placeholder narrowed so text no
  longer runs under the screenshot.

Net: +2 slides, +1 hidden → visible 57 → 58. Validated against v1.9; ladder, background-agents,
slide-10, Lab-1-title and Beyond-the-Terminal pages rendered and checked.

### Deliberately NOT given lab time (decision log)

- **Agent teams / dynamic workflows** — instructor demo + slides (token cost, experimental gate).
- **Channels, Monitor tool** — slides only (research preview, credential + Bun setup).
- **Cloud sessions / Remote Control** — closing slide (needs org enablement; runs outside the
  Codespace).
- **/subtask** — didn't survive live verification in a configured session; fork taught via
  frontmatter instead.
- **Sandbox** — stays a slide (bubblewrap availability in the Codespace unverified).
- **Output styles, LSP/IDE, OpenTelemetry, plugin eval / skill-doctor** — neither (not advanced,
  not class-runnable, or early-access gated).


## labs 1.12 / deck v1.9 — 08/23/26 — Loops become a first-class topic

`/loop` and `/goal` appeared **nowhere** in the deck or the labs — grepped and confirmed zero
hits for `/loop`, `/goal`, "Stop hook", `CronCreate` and "scheduled task" in v1.8 / Rev 1.11.
Meanwhile the whole thesis of slide 31 was "remove yourself from the loop," and every driver it
named lived outside Claude Code. Fixed on both sides. Supersedes `workshop-claude-code-adv_v1.8.pptx`.

### Verified live before writing anything (Claude Code 2.1.241)

Not taken from docs. Both features were exercised against a copy of this repo's `app/`:

- **`/goal`** — `claude -p "/goal python3 app/test_app.py reports 14 passed, 0 failed…"` fixed the
  four 400/404 contract violations in `app.py`, never touched `test_app.py`, and cleared itself when
  the evaluator confirmed 14/14. **8 turns, ~25s, $0.33.** Repeated a second time with the same result.
- **`/loop 1m`** — driven through a real interactive session on a pty. Fires `CronCreate(*/1 * * * *)`,
  prints `Scheduled 8db547d2 (Every minute)`, and the target file collected 4 timestamped lines a
  minute apart. Jitter was visible: first fire at :31, then settling to :19.
- **Workspace trust gates `/goal`** — the evaluator is part of the hooks system, so an untrusted
  folder prompts first. Codespaces seed trust, but it is a real failure mode on a laptop demo.
- `/goal` and `/loop` are both registered commands in 2.1.241, and `CronCreate` / `CronList` /
  `CronDelete` / `ScheduleWakeup` all appear in the session tool list.

### labs.md Revision 1.12 — Lab 3 rewritten end to end

**Was:** "Headless Mode & CI Automation", 11 steps — six of them `claude -p` mechanics (pipe, JSON,
jq, a for-loop, inspect its output, pre-approve permissions) and five GitHub Actions.
**Now:** "Loops Instead of Prompts — `/goal` and `/loop`", 12 steps:

1. `git switch -c loop-lab` — a throwaway branch, because `/goal` edits real files
2. `/goal` against the failing suite — Lab 1's ultrathink plan, actually executed
3. Reading the evaluator's verdicts (not yet met / met / impossible), Ctrl+O for the reason
4. `/goal` with no arguments — status: turns evaluated, spend, last reason
5. Confirm 14/14 and `git diff --stat`, commit, `git switch -` — **restores the 4 failures for Lab 5**
6. `/loop 2m …` — `CronCreate`, the job ID, the cadence confirmation
7. `.claude/loop.md` — replacing the built-in maintenance prompt (written while the loop ticks)
8. `CronList` / `CronDelete` in plain English, and Esc
9. `claude -p "/goal …" --output-format json | jq` — the same loop with no session at all
10-11. The two GitHub Actions workflows (unchanged, reframed as the outer loop off your machine)
12. Bounding a loop: stop clauses, `--max-turns`, `timeout-minutes`, CI security baseline

The `-p` mechanics that left the lab were **already on deck slides 36-37** (pipe, jq, the JSON
envelope, stream-json, exit codes), so nothing was lost — they are now demonstrated rather than typed.

**Step 5 is load-bearing.** If a student skips the commit-and-switch-back, `app/` stays fixed and
Lab 5's project-health MCP demo reports a clean suite instead of the failures it is meant to summarize.

**Prose:** 707 → 1224 words, which puts Lab 3 in line with Lab 1 (1279), Lab 2 (1039) and Lab 4 (1398)
rather than being the outlier it was. Still above the 400-600 target, like every other lab.

**Six screenshots need capture** on the next QA run: `ccadv10`-`ccadv15.png` (goal set, verdicts,
status, loop scheduled, loop cancelled, headless goal). Seven images are newly orphaned:
`cc-se29/31/32/36/37/38/78.png`.

### Deck v1.9 — the loop arc rebuilt, in-session first

**Slide 31 "From Prompts to Loops" rewritten.** It listed four drivers, all external (bash loop, SDK,
CI runner, cron). It now reads as a ladder: inner loop (`/goal`) → outer loop (`/loop`) → off the
session (`-p`, SDK) → off your machine (CI). The through-line is unchanged.

**Four new slides, 32-35:**

- **`/goal` — The Inner Loop.** The condition, the Haiku evaluator, three verdicts, and the fact that
  decides everything: the evaluator has no tools, so the condition must name something whose output
  lands in the transcript.
- **`/loop` — The Outer Loop.** Three forms (interval+prompt, prompt-only self-paced, bare + `loop.md`),
  `CronCreate`/`CronList`/`CronDelete`, session scope, jitter, 7-day expiry, and where it stops reaching.
  The code panel is the real terminal output captured above.
- **Three Ways to Keep a Session Going.** `/goal` vs `/loop` vs a Stop hook, split by *what starts the
  next turn*. Lands the payoff for an advanced room: `/goal` is documented as a wrapper around a
  session-scoped prompt-based Stop hook — the Lab 2 mechanism with a friendly front end. Also keeps
  auto mode in its lane: it approves calls *within* a turn and never starts a new one.
- **Anatomy of a Reliable Loop.** Spec · checklist · inspector · budget, mapped onto what `/goal`
  actually implements.

**Retitled:** slide 38 was "The Loop Pattern (This Is the Whole Idea)" — no longer true once `/goal`
and `/loop` are taught four slides earlier. Now "The Loop Pattern — One Headless Call, Multiplied".
Slide 45 (the Lab 3 title slide) retitled and its purpose line rewritten.

**Hidden to pay for the four new slides** (hide, don't delete — `[TRIMMED]` notes on both):

- **43 "The Workflow, Annotated"** — duplicates what students type by hand in Lab 3 steps 10-11, and
  slide 42 already carries the CI flow visually.
- **44 "Deep Cloud Review — claude ultrareview"** — useful but has no lab, sits outside the loop story
  this section now tells, and is the most date-sensitive slide in the deck.

**Slide count 63 → 67, visible 55 → 57.** Net +2 rather than the usual zero: Lab 3 gave back roughly
six minutes of hands-on `-p` mechanics, which is what the two extra slides spend. Flagged rather than
buried — if the timing runs long, slides 42 and 38 are the next candidates to hide.

Speaker notes added to every new and changed slide. Validated with `validate.py --original v1.8`;
all four new slides rendered to PNG and checked for overflow.


## deck v1.8 — 08/23/26 — Define "tool" and "classifier" on the slides

Both terms were used throughout the deck without ever being defined. Labs unchanged
(still Revision 1.11); this is a deck-only revision. `workshop-claude-code-adv_v1.7.pptx`
is superseded. 63 slides / 55 visible, unchanged.

### Slide 9 (Claude Basics — The Agent Loop) — new bullet

The deck leaned on "tool" everywhere — hooks fire at the tool boundary, `allowed_tools`
scopes the SDK, MCP adds new ones — but the only thing resembling a definition was
"An agent = model + tools in a loop". Added, directly under that bullet:

> • A tool = one named capability the model requests and the harness runs — Read, Write,
> Edit, Bash, Glob, Grep, WebFetch, Task

This is the concept Lab 2's loophole depends on: blocking the Edit *tool* leaves the Bash
*tool* untouched, which only lands if students hold "tool = one discrete named capability".
Speaker note added spelling out model-requests / harness-runs and the tie to Lab 2.

### Slide 11 (What Changed on August 14, 2026) — classifier bullet rewritten

"A classifier model reviews each risky call instead of you" assumed the term. Now:

> • A classifier — a second, fast model — reads each risky call and answers allow/block;
> 3 blocks in a row (or 20 in a session) and prompts return

The real explanation (second model, probabilistic, 89% vs 13.6%) was already in the speaker
notes but never reached a slide, which mattered because the slide immediately contrasts the
classifier with hooks. Speaker note added defining it as a risk verdict rather than a rule.

### Slide 11 code panel — formatting fix (pre-existing defect)

The `# the classifier is a MODEL.` line in the dark panel carried **no run properties** —
no size, no color, no Consolas — so it rendered small, dark and proportional against its
matched pair `# a hook is YOUR CODE.`. Confirmed present in v1.7 by inspecting the slide XML,
and visible in a LibreOffice render. Given the same rPr as the hook line (1600, italic,
`888888`, Consolas).

Verified: `validate.py --original v1.7` passes; slides 9 and 11 rendered to PNG and checked
for overflow — neither box runs past the code panel.


## labs 1.11 — 08/21/26 — First full live run of all 5 labs; Lab 5 unblocked

The first end-to-end execution of every lab in a real Codespace (Claude Code **2.1.238**, Node
v22.23.2, `claude-agent-sdk` **0.2.143**, Claude Max / Sonnet 5 / medium). All 56 steps run,
all 40 screenshots recaptured. **Deck stays at v1.7** — the deck was grepped slide by slide for
every claim touched below and needed nothing; see "Checked and NOT changed".
Full evidence in `qa-report-live-run-2026-08-21.md`.

### requirements.txt — Lab 5 was completely broken

`mcp>=1.2` had started resolving to **mcp 2.0.0**, which renamed FastMCP to `MCPServer` and
**deleted `mcp.server.fastmcp`** with no compatibility shim. Both `mcpserver/project_server.py`
and the answer key `extra/project_server.txt` import it, so every step of Lab 5 died on
`ModuleNotFoundError` — students never even reached step 2's "still the skeleton" message.

- **`mcp>=1.2,<2`** — pins to the 1.x line (last release 1.29.0). Chosen over migrating the code to
  `MCPServer` so that Lab 5's prose and the deck's FastMCP naming stay correct. The migration is a
  two-token change in each file if we ever want it; it would cost a rewrite of Lab 5 steps 1 and 3
  plus the deck's MCP slides.
- **`pydantic-settings<2.13`** — 2.13+ emits an `IncompleteFieldDefinitionWarning` about mcp's
  `lifespan` field. Four lines of noise printed before the server starts, which wrecks Lab 5 step 4
  where a *silent* start is the success signal. Verified: on 2.12.0 the server starts silently again.

Both pins verified with `pip install --dry-run -r requirements.txt` (exit 0, no conflicts) and by
re-running Lab 5 end to end.

### STARTUP.md — step 4 was putting every student on Opus

The `/model` picker reordered. It now reads `1. Default (Opus 5) · 2. Opus (1M context) ·
3. Fable · 4. Sonnet · 5. Haiku`, and STARTUP.md still said *type "2"*. Rewritten to select
**Sonnet by name**, with an explicit warning that position 2 is an Opus entry — matching the
guidance labs.md's preamble already carried.

### labs.md (Revision 1.11) — 20 corrections from the live run

**Wrong, now fixed:**

- **Lab 1 step 7** — the pre-restart session does *not* refuse with "There's no test-scout agent type
  available". It says that **and then silently falls back to `general-purpose`**, runs the suite, and
  returns a correct-looking 10/4 table from the wrong agent on the wrong model with the full test
  output in the main context. That is the opposite of the step's lesson, so the step now says so.
- **Lab 2 step 10** — "Your own `!` commands appear too — they go through the Bash tool" is false.
  Verified twice: the log holds only Claude's own tool calls. Reversed.
- **Lab 2 step 10** — the "*Enter* is silently ignored while the suggested-path line shows" warning no
  longer reproduces on 2.1.238. Softened to describe the hint and say Enter still submits.
- **Lab 1 preamble** — "Each row also shows that model's price per million tokens" is no longer true;
  the picker shows no prices. Replaced with a pointer to the ladder, plus a note that Sonnet now sits
  at position 4.

**UI drift, re-described against 2.1.238:**

- **Lab 1 step 3** — `/memory` now shows `Auto-memory: on` as a status line above
  **1. Project instructions** / **2. User instructions** / **3. Open auto-memory folder**.
- **Lab 1 step 10** — `/context` has no "project files" category. Categories are now System prompt,
  System tools, Custom agents, Memory files, Skills, Messages.
- **Lab 2 step 6** — `/hooks` opens on a **read-only list of events**, not the two-hook summary.
  `[command]` and `Project Settings` are two levels down; both drill-in steps now say what to expect.
- **Lab 5 step 8** — the tool detail view has no input-schema section; it shows Full name and the
  docstring as Description. Rewritten around what's actually on screen.
- **Lab 5 step 10** — tool calls collapse to `Called project-health 2 times`; the `mcp__…` names only
  appear after *Ctrl+o*. Step now says to press it.

**Missing steps / undocumented prompts:**

- **Lab 2 step 5** — `claude-yolo` opens a red "Bypass Permissions mode" warning requiring
  **2. Yes, I accept**. Was undocumented; now called out.
- **Lab 5 step 4** — `Ctrl+C` on the stdio server prints a long `KeyboardInterrupt` traceback.
  Now flagged as expected rather than a failure.

**Auto-mode drift missed by Rev 1.10** — three more places assumed a prompt that auto mode removes:
Lab 1 step 3 ("Approve the edit"), Lab 1 step 7 ("Approve as needed… asks before running"), and
Lab 5 step 9 ("Approve the tool use"). All now name both modes.

**Accuracy nits:**

- **Lab 4 step 4** — new callout: `allowed_tools` is **not** an exhaustive whitelist. A `[tool] Bash`
  line appears for `ls` even though Bash isn't listed, because read-only commands never need approval.
- **Lab 4 step 5** — the run uses `Grep` several times, not "`Glob`, then `Grep`".
- **Lab 4 step 9** — the deny line is whatever command Claude picks (`rm -f …` in our run), and Claude
  usually *explains* it couldn't delete rather than blandly printing DONE.
- **Preamble** — auto mode is now "normally", with a note that a first session after a fresh install
  (i.e. a new Codespace) can start in Manual whatever the plan.

Prose grew ~420 words (5.6k → 6.1k) — all of it correctness, none of it new teaching.

### images/ — all 40 recaptured

Every screenshot `labs.md` references was recaptured from this run on 2.1.238 and replaced in place;
filenames are unchanged. The old set predated the `/model`, `/memory`, `/hooks`, `/context` and
MCP-panel redesigns and the much larger `--output-format json` payload.

### Checked and NOT changed

- **Lab 3** — all 11 steps passed with zero defects.
- **`claude-agent-sdk` 0.2.143** — despite the jump from 0.1.73, `query`, `ClaudeAgentOptions`,
  `AssistantMessage`, `ResultMessage`, `TextBlock`, `ToolUseBlock`, `HookMatcher` and the
  `hooks={"PreToolUse": [HookMatcher(...)]}` shape all still work. No code changes.
- **`model: haiku` really pins the subagent** — `claude-haiku-4-5` appears only in the subagent
  transcript, and `/usage` bills it separately.
- **Lab 4 step 6's claim that the Lab 2 shell hook fires inside the SDK agent** — verified with a
  probe: the Python gatekeeper allowed the Write and `protect-config.sh` still blocked it.
- **`-p` / SDK "start in `default`"** — correct terminology; the docs still call the mode `default`
  and label it Manual.
- **`--max-turns`** — dropped from `claude --help` but still parses, so Lab 3 step 9 stands.
- Diff-merge hunk counts (1 / 2 / 1), the 10-passed/4-failed suite, 40 image references with 0
  missing, and the Rev 1.10 devcontainer IDE-diff fix all verified working.
- **The deck (v1.7), checked slide by slide against every fix above.** Slide 7's prices are labelled
  *API* price per M tokens, so the picker dropping them changes nothing; "above Haiku every model has
  a 1M context window" is confirmed (Sonnet 5 reports 967k). Slide 20's `model: haiku` block, slides
  23/25's hook events and `/hooks → inspect`, and slides 43/45/46's `allowed_tools` framing
  ("pre-approve routine tools" — never claimed to be exhaustive) are all still accurate.
- **Slides 54-55 keep their FastMCP naming — and that is the reason the pin was chosen over migrating
  the code.** `from mcp.server.fastmcp import FastMCP` on slide 54 is correct only while
  `mcp<2` holds. If we ever take the `MCPServer` migration, slides 54 and 55 and Lab 5 steps 1 and 3
  must move with it.


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
