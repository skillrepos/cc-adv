# Advanced Claude Code: True AI Productivity
## Go beyond the basics — advanced delegation, hooks, loops, the Agent SDK, and your own MCP server
## Session Labs
## Revision 1.39 - 08/25/26

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

> If Claude offers **"Try the new fullscreen renderer?"**, choose **2. Not now** — the classic renderer matches this lab's screenshots.

> For creating/editing files: If running in the codespace you can use the command `code <filename>`.  And use `Ctrl+S` (Windows) or `Cmd+S` (Mac)
to save changes.  If running locally, use whatever editor you prefer.
<br><br>

**NOTE:** This course assumes you are already comfortable with the Claude Code basics — running it, permission modes, `/init` and CLAUDE.md, skills, subagents and custom commands. A few steps re-establish that groundwork so the rest of the day has something to build on. Everything else is new ground.

<br><br>

---
<br><br>

# Lab 1: Advanced Delegation — Right Model, Right Context, Right Worker

## Lab Purpose
See how we can delegate work at different levels: a parameterized command, a hot-reloaded skill, a forked skill, a Haiku-pinned subagent, and finally a fully detached background agent you manage from the CLI.

---
<br><br>

## 1: Start Claude and Initialize
This repo holds a Flask to-do API in `app/` (its tests fail in 4 places *by design*), plus SDK and MCP skeletons for later labs.
Let's get Claude to learn about the repo.

**Action:** In the terminal, start Claude, then initialize the project:
```bash
claude
```
Type in Claude:

```
/init
```

`/init` writes a CLAUDE.md with everything it can *discover* — repo layout, test command, even that the failures are deliberate.

![claude.md](./images/ccadv12.png?raw=true "claude.md")

---
<br><br>

## 2: Add a Standing Rule
What `/init` can't discover is *your* policy. Let's add a rule ourselves for that. 

**Action:** In Claude, type:
```
Add this standing rule to CLAUDE.md: Never run git commit or git push in this repo - I handle version control myself. If you think something should be committed, say so and stop.
```

Open **CLAUDE.md** to see your rule in the standing-rules section. (In the codespace, you can click the file in the file list.)

![Add rule](./images/ccadv26.png?raw=true "Add rule")

---
<br><br>

## 3: Create a Custom Command

**Action:** In a separate terminal tab (keep Claude running), create folders for commands and skills. 

```bash
mkdir -p .claude/commands .claude/skills
```

Now create the file `.claude/commands/triage.md` with these contents and **save it**:

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

There are four advanced features in the file: **`$ARGUMENTS`** (text typed after `/triage`) · **`` !`git status --short` ``** (runs at invocation, output injected) · **`@CLAUDE.md`** (pulled into context) · **`allowed-tools`** (scopes the command, down to `Bash(git status:*)`).

![Creating the triage command](./images/ccadv15.png?raw=true "Creating the triage command")

---
<br><br>

## 4: Restart Claude and Run the Command.
Commands load at **startup**, so your running session doesn't know `/triage` yet.

**Action:** In Claude, type `/exit`. Then start Claude via `claude`, and run the command below in Claude:

(If Claude offers **"Try the new fullscreen renderer?"**, choose **2. Not now**.)

```
/triage app/app.py
```

The triage should flag the API returning **500** where the contract demands **400** or **404**.

![Running the triage command](./images/ccadv2.png?raw=true "Running the triage command")

---
<br><br>

## 5: Turn the Command Into a Skill — Without Restarting
Commands have been **merged into skills**: both paths create `/triage`, same frontmatter. What changes is *who can invoke it*. To see this, we'll move the file to the skills area.

**Action:** In your other terminal tab (one where Claude is not running):
```bash
mkdir -p .claude/skills/triage
mv .claude/commands/triage.md .claude/skills/triage/SKILL.md
```

**Action:** Back in Claude — **no restart** — run:
```
/triage app/datastore.py
```

It works: skill directories are **watched and hot-reloaded** mid-session. Commands and agents are not.

**And `/triage` is no longer only yours to run.** A command's `description` is autocomplete text — nothing happens until you type the slash. A skill's `description` goes into Claude's *context*, so Claude can reach for it on its own. **A command is a skill only you can invoke.** 

> **If `/triage` isn't found**, restart once — the watcher only follows directories that existed at session start.

---
<br><br>

## 6: Next Level: Fork the Skill — Same Context, Separate Worker
`context: fork` runs the skill in a **forked subagent**: it inherits your full conversation, but its work stays out of your main context.

**Action:** Edit `.claude/skills/triage/SKILL.md`, add two lines to the frontmatter (see screenshot), and save:
```md
name: triage
context: fork
```

![Adding fields](./images/ccadv27.png?raw=true "Adding fields")

**Action:** In Claude, run the command below (no restart needed):
```
/triage app/auth.py
```

The triage runs as a delegated task; only the report returns. (The transcript's *"Running in the background as @triage"* means *delegated* — the result still lands here.)

![Forked triage](./images/ccadv16.png?raw=true "Forked triage")

---
<br><br>

## 7: Create a Subagent bound to a cheaper, smaller model

**Action:** Let's create a subagent that uses the smaller, cheaper Haiku model. In your terminal tab, create the *agents* folder:

```bash
mkdir -p .claude/agents
```

Next, create `.claude/agents/test-scout.md` with these contents, and save:

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

## 8: Restart Claude and Run the Subagent
Agents load at startup (they don't hot-reload).

**Action:** In Claude, `/exit`, then  start it again with `claude`, then enter (in Claude):
```
Use the test-scout subagent to run the test suite and summarize the failures.
```

You get a compact report — 10 passed / 4 failed with causes.  This was run on Haiku, with the verbose test output kept out of your context.

![Haiku test-scout subagent](./images/ccadv8.png?raw=true "Haiku test-scout subagent")

---
<br><br>

## 9: Send a Worker to the Background

`claude --bg` starts a **detached session** that keeps working while you do something else. With nobody there to click "Yes", a worker must never have to *wait* for approval.  So we pass several command line options: `--permission-mode dontAsk` **auto-denies** anything not pre-approved instead of queuing a question nobody will answer. And `--allowedTools` lists/allows exactly what the job needs. In this case, that's the test command and the report write.

**Action:** In a separate **terminal tab** (leave Claude running), run this complete command:

```bash
claude --bg "Run python3 app/test_app.py and write a markdown summary of the failures to bg_report.md - one line per failure naming the contract each violates. python3 is on your PATH - run the tests directly and do not probe the environment first. Do not run any git commands." --permission-mode dontAsk --allowedTools "Bash(python3:*),Write"
```

You get a session ID and management commands back immediately. 

![Background agent started](./images/ccadv17.png?raw=true "Background agent started")

---
<br><br>

## 10: (OPTIONAL) View and Drill into the Agents List
**Action:** Still in the terminal tab, list your sessions. After the agent is done, you can view the report:
```bash
claude agents
```

![Agent view — worker completed](./images/ccadv28.png?raw=true "Agent view — worker completed")

(Some navigation controls to be aware of: Two levels here: in the list, **Space** peeks at the worker — **Enter** opens its full transcript, where **Esc** does nothing and **←** brings you back to the list, as the status line says. **Esc** closes the list itself.) 

Now, you can view the report, which is stored in a separate Git working directory call a *worktree*:
```bash
cat .claude/worktrees/*/bg_report.md
```

Before writing anything, `--bg` gave the worker **its own worktree checkout** on a `worktree-<name>` branch; your `main` was never touched. `claude rm <id>` removes a session *and* its worktree.


---
<br><br>

## 11: Exit

**Action:** In prep for the next lab, type `/exit` to exit Claude Code.
```
/exit
```

## Lab Summary
✅ You've climbed the delegation ladder:
- One-pass setup: CLAUDE.md + your own rule
- Built `/triage` with `$ARGUMENTS`, inline bash context, `@file` references and scoped `allowed-tools`
- Converted it to a **skill** — hot-reloaded without a restart
- Forked it with `context: fork` — full conversation, separate workspace
- Delegated verbose test output to a `model: haiku` subagent
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

## 1: Set Up the Protected File and Hooks Folder to Implement a Policy.

The policy we'll enforce is that nobody is allowed to edit `config.json` via Claude. (The file is just a stand-in for the credential/config files every real project has.)

**Action:** In a regular terminal (not Claude), create the file and the hooks folder:
```
echo '{ "database": { "host": "localhost", "port": 5432 } }' > config.json
mkdir -p .claude/hooks
```

---
<br><br>

## 2: Create the Guard Script That will be used by the Hook

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

Each entry names an *event*, a *matcher* filtering by tool name, and the *handler* to run. Notice that we're adding not only the hook to protect the config file, but also a second hook that will log bash commands that Claude runs.

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

In the *matcher* sections, `Edit|Write` fires on either tool; `Bash` matches only Bash. The guard uses the *exec form* (`args: []` — no shell); the logger omits `args` and runs in *shell form*, which its `>>` redirect needs.

![The hooks settings file](./images/cc-se5.png?raw=true "The hooks settings file")

---
<br><br>

## 5: Start Claude in Bypass Mode

Hooks fire at the *tool boundary*, outside the permission system — your hook code is checked even with every permission check off.

**Action:** In a terminal other than your original one, start Claude:
```
claude --dangerously-skip-permissions

  or

claude-yolo (if running in the codespace)
```

> Pay attention on the warning screen — choose **2. Yes, I accept**. The status line now reads *bypass permissions on*.

---
<br><br>

## 6: Inspect the Hooks with /hooks
**Action:** In Claude, type:
```
/hooks
```

The screen that comes up lists hook **events** — yours are **PreToolUse (1)** and **PostToolUse (1)**. (This menu only *shows* hooks; to change one you edit `.claude/settings.json`.)

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


## 8: Generate Some Bash Traffic
PostToolUse fires *after* a tool call succeeds — it can't block, but it's ideal for auditing and logging. So we'll create some activity to be logged by it.

**Action:** Type:
```
Use bash to list the files in this project and count the lines in app/app.py.
```

Let Claude run its commands.

---
<br><br>

## 9: Check the Audit Log
**Action:** Type:
```
! cat .claude/bash-command-log.txt
```

Each command Claude ran is there, with its description. Your own `!` commands are **not** — they don't go through the Bash tool, so PostToolUse never fires. The log is Claude's activity, not yours.

![The bash command log](./images/cc-se11.png?raw=true "The bash command log")

---
<br><br>

## 10: Exit

**Action:** In prep for the next lab, type `/exit` to exit Claude Code.


> Hooks can also return JSON decisions, rewrite inputs, or inject context, with more handler types and events — full schema: [hooks reference](https://code.claude.com/docs/en/hooks).

---
<br><br>

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
Use `/goal` to keep a session working until a condition holds (the **inner loop**), `/loop` to re-run work on a schedule (the **outer loop**), and `claude -p` to run a goal with no session at all. 

**NOTE: Steps 1-8 run in an interactive Claude session. Step 9 runs in a regular terminal. Step 10 is reading.**

---
<br><br>

## 1: Work on a Throwaway Branch
`/goal` is about to change real files, and Lab 5 still needs this project's tests to fail. So we'll use Git to work in another branch temporarily.

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
`/goal` sets a **completion condition**. After every turn a small fast model (default is Haiku) checks it; until it holds, Claude takes another turn on its own instead of handing control back to you.

**Action:** At the Claude prompt, type:
```
/goal python3 app/test_app.py reports 14 passed, 0 failed and exits 0. Never edit app/test_app.py - it defines the contract.
```

Setting the goal **starts a turn immediately** — watch for `◎ /goal active` and let it run.

![goal set](./images/ccadv19.png?raw=true "goal set")

> **This is Lab 1's plan, executed.** In Lab 1 you had Claude *plan* the 400/404 fix; here it does the work and decides for itself when it's finished.

---
<br><br>

## 3: Read the Verdict
Claude usually fixes all four routes in one turn, so expect a single result card:

```
✔ Goal achieved (18s · 1 turn · 1.3k tokens)
  Goal: python3 app/test_app.py reports 14 passed, 0 failed and exits 0. …
  Reason: The transcript shows the output: "14 passed, 0 failed" …
```

**Action:** Read the **Reason:** line. That is the evaluator — a separate call — saying *why* it accepted, and it is the whole mechanism: the evaluator has **no tools**, so it can only judge what Claude already put in the transcript. That is why the condition names a *command whose output lands there*; "the code is clean" would be unjudgeable.


![goal verdicts](./images/ccadv20.png?raw=true "goal verdicts")

---
<br><br>

## 4: Check Goal Status
**Action:** When the run settles, type `/goal` with no arguments:
```
/goal
```

You get the verdict, condition, runtime, turns and token spend. (More info can be seen with the `Ctrl+O` toggle.)

![goal status](./images/ccadv21.png?raw=true "goal status")

---
<br><br>

## 5: Confirm the Fixes, then Restore the Failures so they're in place for Lab 5.

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
The `/goal` from steps 2-4 was the **inner loop**: one session working turn after turn until its condition held. `/loop` is the **outer loop**: it re-runs a prompt you give it on a timer, for as long as the session stays open.

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

> Leave it running and move on. Intervals take `s`/`m`/`h`/`d` units; cron underneath means nothing fires more than once a minute. Fire times are also deliberately staggered (so everyone's tasks don't hit at the same instant) by up to half the interval — so expect lines ~2 minutes apart but *not on* the 2-minute marks, and allow up to ~3 minutes for the first one. It isn't broken, it's pacing.

---
<br><br>

## 7: Give Bare `/loop` a Default Prompt
Step 6's loop ran a prompt you typed. Plain `/loop` — no prompt at all — also works: it falls back to a **maintenance prompt**, generic "check on the project" housekeeping instructions built into Claude Code. A `loop.md` file replaces that generic default with standing instructions of your own.

**Action:** Create `.claude/loop.md` with these contents, and save:

```markdown
Run python3 app/test_app.py. If anything fails, report the failing test
names and the contract each one violates - do not fix them.
If everything passes, say so in one line.
```

From now on, bare `/loop` in this project runs *your* prompt. Project scope (`.claude/loop.md`) wins over user scope (`~/.claude/loop.md`), and edits take effect on the loop's next pass.

---
<br><br>

## 8: Inspect and Cancel the Loop
"Loop" is the command's name — but what `CronCreate` stored in step 6 is called a **scheduled task**, and that's the term to use when asking Claude about it. Scheduled tasks are **session-scoped**: they die with the conversation, restore on `claude --resume`, and expire after 7 days.

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

## 9: (OPTIONAL) Run the Goal Loop From a Plain Shell
Steps 6-8 were the **outer** loop — `/loop` re-running a prompt on a timer *inside* your session. This step goes back to the **inner** loop, `/goal`, and runs it with no session at all. `claude -p` is headless: it starts a session, works the goal to completion, prints one JSON result, and exits. Anything that can run a shell command — a script, a cron job, a build pipeline — can now run that loop.

**Action:** Exit Claude (*Ctrl+D*) and run in the terminal:
```bash
claude -p "/goal health.md exists and names the pass and fail counts from running python3 app/test_app.py" \
  --permission-mode acceptEdits --allowedTools "Bash(python3:*)" \
  --output-format json | jq '{result, num_turns, total_cost_usd}'
```
![headless goal](./images/ccadv28.png?raw=true "headless goal")

**Action:** After it completes, check what it produced:
```bash
cat health.md
```

The counts should match the suite on this branch. `health.md` is throwaway — delete it whenever.

> **What just happened.** One shell command ran the whole loop: Claude ran the suite, wrote the file, and the evaluator confirmed it — no prompt, no approval, nobody watching. `--output-format json` is what makes that *usable*: `num_turns` and `total_cost_usd` mean a script can log what a run cost, and a pipeline can fail a build on it.




---
<br><br>

## 10: Know the Bounds
Every loop needs a stop condition, and every unattended loop needs a budget. (Reading only)

- **Bound the goal** — a condition can carry its own limit: `…or stop after 20 turns`.
- **Bound the job** — `--max-turns` caps how far a headless run can go before it stops on its own.
- **`/loop`'s reach** — its tasks fire only while your session is open. Work that must outlive the session belongs on a scheduler that stays up without you — an OS cron job, or a scheduled task in the Claude cloud/desktop apps.

## Lab Summary
✅ You've used:
- `/goal` — an inner loop that works until a condition holds, judged by a separate evaluator model
- Reading the evaluator's verdicts, and writing a condition it can actually judge
- `/loop` — an outer loop on an interval, backed by `CronCreate` / `CronList` / `CronDelete`
- `loop.md` — replacing the built-in maintenance prompt with your own
- Running the same goal headless with `claude -p` and `--output-format json`
- Bounding a loop: stop clauses and `--max-turns`

<br><br>
---
## END OF LAB
---
<br><br>
# Lab 4: Agent SDK: Programmatic and Unattended Loops
## Lab Purpose
Run the **same Claude agent from a small Python program** — first read-only, then *unattended*, doing real work safely with nobody watching. 

> **Framing: the **Agent SDK** is like running `claude` but as a Python library. 

> We'll assemble some code using **diff-merge steps:** `code -d extra/<finished> sdk/<skeleton>` opens the finished file (**left**) beside your skeleton (**right**). Copy each highlighted block left → right (gutter arrow toward the right, or copy/paste) until nothing is highlighted, then **save the right file** (Cmd/Ctrl+S). A skeleton run before merging prints *"still the skeleton"* and stops — re-open the diff, merge what remains, save.

---
<br><br>

## 1: Install the Agent SDK (Skip if running in a Codespace.)
**Action:** In a terminal, run:
```bash
python -m pip install claude-agent-sdk
```

> Info: The SDK drives the bundled CLI, so it rides your existing CLI login here — the developer loop. *Shipping* is different: distributed products can't offer claude.ai login and authenticate with an `ANTHROPIC_API_KEY` (or Bedrock / Vertex / Foundry).

---
<br><br>

## 2: View the Starter Version of our Agent that uses the SDK.
**Action:** Open the skeleton:
```bash
code sdk/agent_loop.py
```

The imports name the pieces you'll use — `query`, `ClaudeAgentOptions`, `AssistantMessage`, `ResultMessage`. The body of `run_agent()` is a placeholder; you'll merge in the **options** (pre-approved tools plus a turn cap) and the **message loop**.

![skeleton view](./images/cc-se58.png?raw=true "skeleton view")

---
<br><br>

## 3: Diff, Merge, and Map It to the CLI
**Action:** Run the diff, merge the **one highlighted region** (the body of `run_agent()`), save the right file, and close the tab to save your changes:
```bash
code -d extra/agent_loop.txt sdk/agent_loop.py
```

Every piece maps to something you've already used:

| SDK piece (now in your file) | CLI equivalent you've used |
|---|---|
| `query(prompt=..., options=...)` | `claude -p "<prompt>"` (Lab 3) |
| `ClaudeAgentOptions(allowed_tools=[...])` | `--allowedTools "..."` (Lab 3) |
| `ClaudeAgentOptions(max_turns=...)` | `--max-turns` (Lab 3) |
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
You've *used* MCP servers; now **build one**. Complete a Python MCP server exposing three "project health" tools, register it at project scope, drive it from natural-language prompts, then connect a real remote server. Estimated time: 10-12 minutes.

> **MCP in one paragraph:** an MCP server is a process Claude Code talks to over stdin/stdout (or HTTP), exposing *tools* Claude can call. Add one with `claude mcp add <name> -- <command>`, inspect it with `/mcp`; its tools are named `mcp__<server>__<tool>`. Today the server is yours.

---
<br><br>

## 1: Complete the Server — Diff-Merge the Three Tools
The MCP SDK makes a server out of ordinary Python functions: decorate one with `@mcp.tool()` and its **docstring and type hints become the tool's documentation and input schema** — what Claude reads when choosing a tool.

> Older tutorials and blog posts show a `FastMCP` class — the SDK renamed it `MCPServer` in 2.0. The decorators below are identical either way.

Already in place in the skeleton: the `MCPServer("project-health")` instance (that name becomes the `mcp__project-health__...` prefix) and the `mcp.run()` call that starts the stdio transport. Missing are the three tools — `run_tests()` (runs `app/test_app.py`), `count_todos()` (TODO/FIXME counts per file), and `project_stats()` (file and line counts). That's your merge.

**Action:** Run the diff, merge the **one highlighted region** left → right, save the right file, and close the tab:
```bash
code -d extra/project_server.txt mcpserver/project_server.py
```

As you merge, read the docstrings — each tells Claude *when* to reach for that tool.

![diff merge server](./images/ccadv4.png?raw=true "diff merge server")

---
<br><br>

## 2: Start It Once by Hand
"Success" for a stdio server is **silence** — it's waiting for a client to speak JSON-RPC on stdin.

**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

Nothing appears — correct. (The skeleton message means the merge didn't save.) Stop it with `Ctrl+C` — the long `KeyboardInterrupt` traceback is expected, not a failure. From now on Claude Code starts and stops this process for you.

---
<br><br>

## 3: Register It at Project Scope
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

## 4: Health-Check the Connection
`claude mcp list` actually starts each server and reports whether it connects — your first diagnostic stop.

**Action:** Run:
```bash
claude mcp list
```

At project scope it shows **⏸ Pending approval (run `claude` to approve)** — project-scoped servers stay unapproved until you accept them in a session, next. On a connection *error*, run the server by hand (step 4) and read the message — with your own server, *you* are the maintainer.

![mcp list](./images/cc-se13.png?raw=true "mcp list")

---
<br><br>

## 5: Start Claude and Approve Your Server
Because `.mcp.json` can arrive in a repo from *anyone*, Claude Code asks before running project-scoped servers.

**Action:** Start Claude (*don't use* bypass mode here) and approve the server when prompted:
```bash
claude
```

![Approving the MCP server](./images/cc-se17.png?raw=true "Approving the MCP server")

---
<br><br>

## 6: Inspect It with /mcp
**Action:** Type:
```
/mcp
```

Select the **project-health** server and browse its three tools. Select one — the **Full name** (`mcp__project-health__run_tests`) and a **Description** that is your merged docstring, word for word: the entire basis on which Claude decides to reach for this tool. `Esc` back to the prompt.

![mcp panel](./images/ccadv5.png?raw=true "mcp panel")

---
<br><br>

## 7: Drive the Server: Run the Test Suite
**Action:** Type:
```
Use the project-health server to run the test suite and summarize what's failing and why.
```

Claude calls `mcp__project-health__run_tests`, gets your captured test output back, and explains the four contract violations — the ones `/triage` found in Lab 1, now through a tool you built.

![run tests tool](./images/ccadv6.png?raw=true "run tests tool")

---
<br><br>

## 8: Drive the Server: Full Health Report
**Action:** Type:
```
Using the project-health tools, give me a one-paragraph health report on this repo: test status, TODO count, and overall size.
```

You should see a line like **`Called project-health 2 times`**, then a synthesized report — *Ctrl+o* expands the transcript to watch the real `mcp__project-health__...` names go by.

> **Tie-back to Lab 2:** those full names are what a hook matcher targets — `"matcher": "mcp__project-health__.*"` governs *your own server's* tools the way it governed Edit/Write.

![health report](./images/ccadv7.png?raw=true "health report")

---
<br><br>

## 9: Get a GitHub Token
Your server needed no credentials — it's a local process you already trust. **Remote** servers are someone else's service over HTTPS, so they need authentication. GitHub publishes one, and everything else in this lab applies to it unchanged.

**Action:** While logged into GitHub, click the link below, enter a note, and click the green **Generate token** button at the bottom. The scopes are pre-selected for you.

Link: [Generate classic personal access token (repo & workflow scopes)](https://github.com/settings/tokens/new?scopes=repo,workflow)

![Creating token](./images/ccadv29.png?raw=true "Creating token")
![Creating token](./images/ccadv30.png?raw=true "Creating token")

On the next screen, **copy the generated token and save it** — you will not be able to see it again.

![Copying token](./images/ccadv31.png?raw=true "Copying token")

---
<br><br>

## 10: Register the Remote Server — Without Committing Your Token
Claude Code expands `${VAR}` in `.mcp.json` **when a session starts**, so the file can name a secret it never contains.

**Action:** Leave Claude with `/exit`. Then, in the terminal, export your token and register the server — note the **single** quotes:
```bash
export GITHUB_TOKEN=<paste-your-token>
claude mcp add --scope project --transport http \
  github https://api.githubcopilot.com/mcp/readonly \
  --header 'Authorization: Bearer ${GITHUB_TOKEN}'
```

Now look at what got written:
```bash
cat .mcp.json
```

You should see the literal text `${GITHUB_TOKEN}` — **not** your token. Double quotes would have let the shell expand it and baked your credentials into a file you're about to commit; single quotes left the placeholder for Claude Code to resolve at startup. Two characters decide whether this file is safe to share.

> **Order matters here.** The name and URL must come *before* `--header`; `--header` is repeatable, so if it appears first it swallows `github` and the URL as extra header values and the CLI reports `error: missing required argument 'name'`.

> Windows PowerShell: `$env:GITHUB_TOKEN = "<paste-your-token>"`. Whatever the shell, export the token **before** launching Claude — the expansion happens at session start, so a token exported in a different terminal won't be found.

---
<br><br>

## 11: Inspect the Remote Server
**Action:** Start Claude, approve the new server when prompted — the same gate you saw in step 5, now protecting you from someone else's service — then type:
```bash
claude
```
```
/mcp
```

Select **github** and browse. Two things to notice: it connects over HTTP rather than a local process, and where your server offered three tools, this one offers dozens. Every one of those tool definitions costs context in every session — which is why the URL above ends in `/readonly`, and why you remove servers you aren't using.

![github mcp panel](./images/ccadv32.png?raw=true "github mcp panel")

> Ask it something real — *"Use the github tools to summarize the open issues on this repo"* — and watch `mcp__github__...` names go by in the transcript, exactly like your own server's did.

---
<br><br>

## 12: Exit (and Optional Cleanup)

**Action:** Type `exit` to leave Claude. To remove the server registration afterwards:
```bash
claude mcp remove project-health
claude mcp remove github --scope project
```

(Leaving it is fine too — it's your repo's feature now.)

## Lab Summary
✅ In the capstone you've:
- Completed an MCP server: three `@mcp.tool()` functions whose docstrings are the tool documentation
- Learned the stdio contract (silence = waiting for a client)
- Registered it at project scope and read the shareable `.mcp.json`
- Approved and inspected it with `/mcp`
- Driven it from natural language, single- and multi-tool
- Connected GitHub's **remote** server with header auth, keeping the token out of the committed `.mcp.json`
- Connected the picture: commands → hooks → loops (`/goal`, `/loop`) → headless → SDK → your own MCP server

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
