# Advanced Claude Code: True AI Productivity
## Go beyond the basics — advanced delegation, hooks, loops, CI automation, the Agent SDK, and your own MCP server
## Session Labs
## Revision 1.21 - 08/24/26

<br><br>

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**Copy and paste may not work as expected if using the mouse. If not, use the keyboard shortcuts - *Ctrl+C/Cmd+C and Ctrl+V/Cmd+V*.**

**If you haven't done so already, set your model to `Sonnet` instead of `Opus`.**

> In Claude Code at the prompt, type:
> ```
> /model
> ```
> In the list that comes up, use the up/down arrow keys to move the pointer to *Sonnet* and hit *Enter*. **Select by name, not by number** — the menu order shifts as models are added (the list carries Opus 5 and, on some accounts, Fable 5 — on a Max account today *Sonnet* sits at position **4**, behind two Opus entries). The picker no longer prints per-model prices; the ladder below has them. Also use the **left/right** arrow keys to set the **effort level** to *medium* (it defaults to *high*).
>
> ![set model](./images/ccode209.png?raw=true "set model")
>
> You should see an indicator that the model was set to a *Sonnet* model (currently *Sonnet 5* / `claude-sonnet-5` — the exact version shown may be newer) with *medium* effort. Note: your `/model` selection is saved as the default for new sessions; press `s` in the model list to set it for the current session only.
>
<br><br>

**These labs assume `⏵⏵ auto mode on` — STARTUP.md Step 5.**

> Check the bottom-left of the prompt; if it reads `⏸ manual mode on` — which is where a brand-new Codespace starts — press **Shift+Tab** until it reads *auto mode on*. Lab 2 deliberately switches to bypass mode; every other lab assumes auto.

<br><br>

**NOTE:** This course assumes you are already comfortable with the Claude Code basics — running it, permission modes, `/init` and CLAUDE.md, skills, subagents and custom commands. A few steps re-establish that groundwork so the rest of the day has something to build on; those are marked *(recap)* and kept short. Everything else is new ground.

<br><br>

---
<br><br>

# Lab 1: Advanced Delegation — Right Model, Right Context, Right Worker

## Lab Purpose
Climb the delegation ladder: a parameterized command, a hot-reloaded skill, a forked skill, a Haiku-pinned subagent, and finally a fully detached background agent you manage from the CLI.

---
<br><br>

## 1: Start Claude and Initialize *(recap)*
The repo holds a Flask to-do API in `app/` (its tests fail in 4 places *by design*), plus SDK and MCP skeletons for later labs.

**Action:** In the terminal, start Claude, then initialize the project:
```bash
claude
```
```
/init
```

> If Claude offers **"Try the new fullscreen renderer?"**, choose **2. Not now** — the classic renderer matches this lab's screenshots.

`/init` writes a CLAUDE.md with everything it can *discover* — repo layout, test command, even that the failures are deliberate.

![claude.md](./images/ccadv12.png?raw=true "claude.md")

---
<br><br>

## 2: Add a Standing Rule
What `/init` can't discover is *your* policy. **Action:** Type:
```
Add this standing rule to CLAUDE.md: Never run git commit or git push in this repo - I handle version control myself. If you think something should be committed, say so and stop.
```

Click **CLAUDE.md** in the file list to see your rule land in the standing-rules section. Lab 2 comes back to this rule to show how much a CLAUDE.md instruction is really worth.

> **fyi:** shared repo rules → CLAUDE.md; personal facts Claude learns about *you* → auto-memory (`/memory` shows the hierarchy).

![Add rule](./images/ccadv26.png?raw=true "Add rule")

---
<br><br>

## 3: Create a Real Custom Command
**Action:** In a separate terminal tab (keep Claude running), create the folders, then create `.claude/commands/triage.md` with these contents and **save it**:
```bash
mkdir -p .claude/commands .claude/skills
```

```md
---
description: Triage a source file: bugs, risks, and a fix plan
argument-hint: <file-to-triage>
allowed-tools: Bash(git status:*), Bash(git log:*), Read, Grep, Glob
---

## Context

- Current repo status: !`git status --short`
- Project conventions: @CLAUDE.md

## Task

Triage the file $ARGUMENTS:
1) Summarize what it does in 2 sentences.
2) List up to 3 likely bugs or contract violations (cite line numbers).
3) List 3 risks if this shipped to production as-is.
4) Propose the smallest fix plan (max 5 steps). Do not edit any files.
```

Four advanced features here: **`$ARGUMENTS`** (text typed after `/triage`) · **`` !`git status --short` ``** (runs at invocation, output injected) · **`@CLAUDE.md`** (pulled into context) · **`allowed-tools`** (scopes the command, down to `Bash(git status:*)`).

![Creating the triage command](./images/ccadv15.png?raw=true "Creating the triage command")

---
<br><br>

## 4: Restart and Run It
Commands load at **startup**, so your running session doesn't know `/triage` yet.

**Action:** In Claude, type `/exit`, then `claude`, then:
```
/triage app/app.py
```

The triage should flag the API returning **500** where the contract demands **400** or **404**.

![Running the triage command](./images/ccadv2.png?raw=true "Running the triage command")

---
<br><br>

## 5: Turn It Into a Skill — Without Restarting
Commands have **merged into skills**: both paths create `/triage`, same frontmatter.

**Action:** In your other terminal tab:
```bash
mkdir -p .claude/skills/triage
mv .claude/commands/triage.md .claude/skills/triage/SKILL.md
```

**Action:** Back in Claude — **no restart** — run:
```
/triage app/datastore.py
```

It works: skill directories are **watched and hot-reloaded** mid-session. Commands and agents are not.

> **If `/triage` isn't found**, restart once — the watcher only follows directories that existed at session start.

---
<br><br>

## 6: Fork the Skill — Same Context, Separate Worker
`context: fork` runs the skill in a **forked subagent**: it inherits your full conversation, but its work stays out of your main context.

**Action:** Edit `.claude/skills/triage/SKILL.md`, add two lines to the frontmatter, and save:
```md
name: triage
context: fork
```

**Action:** In Claude — still no restart:
```
/triage app/auth.py
```

The triage runs as a delegated task; only the report returns. (The transcript's *"Running in the background as @triage"* means *delegated* — the result still lands here.)

![Forked triage](./images/ccadv16.png?raw=true "Forked triage")

---
<br><br>

## 7: Create a Haiku Subagent
**Action:** In your terminal tab, create the folder and `.claude/agents/test-scout.md` with these contents, and save:
```bash
mkdir -p .claude/agents
```

```md
---
name: test-scout
description: Runs the project test suite and returns a compact failure summary. Reporting only.
model: haiku
disallowedTools: Write, Edit
---

## Instructions
- Run: python3 app/test_app.py
- Report: pass/fail counts, then one line per failure naming the cause.
- Keep the whole report under 10 lines. Never modify files.
```

`model:` pins the subagent to a cheaper, faster model. **Cheap scouts, smart supervisor.**

---
<br><br>

## 8: Restart and Run the Subagent
Agents load at startup (they don't hot-reload).

**Action:** In Claude, `/exit`, then `claude`, then:
```
Use the test-scout subagent to run the test suite and summarize the failures.
```

You get a compact report — 10 passed / 4 failed with causes — run on Haiku, with the verbose test output kept out of your context.

![Haiku test-scout subagent](./images/ccadv8.png?raw=true "Haiku test-scout subagent")

---
<br><br>

## 9: Ask for a Deeper Plan
`ultrathink` anywhere in a prompt requests deeper reasoning **on that turn only**.

**Action:** Type:
```
ultrathink: Propose a refactoring plan for app/ that fixes the 400/404 contract violations without changing test_app.py. Consider at least two approaches and recommend one. Plan only - do not edit files.
```

Skim the plan — Lab 3 will *execute* this exact fix. (Ctrl+O shows the detailed transcript; the session-wide effort dial is on the slides.)

![Extended thinking](./images/ccadv3.png?raw=true "Extended thinking")

---
<br><br>

## 10: Send a Worker to the Background
`claude --bg` starts a **detached session** that keeps working while you do something else — and with nobody there to click "Yes", it must be pre-approved up front: **mode governs edits; `--allowedTools` governs commands.**

**Action:** In your **terminal tab** (leave Claude running), run:
```bash
claude --bg "Run python3 app/test_app.py and write a markdown summary of the failures to bg_report.md - one line per failure naming the contract each violates. Do not run any git commands." --permission-mode acceptEdits --allowedTools "Bash(python3:*)"
```

You get a session ID and management commands back immediately. (The prompt forbids git because your CLAUDE.md rule won't reach the worker's fresh checkout — say it in the prompt.)

![Background agent started](./images/ccadv17.png?raw=true "Background agent started")

---
<br><br>

## 11: Find the Report
**Action:** Still in the terminal tab, list your sessions, then go looking for the report:
```bash
claude agents
```
(Arrow to the worker to watch it; **Esc** leaves the view.) Then:
```bash
cat bg_report.md
cat .claude/worktrees/*/bg_report.md
```

The first `cat` **fails** — and the second finds your four failures. Before writing anything, `--bg` gave the worker **its own worktree checkout** on a `worktree-<name>` branch; your `main` was never touched. `claude rm <id>` removes a session *and* its worktree. *(Slides: "Worktree Isolation".)*

![Agent view](./images/ccadv18.png?raw=true "Agent view")

---
<br><br>

## 12: Exit

**Action:** In prep for the next lab, type `exit` to exit Claude Code.
```
exit
```

## Lab Summary
✅ You've climbed the delegation ladder:
- One-pass setup: CLAUDE.md + the standing rule the whole day leans on
- Built `/triage` with `$ARGUMENTS`, inline bash context, `@file` references and scoped `allowed-tools`
- Converted it to a **skill** — hot-reloaded without a restart
- Forked it with `context: fork` — full conversation, separate workspace
- Delegated verbose test output to a `model: haiku` subagent
- Asked for a deeper plan with `ultrathink`
- Detached a worker with `claude --bg`, pre-approved with mode **and** `--allowedTools`
- Found its output in its own **git worktree** — isolation you can see

> **The decision rule, in one breath:** **subagent** = delegated specialist inside your workflow · **fork** = keep noisy work out of your primary context · **background agent** = independent concurrent session · **worktree** = independent filesystem changes · **cheaper model** = match cost and intelligence to the task.

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 2: Hooks: Enforcing Policy at the Tool Boundary
## Lab Purpose
Create a PreToolUse hook that blocks edits to a protected file and a PostToolUse hook that logs every bash command, then watch both fire — even in bypass-permissions mode.

---
<br><br>

## 1: Set Up the Protected File and Hooks Folder
The policy: nobody edits `config.json` — a stand-in for the credential/config files every real project has.

**Action:** In a regular terminal (not Claude), create the file and the hooks folder:
```
echo '{ "database": { "host": "localhost", "port": 5432 } }' > config.json
mkdir -p .claude/hooks
```

---
<br><br>

## 2: Create the Guard Script
Claude Code sends the tool call as JSON on the script's *stdin*. The script answers with an exit code — **0** = no objection, **2** = block it — and whatever it prints to *stderr* goes back to Claude as the reason.

**Action:** Create `.claude/hooks/protect-config.sh` with these contents, and save it:

```
#!/bin/bash
# PreToolUse guard: block any Edit/Write that targets config.json
FILE=$(jq -r '.tool_input.file_path // ""')

if [[ "$(basename "$FILE")" == "config.json" ]]; then
  echo "POLICY: config.json is protected. Do not modify it. Suggest the change to the user instead." >&2
  exit 2
fi

exit 0
```

![Creating the guard script](./images/cc-se4.png?raw=true "Creating the guard script")

---
<br><br>

## 3: Make the Script Executable
**Action:** Set the execute bit — Claude Code runs the script as a process:
```
chmod +x .claude/hooks/protect-config.sh
```

---
<br><br>

## 4: Wire Up the Hooks in settings.json
Each entry names an *event*, a *matcher* filtering by tool name, and the *handler* to run.

**Action:** Create `.claude/settings.json` with these contents, and save it.

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-config.sh",
            "args": []
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> \"${CLAUDE_PROJECT_DIR}/.claude/bash-command-log.txt\""
          }
        ]
      }
    ]
  }
}
```

`Edit|Write` fires on either tool; `Bash` matches only Bash. The guard uses the *exec form* (`args: []` — no shell); the logger omits `args` and runs in *shell form*, which its `>>` redirect needs.

![The hooks settings file](./images/cc-se5.png?raw=true "The hooks settings file")

---
<br><br>

## 5: Start Claude in Bypass Mode
Hooks fire at the *tool boundary*, outside the permission system — your code keeps its veto even with every permission check off.

**Action:** In a terminal other than your original one, start Claude:
```
claude --dangerously-skip-permissions

  or

claude-yolo (if running in the codespace)
```

> Accept the red **"WARNING: … Bypass Permissions mode"** screen — choose **2. Yes, I accept**. The status line now reads *bypass permissions on*.

---
<br><br>

## 6: Inspect the Hooks with /hooks
**Action:** Type:
```
/hooks
```

The first screen lists hook **events** — yours are **PreToolUse (1)** and **PostToolUse (1)**. This menu only *shows* hooks; to change one you edit `.claude/settings.json`.

![The /hooks menu](./images/cc-se6.png?raw=true "The /hooks menu")

Select **PreToolUse** to see the exit-code legend and your matcher (`[Project] Edit|Write  1 hook`); drill in once more to see the command itself. Hit `Esc` several times to get back to the prompt.

![How the hook works](./images/cc-se8.png?raw=true "How the hook works")

---
<br><br>

## 7: Try to Edit the Protected File
**Action:** Type:
```
Add a connection_timeout setting to config.json using the Edit tool.
```

The tool call is **blocked** before it touches the file, and the hook's stderr message surfaces in the conversation — Claude reads it too.

![Edit blocked by hook](./images/cc-se10.png?raw=true "Edit blocked by hook")

---
<br><br>

## 8: Look at How Claude Reacts
Ours told Claude to suggest the change instead — read its response. Then verify the file is untouched, in your **original (plain) terminal** (in bypass mode, an in-session `! cat` could tempt Claude to *finish* the edit via Bash, which `Edit|Write` doesn't block):
```bash
cat config.json
```

> **Spot the loophole:** the matcher only guards `Edit|Write` — real policies add a Bash matcher too. If Claude offers to work around the block, tell it no.

---
<br><br>

## 9: Generate Some Bash Traffic
PostToolUse fires *after* a tool call succeeds — it can't block, but it's ideal for auditing and logging.

**Action:** Type:
```
Use bash to list the files in this project and count the lines in app/app.py.
```

Let Claude run its commands.

---
<br><br>

## 10: Check the Audit Log
**Action:** Type:
```
! cat .claude/bash-command-log.txt
```

Each command Claude ran is there, with its description. Your own `!` commands are **not** — they don't go through the Bash tool, so PostToolUse never fires. The log is Claude's activity, not yours.

![The bash command log](./images/cc-se11.png?raw=true "The bash command log")

---
<br><br>

## 11: Prompt vs. Tool vs. Hook Constraints
Four ways to say "don't do that," in rising order of strength. (Reading only)

- **Prompt constraint** — CLAUDE.md instructions (like Lab 1's *"never commit"* rule): durable, but still only a request.
- **Tool constraint** — `disallowedTools` removes the tool entirely, for one agent.
- **Classifier** — auto mode's second *model* judging each risky call: probabilistic.
- **Hook** — your code, on *every* tool call. Exit 2 is a hard no, even in bypass mode.

> Hooks can also return JSON decisions, rewrite inputs, or inject context, with more handler types and events — full schema: [hooks reference](https://code.claude.com/docs/en/hooks).

---
<br><br>

## 12: Exit

**Action:** In prep for the next lab, type `exit` to exit Claude Code.

```
exit
```

## Lab Summary
✅ You've successfully:
- Blocked edits to a protected file with a PreToolUse hook
- Used exit 2 + stderr to veto a call and explain why
- Logged every bash command with a PostToolUse hook
- Verified hooks with `/hooks`
- Proved hooks fire in bypass mode, outside auto mode's classifier
- Placed hooks in the constraint hierarchy

<br><br>
---
## END OF LAB
---
<br><br>
# Lab 3: Loops Instead of Prompts — `/goal` and `/loop`
## Lab Purpose
Use `/goal` to keep a session working until a condition holds (the **inner loop**), `/loop` to re-run work on a schedule (the **outer loop**), and `claude -p` to run a goal with no session at all — then read how GitHub Actions moves it off your machine. Estimated time: 10-12 minutes.

**NOTE: Steps 1-8 run in an interactive Claude session. Step 9 runs in a regular terminal. Steps 10-11 are reading.**

---
<br><br>

## 1: Work on a Throwaway Branch
`/goal` is about to change real files, and Lab 5 still needs this project's tests to fail.

**Action:** In a terminal, run:
```bash
git switch -c loop-lab
```

Then start Claude in that same directory:
```bash
claude
```

---
<br><br>

## 2: Set a Goal
`/goal` sets a **completion condition**. After every turn a small fast model (Haiku) checks it; until it holds, Claude takes another turn on its own instead of handing control back to you.

**Action:** At the Claude prompt, type:
```
/goal python3 app/test_app.py reports 14 passed, 0 failed and exits 0. Never edit app/test_app.py - it defines the contract.
```

Setting the goal **starts a turn immediately** — watch for `◎ /goal active` and let it run.

![goal set](./images/ccadv19.png?raw=true "goal set")

> **This is Lab 1's plan, executed.** In Lab 1 you had Claude *plan* the 400/404 fix; here it does the work and decides for itself when it's finished.

---
<br><br>

## 3: Watch the Evaluator's Verdicts
Three verdicts: **not yet met** (the reason feeds back as guidance), **met**, or **impossible**.

**Action:** Press *Ctrl+O* to expand the detailed transcript and read the **Reason:** line under the verdict.

> Claude usually fixes all four routes in one turn, so expect a single `✓ Goal achieved (… · 1 turn · …)`. And note the condition names a *command whose output lands in the transcript* — the evaluator has **no tools**, so "the code is clean" would be unjudgeable.

![goal verdicts](./images/ccadv20.png?raw=true "goal verdicts")

---
<br><br>

## 4: Check Goal Status
**Action:** When the run settles, type `/goal` with no arguments:
```
/goal
```

You get the verdict, condition, runtime, turns and token spend. (The evaluator's *reason* isn't on this card — that's the `Ctrl+O` view.)

![goal status](./images/ccadv21.png?raw=true "goal status")

---
<br><br>

## 5: Confirm the Work, Then Put It Away
**Action:** In a terminal (not the Claude session), run:
```bash
python3 app/test_app.py
git diff --stat
```

You should see `14 passed, 0 failed`, and a diff touching `app/app.py` only — **not** `app/test_app.py`. Now commit it to the throwaway branch and go back:
```bash
git add -A && git commit -m "goal: fix 400/404 contract violations"
git switch -
```

`python3 app/test_app.py` should report `10 passed, 4 failed` again — Lab 5 needs those failures. The fix stays on `loop-lab`.

---
<br><br>

## 6: Schedule a Repeating Prompt with `/loop`
That was the inner loop; `/loop` re-runs a prompt on an interval for as long as the session stays open.

**Action:** Back in the Claude session, type:
```
/loop 2m append the current UTC time and the current test pass/fail counts as one line in beat.md
```

Claude converts the interval to a cron expression and calls the `CronCreate` tool:

```
● CronCreate(*/2 * * * * : append the current UTC time…)
  ⎿  Scheduled 8db547d2 (Every 2 minutes)
```

![loop scheduled](./images/ccadv22.png?raw=true "loop scheduled")

> Leave it running and move on. Units are `s`/`m`/`h`/`d`; cron granularity is one minute, and fire times jitter — up to half the interval late.

---
<br><br>

## 7: Give Bare `/loop` a Default Prompt
`/loop` with **no prompt** runs a built-in maintenance prompt; a `loop.md` file replaces it with your own.

**Action:** Create `.claude/loop.md` with these contents, and save:

```markdown
Run python3 app/test_app.py. If anything fails, report the failing test
names and the contract each one violates - do not fix them.
If everything passes, say so in one line.
```

Project scope (`.claude/loop.md`) wins over user scope (`~/.claude/loop.md`), and edits take effect on the next iteration.

---
<br><br>

## 8: Inspect and Cancel the Loop
Scheduled tasks are **session-scoped**: they die with the conversation, restore on `claude --resume`, and expire after 7 days.

**Action:** Check that the loop has fired at least once:
```
! cat beat.md
```

Then ask for the task list and cancel it in plain English:
```
what scheduled tasks do I have? cancel the beat.md one
```

Claude uses `CronList` and `CronDelete` under the hood.

![loop cancelled](./images/ccadv23.png?raw=true "loop cancelled")

---
<br><br>

## 9: The Same Loop With No Session at All
`/goal` also works headless — one invocation runs the whole loop to completion. This is the unit that CI, cron and scripts multiply.

**Action:** Exit Claude (*Ctrl+D*) and run in the terminal:
```bash
claude -p "/goal beat.md exists and its last line names the current test pass/fail counts" \
  --permission-mode acceptEdits --allowedTools "Bash(python3:*)" \
  --output-format json | jq '{result, num_turns, total_cost_usd}'
```

`-p` works, prints, and exits; the JSON wrapper makes every run scriptable and auditable. Expect roughly **3 turns and a few cents**.

![headless goal](./images/ccadv24.png?raw=true "headless goal")

> **`-p` has no human to click "Yes"** — it starts in `default` mode whatever your interactive default is, so unattended runs pre-approve with `--permission-mode` **and** `--allowedTools`. Drop the `--allowedTools` half and it does *not* fail loudly: `acceptEdits` covers writes, not Bash, so the goal stays unmet and Claude eventually **improvises** — reasoning out what the counts "must be" and writing a confident, wrong `12 passed, 4 failed` (measured: 9 turns / ~$0.41 fabricated vs 3 turns / ~$0.05 real). Bound what it may do, then check what it actually ran. *(Slides: "Anatomy of a Reliable Loop".)*

---
<br><br>

## 10: The Same Engine on GitHub's Runners
`claude-code-action@v1` runs this exact engine in CI. (Reading only — the workshop repo isn't yours to wire up.)

**The responder.** With **no `prompt:`**, a teammate comments `@claude fix the TypeError` on a PR or issue, and Claude answers on GitHub's runners:

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

**The outer loop in CI.** With a **`prompt:`** and a `schedule:` trigger, it's `/loop` on infrastructure that doesn't need your laptop open:

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * 1-5"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Run python3 app/test_app.py and summarize the failures as a markdown report"
          claude_args: |
            --max-turns 5
            --model sonnet
```

`claude_args` passes through the same CLI flags you used in step 9 — `--max-turns`, `--allowedTools`, `--model`, `--append-system-prompt`.

---
<br><br>

## 11: Know the Bounds
Every loop needs a stop condition, and every unattended loop needs a budget. (Reading only)

- **Bound the goal** — a condition can carry its own limit: `…or stop after 20 turns`.
- **Bound the job** — `--max-turns` plus a workflow-level `timeout-minutes`.
- **`/loop`'s reach** — its tasks fire only while the session is open; to outlive one, use cloud Routines, a Desktop scheduled task, or a `schedule:` trigger.
- **CI security baseline** — the key comes only from `${{ secrets.ANTHROPIC_API_KEY }}`; minimal App permissions; review Claude's PRs like any contributor's.

> **Homework:** in a repo you own, `/install-github-app` sets up the app and secret; commit `claude.yml`, open an issue, and comment `@claude suggest an improvement to the README`.

## Lab Summary
✅ You've mastered:
- `/goal` — an inner loop that works until a condition holds, judged by a separate evaluator model
- Reading the evaluator's verdicts, and writing a condition it can actually judge
- `/loop` — an outer loop on an interval, backed by `CronCreate` / `CronList` / `CronDelete`
- `loop.md` — replacing the built-in maintenance prompt with your own
- Running the same goal headless with `claude -p` and `--output-format json`
- How `claude-code-action@v1` runs the same engine in CI (reference)
- Bounding a loop: stop clauses, `--max-turns`, `timeout-minutes`

<br><br>
---
## END OF LAB
---
<br><br>
# Lab 4: Agent SDK: Programmatic and Unattended Loops
## Lab Purpose
Run the **same Claude agent from a small Python program** — first read-only, then *unattended*, doing real work safely with nobody watching. Estimated time: 10-12 minutes.

> **In one line:** the `claude` command is a finished app; the **Agent SDK** is that same engine as a Python library. `query()` does what `claude -p "..."` did in Lab 3, and you set permissions *in code*.

> **Diff-merge steps:** `code -d extra/<finished> sdk/<skeleton>` opens the finished file (**left**) beside your skeleton (**right**). Copy each highlighted block left → right (gutter arrow toward the right, or copy/paste) until nothing is highlighted, then **save the right file** (Cmd/Ctrl+S). A skeleton run before merging prints *"still the skeleton"* and stops — re-open the diff, merge what remains, save.

---
<br><br>

## 1: Install the Agent SDK (Skip if running in a Codespace.)
**Action:** In a terminal, run:
```bash
python3 -m pip install claude-agent-sdk
```

> The SDK drives the bundled CLI, so it rides your existing CLI login here — the developer loop. *Shipping* is different: distributed products can't offer claude.ai login and authenticate with an `ANTHROPIC_API_KEY` (or Bedrock / Vertex / Foundry) — the same secret Lab 3's CI workflows used.

---
<br><br>

## 2: View the Skeleton
**Action:** Open the skeleton:
```bash
code sdk/agent_loop.py
```

The imports name the pieces you'll use — `query`, `ClaudeAgentOptions`, `AssistantMessage`, `ResultMessage`. The body of `run_agent()` is a placeholder; you'll merge in the **options** (pre-approved tools plus a turn cap) and the **message loop**.

![skeleton view](./images/cc-se58.png?raw=true "skeleton view")

---
<br><br>

## 3: Diff, Merge, and Map It to the CLI
**Action:** Run the diff, merge the **one highlighted region** (the body of `run_agent()`), save the right file, and close the tab:
```bash
code -d extra/agent_loop.txt sdk/agent_loop.py
```

Every piece maps to something you've already used:

| SDK piece (now in your file) | CLI equivalent you've used |
|---|---|
| `query(prompt=..., options=...)` | `claude -p "<prompt>"` (Lab 3) |
| `ClaudeAgentOptions(allowed_tools=[...])` | `--allowedTools "..."` (Lab 3) |
| `ClaudeAgentOptions(max_turns=...)` | `--max-turns` / `claude_args` (Lab 3) |
| iterating `AssistantMessage` / `ToolUseBlock` / `ResultMessage` | `--output-format stream-json` events |

`query()` returns an async iterator; your loop prints `[claude]` lines for text and `[tool]` lines for each call, ending with a `ResultMessage` of stats.

![diff merge](./images/cc-se59.png?raw=true "diff merge")

---
<br><br>

## 4: Run Your Agent
**Action:** Run:
```bash
python3 sdk/agent_loop.py "What files are in the sdk directory? Answer in one sentence."
```

You'll see `[claude]` lines, likely a `[tool]` line or two, then the stats.

> **`allowed_tools` is not an exhaustive whitelist** — a built-in set of read-only commands (`ls`, `cat`, `git status`, ...) never needs approval, so a `[tool] Bash` line here is normal. `allowed_tools` governs the calls that would otherwise stop and ask — which step 6 shows with `Write`.

![sdk run](./images/cc-se60.png?raw=true "sdk run")

---
<br><br>

## 5: Force Multiple Turns
**Action:** Run a prompt that forces tool use:
```bash
python3 sdk/agent_loop.py "Find every TODO comment in the .py files under sdk/ and mcpserver/ and list them"
```

Watch the `[tool]` lines: read-only calls (`Grep`, usually more than once), then the answer. Each `[tool]` line is one trip around the loop; **Turns used** counts those trips.

![sdk run](./images/cc-se61.png?raw=true "sdk run")

---
<br><br>

## 6: Try to Write Without Pre-Approval
**Action:** Run:
```bash
python3 sdk/agent_loop.py "Create a file named sdk_test.txt containing hello"
```

The write isn't blocked — it just isn't *pre-approved*, and with no human attached it can't proceed. Confirm nothing was created: `ls sdk_test.txt`.

![sdk run](./images/cc-se62.png?raw=true "sdk run")

---
<br><br>

## 7: View the Unattended Skeleton and Its Gate
Unattended there is no human to ask, so your code must decide — and must see **every** call.

**Action:** Open it:
```bash
code sdk/auto_agent.py
```

The gate is a **PreToolUse hook** — `gatekeeper()` — run by the CLI *before* each tool executes, returning `"allow"` or `"deny"`. Lab 2's idea, in Python, inside your own program. (The `prompt_stream()` generator is what lets the hook run as the agent works.)

![skeleton view](./images/cc-se70.png?raw=true "skeleton view")

> **SDK sessions start in `default` mode** whatever your interactive default is — permissions in code are not optional. And by default the SDK reads the same disk config as the CLI (settings, `CLAUDE.md`, `.claude/` skills/agents — so your Lab 2 hook is still armed and fires alongside `gatekeeper()`); `setting_sources=[]` is the isolation switch for multi-tenant deployments.

> **Why a hook, not `can_use_tool`?** The `can_use_tool` callback is consulted only for calls that resolve to **"ask"** — anything already permitted sails past it. A PreToolUse hook fires on **every** call.

---
<br><br>

## 8: Diff and Merge the Unattended Agent
**Action:** Run the diff. This time there are **two highlighted regions** — the `gatekeeper()` body and the `main()` body. Merge **both** left → right, save the right file, and close:
```bash
code -d extra/auto_agent.txt sdk/auto_agent.py
```

![diff merge auto](./images/cc-se71.png?raw=true "diff merge auto")

---
<br><br>

## 9: Run It Unattended
**Action:** Run:
```bash
python3 sdk/auto_agent.py
```

Watch the `[gatekeeper] allowing: ...` lines (one per tool used), then the final turn count. Check the product:
```bash
cat agent_report.md
```

You should see every `.py` file in `app/` listed with a one-line description.

![gatekeeper run](./images/cc-se73.png?raw=true "gatekeeper run")

---
<br><br>

## 10: Trigger the Deny Path
**Action:** In `sdk/auto_agent.py`, replace the **whole** `TASK = ( … )` block — all three lines, through the closing `)` — with this single line, and **save**:
```python
TASK = "Use a Bash rm command to delete agent_report.md. Then say DONE."
```
(Replacing only the first line leaves fragments behind and Python stops with an `IndentationError`.)

Run it again (`python3 sdk/auto_agent.py`) and watch for the deny line:
```
  [gatekeeper] DENIED: Bash -> 'rm -f agent_report.md'
```

Claude still says `DONE` because the task told it to — the `Result:` line proves nothing. The proof is the deny line *and* the file still being there:
```bash
ls agent_report.md
```

![gatekeeper run](./images/cc-se74.png?raw=true "gatekeeper run")

---
<br><br>

## 11: Connect It Back to the CLI
**Action:** Run the read-only program's CLI equivalent and compare:
```bash
claude -p "What files are in the sdk directory? Answer in one sentence." --output-format json | jq '{result: .result, num_turns: .num_turns, duration_ms: .duration_ms}'
```

The JSON fields mirror the `ResultMessage` attributes your program printed. Same loop, different driver.

> **Going further:** Lab 1's **auto-memory** loads into the SDK's system prompt at session start — but it saves with the ordinary `Write`/`Edit` tools, so an `allowed_tools` that omits `Write` silently can't record. Disable with `autoMemoryEnabled: false`. See the [Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/overview).

---
<br><br>

## Lab Summary
✅ You've built and exercised:
- A read-only `query()` loop merged from skeleton to working program
- An unattended agent gated by a PreToolUse hook, plus `allowed_tools` and `max_turns`
- Why `can_use_tool` is not a universal gate (it only sees "ask" calls)
- The deny path — blocking a destructive command programmatically
- The CLI-to-SDK mapping: same loop, programmatic driver
- That the SDK loads `.claude/` config by default; `setting_sources=[]` is the isolation switch

<br><br>
---
## END OF LAB
---
<br><br>
# Lab 5: Capstone: Build a Custom MCP Server
## Lab Purpose
You've *used* MCP servers; now **build one**. Complete a Python FastMCP server exposing three "project health" tools, register it at project scope, and drive it from natural-language prompts. Estimated time: 10-12 minutes.

> **MCP in one paragraph:** an MCP server is a process Claude Code talks to over stdin/stdout (or HTTP), exposing *tools* Claude can call. Add one with `claude mcp add <name> -- <command>`, inspect it with `/mcp`; its tools are named `mcp__<server>__<tool>`. Today the server is yours.

---
<br><br>

## 1: Tour the Server Skeleton
FastMCP makes a server out of ordinary Python functions: decorate one with `@mcp.tool()` and its **docstring and type hints become the tool's documentation and input schema** — what Claude reads when choosing a tool.

**Action:** Open the skeleton:
```bash
code mcpserver/project_server.py
```

Already in place: the `FastMCP("project-health")` instance (that name becomes the `mcp__project-health__...` prefix) and the `mcp.run()` call that starts the stdio transport. The three tools are missing — that's your merge.

---
<br><br>

## 2: Prove It's Still the Skeleton
**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

You should see the *"still the skeleton"* message and the program stops.

---
<br><br>

## 3: Diff-Merge the Three Tools
The diff is exactly the three `@mcp.tool()` functions: `run_tests()` (runs `app/test_app.py`), `count_todos()` (TODO/FIXME counts per file), and `project_stats()` (file and line counts).

**Action:** Run the diff, merge the **one highlighted region** left → right, save the right file, and close the tab:
```bash
code -d extra/project_server.txt mcpserver/project_server.py
```

As you merge, read the docstrings — each tells Claude *when* to reach for that tool.

![diff merge server](./images/ccadv4.png?raw=true "diff merge server")

---
<br><br>

## 4: Start It Once by Hand
"Success" for a stdio server is **silence** — it's waiting for a client to speak JSON-RPC on stdin.

**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

Nothing appears — correct. (The skeleton message means the merge didn't save.) Stop it with `Ctrl+C` — the long `KeyboardInterrupt` traceback is expected, not a failure. From now on Claude Code starts and stops this process for you.

---
<br><br>

## 5: Register It at Project Scope
Project scope writes the config to `.mcp.json` in the repo root — commit it and everyone who clones the project gets your server.

**Action:** Run (the `--` separates Claude's options from the server's command line):
```bash
claude mcp add project-health --scope project -- python3 mcpserver/project_server.py
```

Then look at the shareable artifact that just appeared — plain JSON, no secrets:
```bash
cat .mcp.json
```

![mcp json](./images/cc-se16.png?raw=true "mcp json")

---
<br><br>

## 6: Health-Check the Connection
`claude mcp list` actually starts each server and reports whether it connects — your first diagnostic stop.

**Action:** Run:
```bash
claude mcp list
```

At project scope it shows **⏸ Pending approval (run `claude` to approve)** — project-scoped servers stay unapproved until you accept them in a session, next. On a connection *error*, run the server by hand (step 4) and read the message — with your own server, *you* are the maintainer.

![mcp list](./images/cc-se13.png?raw=true "mcp list")

---
<br><br>

## 7: Start Claude and Approve Your Server
Because `.mcp.json` can arrive in a repo from *anyone*, Claude Code asks before running project-scoped servers.

**Action:** Start Claude (*don't use* bypass mode here) and approve the server when prompted:
```bash
claude
```

![Approving the MCP server](./images/cc-se17.png?raw=true "Approving the MCP server")

---
<br><br>

## 8: Inspect It with /mcp
**Action:** Type:
```
/mcp
```

Select the **project-health** server and browse its three tools. Select one — the **Full name** (`mcp__project-health__run_tests`) and a **Description** that is your merged docstring, word for word: the entire basis on which Claude decides to reach for this tool. `Esc` back to the prompt.

![mcp panel](./images/ccadv5.png?raw=true "mcp panel")

---
<br><br>

## 9: Drive the Server: Run the Test Suite
**Action:** Type:
```
Use the project-health server to run the test suite and summarize what's failing and why.
```

Claude calls `mcp__project-health__run_tests`, gets your captured test output back, and explains the four contract violations — the ones `/triage` found in Lab 1, now through a tool you built.

![run tests tool](./images/ccadv6.png?raw=true "run tests tool")

---
<br><br>

## 10: Drive the Server: Full Health Report
**Action:** Type:
```
Using the project-health tools, give me a one-paragraph health report on this repo: test status, TODO count, and overall size.
```

You should see a line like **`Called project-health 2 times`**, then a synthesized report — *Ctrl+o* expands the transcript to watch the real `mcp__project-health__...` names go by.

> **Tie-back to Lab 2:** those full names are what a hook matcher targets — `"matcher": "mcp__project-health__.*"` governs *your own server's* tools the way it governed Edit/Write.

![health report](./images/ccadv7.png?raw=true "health report")

---
<br><br>

## 11: Where to Take It
Everything beyond this is more of the same pattern. (Reading only)

- **More tools:** anything a Python function can do becomes a tool with one decorator and a good docstring.
- **Arguments:** typed parameters (`def run_tests(pattern: str) -> str:`) — FastMCP builds the schema.
- **Beyond stdio:** the same code can serve HTTP (`claude mcp add --transport http <url>`).
- **Distribution:** `.mcp.json` in the repo (done!), or package it with a plugin.

---
<br><br>

## 12: Exit (and Optional Cleanup)

**Action:** Type `exit` to leave Claude. To remove the server registration afterwards:
```bash
claude mcp remove project-health
```

(Leaving it is fine too — it's your repo's feature now.)

## Lab Summary
✅ In the capstone you've:
- Completed a FastMCP server: three `@mcp.tool()` functions whose docstrings are the tool documentation
- Learned the stdio contract (silence = waiting for a client)
- Registered it at project scope and read the shareable `.mcp.json`
- Approved and inspected it with `/mcp`
- Driven it from natural language, single- and multi-tool
- Connected the picture: commands → hooks → loops (`/goal`, `/loop`) → headless/CI → SDK → your own MCP server

<br><br>
---
## END OF LAB
---
<br><br>
<p align="center">
<b>For educational use only by the attendees of our workshops.</b>
</p>
<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
