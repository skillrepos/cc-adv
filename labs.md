# Advanced Claude Code: True AI Productivity
## Go beyond the basics — advanced delegation, hooks, loops, CI automation, the Agent SDK, and your own MCP server
## Session Labs
## Revision 1.18 - 08/24/26

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

**NOTE:** This course assumes you've completed the introductory Claude Code workshop (or equivalent). Steps that exercise something from that course are marked *(recap)* and kept quick.

<br><br>

---
<br><br>

# Lab 1: Advanced Delegation — Right Model, Right Context, Right Worker
## Lab Purpose
Climb the delegation ladder: a parameterized command, a hot-reloaded skill, a forked skill, a Haiku-pinned subagent, and finally a fully detached background agent you manage from the CLI.

---
<br><br>

## 1: Set Up in One Pass *(recap)*
The repo holds a Flask to-do API in `app/` (its test suite fails in 4 places *by design*), Agent SDK skeletons in `sdk/`, and an MCP server skeleton in `mcpserver/`. The intro course covered `/init`, CLAUDE.md and auto-memory in depth — here we just lay the context the rest of the day builds on.

**Action:** In the terminal, start Claude:
```bash
claude
```

> **First launch only:** Claude Code offers to **"Try the new fullscreen renderer?"**. Choose **2. Not now** — the classic renderer is what the screenshots in this lab show. (You can turn it on later with `/tui fullscreen`.)

Then type:
```
/init
```

![claude.md](./images/ccadv12.png?raw=true "claude.md")

When it finishes, skim the `CLAUDE.md` it wrote. It will already have worked out the repo layout, the test command, and the fact that `app/`'s four failing tests are deliberate — **that is the half of CLAUDE.md Claude can read for itself.**

Now add the half it cannot guess. Type:
```
Add this standing rule to CLAUDE.md: Never run git commit or git push in this repo - I handle version control myself. If you think something should be committed, say so and stop.
```

Confirm it landed under the standing rules. **That contrast is the point of this step:** `/init` documents what it can *discover*; a standing rule is where *your* policy goes — a preference no amount of reading the code would reveal. Lab 2 comes back to this exact rule to show how much a CLAUDE.md instruction is really worth.

> **From the intro course, still true:** shared+enforced rules → CLAUDE.md; personal learned facts → auto-memory (`/memory` shows the hierarchy). We won't walk it again.

![Add rule and memory](./images/ccadv14.png?raw=true "Add rule and memory")

---
<br><br>

## 2: Create a Real Custom Command
**Action:** In a separate terminal tab (keep Claude running), create the folders:
```bash
mkdir -p .claude/commands .claude/skills
```

**Action:** Create `.claude/commands/triage.md` (the `code` command works in the codespace) with these contents, and **save it**:

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

This file demonstrates four advanced features:

- **`$ARGUMENTS`** — text typed after `/triage`; positional `$1`, `$2`, ... also work.
- **`` !`git status --short` ``** — runs *when the command is invoked*; its output is injected into the prompt.
- **`@CLAUDE.md`** — pulls the file into context, same as an @ mention.
- **`allowed-tools`** — scopes what the command may do; note the fine-grained `Bash(git status:*)` syntax.

![Creating the triage command](./images/ccadv15.png?raw=true "Creating the triage command")

---
<br><br>

## 3: Run the Command on the Buggy API
**Action:** Claude Code loads custom commands at **startup**, so your running session doesn't know `/triage` yet (it would say *"Unknown command: /triage"*).

Restart Claude — type `/exit`, then `claude`. Then type:

```
/triage app/app.py
```

Git context and CLAUDE.md are injected automatically. The triage should flag the API returning **500** where the contract demands **400** (bad input) or **404** (missing item).

![Running the triage command](./images/ccadv2.png?raw=true "Running the triage command")

---
<br><br>

## 4: Turn the Command Into a Skill — Without Restarting
Custom commands have **merged into skills**: `.claude/commands/triage.md` and `.claude/skills/triage/SKILL.md` both create `/triage`, and the frontmatter means the same in both.

**Action:** In your other terminal tab (leave Claude running) enter the following:
```bash
mkdir -p .claude/skills/triage
mv .claude/commands/triage.md .claude/skills/triage/SKILL.md
```

**Action:** Now, go back to the terminal tab running Claude. **Without restarting Claude**, run `/triage` against a different file:
```
/triage app/datastore.py
```

It works: **Claude Code watches skill directories and picks up adds, edits and removals inside the current session.** Commands and agents do not.

> **If `/triage` isn't found**, restart Claude once — the watcher only follows directories that already existed at session start, which is why we created `.claude/skills` earlier.

---
<br><br>

## 5: Fork the Skill — Same Context, Separate Worker
Hot-reload means you can change *how* a skill executes mid-session too. `context: fork` runs the skill in its own **forked subagent**: it inherits your full conversation (and the warm prompt cache), but its work happens outside your main context.

**Action:** In your terminal tab, edit `.claude/skills/triage/SKILL.md` and add one line to the frontmatter:

```md
context: fork
```

**Action:** Back in Claude — still no restart — run it a third time:
```
/triage app/auth.py
```

Watch the transcript: the triage now runs as a delegated task and only the report returns. Your main conversation didn't absorb the file reads and git output — in step 11, `/context` will show the difference.

> **Read the wording carefully:** the transcript says *"Running in the background as @triage"*, then *"Agent … finished"*. "Background" here is the transcript's word for *delegated* — the result still lands back in **this** conversation, which is what makes it a fork. A true `background: true` skill would not come back at all.

> **The third execution dial:** `background: true` detaches the skill entirely — fire and keep typing. Fork = *same conversation, separate workspace*. Background = *separate everything, result arrives when ready*.

![Forked triage](./images/ccadv16.png?raw=true "Forked triage")

---
<br><br>

## 6: Delegate to a Cheaper Model — a Haiku Subagent
Verbose output stays in the subagent — only a summary returns — and `model:` pins it to a cheaper, faster model.

**Action:** In your terminal tab, create the agents folder:
```bash
mkdir -p .claude/agents
```

**Action:** Create `.claude/agents/test-scout.md` with these contents, and save:

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

---
<br><br>

## 7: Restart and Run the Subagent

**Action:** Switch back to Claude and restart to ensure the new agent is picked up, and then run it.

Restart — `/exit`, then `claude`. Then type:
```
Use the test-scout subagent to run the test suite and summarize the failures.
```

The subagent runs in the background and you get a compact report (10 passed / 4 failed with causes), run on Haiku, with the full test output kept out of your main context.

> **`model:` values:** an alias (`haiku`, `sonnet`, `opus`, `fable`), a full model string (`claude-haiku-4-5`), or `inherit` (the default). Same field in command frontmatter; `--model` for headless/CI; `ClaudeAgentOptions(model="haiku")` in the SDK (Lab 4). **Cheap scouts, smart supervisor.**

![Haiku test-scout subagent](./images/ccadv8.png?raw=true "Haiku test-scout subagent")

---
<br><br>

## 8: Two Dials of Thinking
The **effort level** is your session-wide dial; `ultrathink` anywhere in a prompt asks for deeper reasoning **on that turn only** — an in-context nudge that stacks on whatever effort is set. ("think", "think hard", "think more" are *not* keywords — just ordinary prompt text.)

**Action:** Type the following, then hit *Ctrl+o* while it runs to switch to the **detailed transcript** — every tool call, with timestamps and the model that served each turn (*Ctrl+o* again returns to the compact view):
```
ultrathink: Propose a refactoring plan for app/ that fixes the 400/404 contract violations without changing test_app.py. Consider at least two approaches and recommend one. Plan only - do not edit files.
```

**Action:** Now check the session dial. Type `/model` and use the **left/right arrow keys** to see the effort options — **low · medium · high · xhigh · max** — leave it on *medium* and hit *Esc*.

> **Also:** `/effort` sets it without the picker, and `/effort ultracode` is a Claude Code *setting*, not a model level — `xhigh` plus a dynamic multi-agent workflow. **Changing effort mid-session invalidates your prompt cache** (keyed by model *and* effort), so set both once, at the top of a session.

![Extended thinking](./images/ccadv3.png?raw=true "Extended thinking")

---
<br><br>

## 9: Send a Worker to the Background
Everything so far ran inside your session. `claude --bg` starts a **background agent**: a whole separate session, detached from any terminal, that keeps working while you do something else.

**Action:** In your **terminal tab** (leave your interactive session running — they coexist fine), run:
```bash
claude --bg "Run python3 app/test_app.py and write a markdown summary of the failures to bg_report.md - one line per failure naming the contract each violates" --permission-mode acceptEdits --allowedTools "Bash(python3:*)"
```

You get back a session ID and the management commands, immediately:

```
Starting background service…
backgrounded · b6cd8417
  claude agents             list sessions
  claude attach b6cd8417    open in this terminal
  claude logs b6cd8417      show recent output
  claude stop b6cd8417      stop this session
```

An unattended session has nobody to click "Yes" — so it must be told, up front, everything it is allowed to do.

> **Why two flags and not one.** Passing `--permission-mode` *replaces* auto mode; it does not add to it. `acceptEdits` pre-approves **file writes** and nothing else — so the very first thing this task does, running the test suite, is a **Bash** call that stops dead waiting for an approval nobody will ever give. `--allowedTools "Bash(python3:*)"` is what covers that call. **Mode governs edits; `--allowedTools` governs commands** — an unattended run usually needs both. (Try dropping the `--allowedTools` half later and watch `claude agents` report the session stuck on *"approve Bash: …"*.)

![Background agent started](./images/ccadv17.png?raw=true "Background agent started")

---
<br><br>

## 10: Manage the Fleet
**Action:** Still in the terminal tab, list your sessions:
```bash
claude agents
```

**Agent view** lists your **detached** sessions — the background worker is here; the interactive session you are typing in is not. Arrow to the background session to watch it; **Esc** leaves the view (Esc twice if you have landed in the "Describe a task" box).

Now go looking for the report the worker wrote:
```bash
cat bg_report.md
```

**It isn't there.** That is not a failure — it is the lesson:
```bash
cat .claude/worktrees/*/bg_report.md
```

There are your four failures. `claude --bg` **isolated the worker into its own git worktree** before letting it touch a file:
```bash
git worktree list
```
You'll see your repo on `main`, plus `.claude/worktrees/<random-name>` on a branch `worktree-<random-name>`.

> **Why worktrees are the answer to "what happens when two agents edit the same code?"** Each agent gets its own working copy of the repo on its own branch, so parallel editors never collide — you merge when you're ready. You can ask for one deliberately with `claude -w <name>` (`--worktree`), and a custom subagent with `isolation: worktree` in its frontmatter *always* edits in a disposable worktree, removed automatically if it finishes without changes.

> **Managing the fleet:** `claude logs <id>` shows recent output without attaching · `claude attach <id>` opens it here · `claude stop <id>` ends it · `claude rm <id>` removes the session **and** its worktree. A session left waiting on an approval holds its worktree **locked**, and plain `git worktree remove` will refuse it — `claude rm` is the clean way out.

> **Why this matters:** subagents die with your session; a background agent is a peer. This is the rung right below **agent teams** (peers that message each other — experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) and **dynamic workflows** (a script orchestrating dozens of agents — the `ultracode` keyword). Slides cover both; they're heavy for a shared classroom, so try them on your own account.

![Agent view](./images/ccadv18.png?raw=true "Agent view")

---
<br><br>

## 11: See What Your Context Costs *(recap)*
Everything you added in this lab rides along in every request.

**Action:** Back in your **interactive Claude session**, type:
```
/context
```

Find how much of the window is taken by each category: **System prompt**, **System tools**, **Custom agents**, **Memory files** (that's your `CLAUDE.md` plus auto-memory), **Skills**, and **Messages**. Note what the fork in step 5 kept *out* of Messages.

> **Companion:** `/usage` answers "what have I spent?" and breaks usage down **by attribution** — skills, subagents, plugins, each MCP server. Look for the `claude-haiku-4-5` line from step 7. Remember it in Lab 5.

![context usage](./images/ccode224.png?raw=true "context usage")

---
<br><br>

## 12: Exit

**Action:** In prep for the next lab and a fresh start, type `exit` to exit Claude Code.

```
exit
```

## Lab Summary
✅ You've climbed the delegation ladder:
- One-pass setup: CLAUDE.md + the standing test rule the whole day leans on
- Built `/triage` with `$ARGUMENTS`, inline bash context, `@file` references and scoped `allowed-tools`
- Converted it to a **skill** — hot-reloaded without a restart
- Forked it with `context: fork` — full conversation, separate workspace
- Delegated verbose test output to a `model: haiku` subagent
- Used `ultrathink` and the session effort dial
- Detached a worker entirely with `claude --bg` and managed it with `claude agents` / `logs` / `stop` / `rm`
- Learned why an unattended run needs a permission **mode** *and* an `--allowedTools` list
- Found the worker's output in its own **git worktree** — isolation you can see
- Audited what all of it costs with `/context` and `/usage`

> **The decision rule, in one breath:** **subagent** = delegated specialist inside your workflow · **fork** = keep noisy work out of your primary context · **background agent** = independent concurrent session · **worktree** = independent filesystem changes · **cheaper model** = match cost and intelligence to the task.

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 2: Hooks: Enforcing Policy at the Tool Boundary
## Lab Purpose
Create a PreToolUse hook that blocks edits to a protected file and a PostToolUse hook that logs every bash command, then watch both fire — even in auto and bypass-permissions modes.

---
<br><br>

## 1: Set Up the Protected File and Hooks Folder
We are working to implement this policy: nobody edits `config.json` — a stand-in for the credentials/config files every real project has.

**Action:** In a regular terminal (not Claude), create the file:
```
echo '{ "database": { "host": "localhost", "port": 5432 } }' > config.json
```

Then create the hooks folder:
```
mkdir -p .claude/hooks
```

---
<br><br>

## 2: Create the Guard Script
Claude Code sends the tool call details as JSON on the script's *stdin*. The script answers with an exit code: **0** = no objection, **2** = block it — and whatever it prints to *stderr* goes back to Claude as the reason.

**Action:** Create `.claude/hooks/protect-config.sh` (the `code` command works in the codespace) with these contents, and save it.

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

The `jq -r '.tool_input.file_path'` line pulls the target file path out of the JSON that arrives on stdin.

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
Hooks live under a `"hooks"` key in `.claude/settings.json`. Each entry names an *event* (PreToolUse, PostToolUse, etc.), a *matcher* filtering by tool name, and the *handler* to run.

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

- The matcher `Edit|Write` fires on either tool; `Bash` matches only the Bash tool.
- The guard uses the newer *exec form* (`args: []`), running the script directly with no shell — recommended with a path placeholder like `${CLAUDE_PROJECT_DIR}`. The logger omits `args` and so runs in *shell form*, which the `>>` redirect needs.

![The hooks settings file](./images/cc-se5.png?raw=true "The hooks settings file")

---
<br><br>

## 5: Start Claude in Bypass Mode
Hooks fire at the *tool boundary*, outside the permission system. Auto mode's classifier is a model making a judgment call; a hook is your code, and it keeps its veto even when every permission check is off.

**Action:** In a terminal other than your original one, start Claude with the option or alias (if working in the codespace):
```
claude --dangerously-skip-permissions

  or

claude-yolo (if running in the codespace)
```

> **You'll have to accept a warning.** Bypass mode opens with a red **"WARNING: Claude Code running in Bypass Permissions mode"** screen — choose **2. Yes, I accept**. The status line at the bottom then reads *bypass permissions on* instead of *auto mode on*.

---
<br><br>

## 6: Inspect the Hooks with /hooks
**Action:** Type:
```
/hooks
```

The first screen lists hook **events**, read-only. Yours are **PreToolUse (1)** and **PostToolUse (1)**; the rest (`PostToolUseFailure`, `PostToolBatch`, `PermissionDenied`, more if you scroll) are empty. Note the banner: this menu only *shows* hooks — to change one you edit `.claude/settings.json`.

![The /hooks menu](./images/cc-se6.png?raw=true "The /hooks menu")

Select **PreToolUse** to see how the event works — the exit-code legend, and your matcher listed as `[Project] Edit|Write  1 hook`. Drill in one more level to see the command itself: `[command] ${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-config.sh`, sourced from `Project Settings`.

![How the hook works](./images/cc-se8.png?raw=true "How the hook works")

Hit `Esc` several times to get back to the main Claude Code prompt.

---
<br><br>

## 7: Try to Edit the Protected File
**Action:** Type:
```
Add a connection_timeout setting to config.json using the Edit tool.
```

Claude attempts the edit; the tool call is **blocked** before it touches the file. The hook's stderr message surfaces in the conversation — Claude reads it too.

![Edit blocked by hook](./images/cc-se10.png?raw=true "Edit blocked by hook")

---
<br><br>

## 8: Look at How Claude Reacts
Exit code 2 also feeds the stderr text back to Claude; ours told it to suggest the change to the user instead.

**Action:** Read Claude's response. Then verify the file is untouched — in your **original (plain) terminal**, not this Claude session:
```bash
cat config.json
```

> **Why not `! cat config.json` here?** Claude Code auto-responds to in-session bash output, and in bypass mode it may *finish* the step 7 edit via the **Bash** tool, which our `Edit|Write` matcher doesn't block. A plain terminal keeps Claude out of the loop.

> **Spot the loophole:** the matcher only guards `Edit|Write`, so Claude could modify the file via Bash (`sed`, `echo >>`). Real policies add a Bash matcher too, or use the `if` field with permission-rule syntax. If Claude offers to work around the block, tell it no.

---
<br><br>

## 9: Generate Some Bash Traffic
PostToolUse fires *after* a tool call succeeds — it can't block, but it's ideal for auditing, logging and follow-ups like auto-formatting.

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

(While you type a path that matches real files, Claude Code shows a dim suggested-path line under the input. It's only a hint — *Enter* still submits.)

You should see each command Claude ran, with its description. Your own `!` commands are **not** in the list — they don't go through the Bash tool, so PostToolUse never fires for them. The log is Claude's activity, not yours.

![The bash command log](./images/cc-se11.png?raw=true "The bash command log")

---
<br><br>

## 11: Prompt vs. Tool vs. Hook Constraints
Four ways to say "don't do that," and they are not equally strong. (Reading only)

- **Prompt constraint** — CLAUDE.md or agent-file instructions: a request, not a guarantee. Your Lab 1 *"never run git commit or git push"* rule is exactly this: durable (unlike a boundary typed in chat, it survives `/compact`), but still only a request Claude can talk itself out of.
- **Tool constraint** — `disallowedTools` removes the tool entirely, for one agent.
- **Classifier** — in auto mode a second *model* judges each risky call: probabilistic, and a boundary stated in chat can be lost when `/compact` drops that message.
- **Hook** — your code at the tool boundary, on *every* tool call. Exit 2 is a hard no, even in bypass mode.

> **Going further:** a hook can exit 0 and print JSON for richer decisions (`permissionDecision: allow / deny / ask`), rewrite a tool's input, or inject context. Handler types beyond shell commands: `prompt`, `agent`, `http`, `mcp_tool`; many more events exist (`SessionStart` is popular). `"disableAllHooks": true` switches everything off. Full schema: [hooks reference](https://code.claude.com/docs/en/hooks).

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
Stop driving Claude one prompt at a time. Use `/goal` to keep a session working until a condition holds, `/loop` to re-run work on a schedule, and `claude -p` to run the same loop with no session at all — then read how GitHub Actions moves it off your machine entirely. Estimated time: 10-12 minutes.

**NOTE: Steps 1-8 run in an interactive Claude session. Step 9 runs in a regular terminal. Steps 10-11 are reading.**

> **Two kinds of loop, and this lab does both.** An **inner loop** works one task until the result is good enough — `/goal`. An **outer loop** re-runs a job on a schedule — `/loop`. Steps 9-11 are those same two loops with different drivers.

---
<br><br>

## 1: Work on a Throwaway Branch
`/goal` is about to change real files. A branch keeps those changes out of the way — Lab 5 still needs this project's tests to fail.

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
`/goal` sets a **completion condition**. After every turn a small fast model (Haiku) checks whether the condition holds. If it doesn't, Claude takes another turn on its own instead of handing control back to you.

**Action:** At the Claude prompt, type:
```
/goal python3 app/test_app.py reports 14 passed, 0 failed and exits 0. Never edit app/test_app.py - it defines the contract.
```

Setting the goal **starts a turn immediately** — you do not send a second prompt. Watch for the `◎ /goal active` indicator, and let it run.

![goal set](./images/ccadv19.png?raw=true "goal set")

> **This is Lab 1's plan, executed.** In Lab 1 you had Claude *plan* a fix for the 400/404 contract violations. Here it does the work and decides for itself when it's finished.

---
<br><br>

## 3: Watch the Evaluator's Verdicts
The evaluator returns one of three verdicts: **not yet met** (Claude keeps going, using the reason as guidance), **met** (the goal clears), or **impossible** (it clears and records why).

**Action:** Press *Ctrl+O* to expand the detailed transcript and read the **Reason:** line under the verdict.

> **Don't be surprised by a one-turn win.** On this task Claude usually fixes all four routes in a single turn, so you'll often see just `✓ Goal achieved (… · 1 turn · …)` with no *not yet met* rounds in between. The verdict and its reason are the thing to read — the number of rounds is whatever the work took.

![goal verdicts](./images/ccadv20.png?raw=true "goal verdicts")

> **The evaluator has no tools.** It only judges what Claude has already put in the conversation. That's why the condition names a command whose output lands in the transcript — "the code is clean" would be unjudgeable.

---
<br><br>

## 4: Check Goal Status
**Action:** When the run settles, type `/goal` with no arguments:
```
/goal
```

You get the verdict, the condition, how long it ran, turns evaluated, and token spend. (The evaluator's *reason* isn't on this card — that's the `Ctrl+O` view from step 3.)

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

`python3 app/test_app.py` should report `10 passed, 4 failed` again — Lab 5 needs those failures. The fix is still on `loop-lab` if you want to look at it later.

---
<br><br>

## 6: Schedule a Repeating Prompt with `/loop`
That was the inner loop. `/loop` is the outer one: it re-runs a prompt on an interval for as long as the session stays open.

**Action:** Back in the Claude session, type:
```
/loop 2m append the current UTC time and the current test pass/fail counts as one line in beat.md
```

Claude converts the interval to a cron expression and calls the `CronCreate` tool. You'll see a confirmation naming the cadence and an 8-character job ID:

```
● CronCreate(*/2 * * * * : append the current UTC time…)
  ⎿  Scheduled 8db547d2 (Every 2 minutes)
```

![loop scheduled](./images/ccadv22.png?raw=true "loop scheduled")

> **Leave it running and move to step 7 while it ticks.** Supported units are `s`, `m`, `h`, `d`. Seconds round up to a minute — cron has one-minute granularity. Fire times carry a deterministic jitter, so an interval job can land up to half its interval late.

---
<br><br>

## 7: Give Bare `/loop` a Default Prompt
`/loop` with **no prompt** runs a built-in maintenance prompt — continue unfinished work, tend the branch's PR, then cleanup passes. A `loop.md` file replaces that default with your own.

**Action:** Create `.claude/loop.md` with these contents, and save:

```markdown
Run python3 app/test_app.py. If anything fails, report the failing test
names and the contract each one violates - do not fix them.
If everything passes, say so in one line.
```

Now a bare `/loop` in this project runs *that* instead of the built-in prompt. Project scope (`.claude/loop.md`) wins over user scope (`~/.claude/loop.md`), and edits take effect on the next iteration — you can refine the instructions while a loop is running.

---
<br><br>

## 8: Inspect and Cancel the Loop
Scheduled tasks are **session-scoped**: they die with the conversation, restore on `claude --resume`, and expire after 7 days.

**Action:** Check that the loop has fired at least once — the `!` prefix runs it as a shell command instead of sending it to Claude:
```
! cat beat.md
```

Then ask for the task list and cancel it in plain English:
```
what scheduled tasks do I have? cancel the beat.md one
```

Claude uses `CronList` and `CronDelete` under the hood. (*Esc* while a loop is waiting also clears the pending wakeup.)

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

`-p` works, prints, and exits. `--output-format json` wraps the answer with `session_id`, `num_turns` and `total_cost_usd` — every run scriptable and auditable. Expect roughly **3 turns and a few cents**.

![headless goal](./images/ccadv24.png?raw=true "headless goal")

> **`-p` has no human to click "Yes."** Interactive sessions start in auto mode on Pro/Max/Team, but `claude -p` and the Agent SDK still start in `default` — so anything unattended must pre-approve its permissions with `--permission-mode` **and** `--allowedTools`. Nothing about the August 2026 auto-mode default changes that.

> **What a half-permissioned loop actually does — worth knowing before you ship one.** Drop the `--allowedTools` and this same command cannot run the test suite: `acceptEdits` covers writes, not Bash. It does **not** fail loudly. The goal stays unmet, so Claude keeps trying — and eventually satisfies the *wording* of the condition by **reading the source** and reasoning out what the counts must be, writing a confident, wrong `12 passed, 4 failed` into `beat.md`. Measured side by side: **9 turns and ~$0.41 for a fabricated answer, against 3 turns and ~$0.05 for a real one.** An autonomous loop denied the tool it needs doesn't stop — it improvises. Bound what it may do, then check what it actually ran.

---
<br><br>

## 10: The Same Engine on GitHub's Runners
Moving the loop onto someone else's machine: `claude-code-action@v1` runs this exact engine in CI. (Reading only — the workshop repo isn't yours to wire up, so this is your reference; step 11 ends with how to try it for real.)

**The responder.** With **no `prompt:`**, the action auto-detects *interactive mode*: a teammate comments `@claude fix the TypeError` on a PR or issue, and Claude answers on GitHub's runners:

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

**The outer loop in CI.** With a **`prompt:`**, it auto-detects *automation mode* and runs immediately on the trigger — and a `schedule:` trigger makes it the same outer loop as `/loop`, on infrastructure that doesn't need your laptop open:

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

`claude_args` is a passthrough to the same CLI flags you used in step 9 — nothing new to learn:

| In claude_args | You used it as |
|---|---|
| `--max-turns 5` | the turn cap (also `max_turns` in Lab 4's SDK) |
| `--allowedTools "Read,Edit,Bash"` | pre-approving an unattended run |
| `--model sonnet` | `/model` |
| `--append-system-prompt "..."` | custom instructions per workflow |

---
<br><br>

## 11: Know the Bounds
Every loop needs a stop condition, and every unattended loop needs a budget. (Reading only)

- **Bound the goal.** A condition can carry its own limit — `…or stop after 20 turns`. Without one, only the evaluator ends the run.
- **Bound the job.** `--max-turns` in `claude_args` plus a workflow-level `timeout-minutes`.
- **Where `/loop` stops reaching.** Its tasks fire only while the session is open and idle. To outlive a session, use cloud Routines, a Desktop scheduled task, or a `schedule:` trigger.
- **CI security baseline.** The key comes only from `${{ secrets.ANTHROPIC_API_KEY }}`; the GitHub App needs Contents, Issues and Pull requests and nothing more; review Claude's PRs like any contributor's.

> **Try it live later:** in a repo you own, run `claude` and type `/install-github-app` — it installs the app and adds the `ANTHROPIC_API_KEY` secret. Commit `claude.yml`, open an issue, and comment `@claude suggest an improvement to the README`. (The workshop repo isn't yours, so this is homework.)

## Lab Summary
✅ You've mastered:
- `/goal` — an inner loop that works until a condition holds, judged by a separate evaluator model
- Reading the evaluator's verdicts, and writing a condition it can actually judge
- `/loop` — an outer loop on an interval, backed by `CronCreate` / `CronList` / `CronDelete`
- `loop.md` — replacing the built-in maintenance prompt with your own
- Running the same goal headless with `claude -p` and `--output-format json`
- How `claude-code-action@v1` runs the same engine in CI — an `@claude` responder and a scheduled outer loop (reference)
- Bounding a loop: stop clauses, `--max-turns`, `timeout-minutes`

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 4: Agent SDK: Programmatic and Unattended Loops
## Lab Purpose
Run the **same Claude agent from a small Python program** — first read-only, then *unattended*, doing real work safely with nobody watching. Estimated time: 10-12 minutes.

> **In one line:** the `claude` command is a finished app; the **Agent SDK** is that same engine as a Python library. `query()` does what `claude -p "..."` did in Lab 3, and you set permissions *in code* — which is what lets it run safely with nobody there to click "approve."

> **How the merge steps work.** A few steps use a **diff-merge**. You open a *skeleton* — a working file with its key lines replaced by a placeholder — next to the *finished* version, and copy the finished lines in:
> - Run `code -d extra/<finished> sdk/<skeleton>` to open the two files **side by side**, differences highlighted. The finished file (`extra/…`) is on the **left**; your skeleton (`sdk/…`) is on the **right**.
> - Copy the **left** side (finished) onto the **right** side (skeleton): click the gutter arrow pointing **toward your skeleton on the right** to move a highlighted block across, or select the left side, copy, and paste over the right.
> - When **nothing is highlighted**, the files match. **Save the right file** — the skeleton (Cmd/Ctrl+S).
>
> Each skeleton prints a *"still the skeleton"* message and stops if you run it before merging — that's the file telling you the merge or the save didn't fully land. Re-open the diff, make sure no highlight remains, and save.

---
<br><br>

## 1: Install the Agent SDK (You can skip this step if running in a Codespace.)
The SDK drives the bundled CLI under the hood, so your existing login carries over.

**Action:** In a terminal, run:
```bash
python3 -m pip install claude-agent-sdk
```

> **`pip: command not found`?** Use the `python3 -m pip …` form above rather than a bare `pip`.

> **Whose login is this?** On your own machine — or this codespace — the SDK rides your existing CLI login: the developer loop, and exactly how this lab runs. *Shipping* is different: Anthropic doesn't allow third-party products to offer claude.ai login, so anything you distribute authenticates with an `ANTHROPIC_API_KEY` in the process environment (or Bedrock / Vertex / Foundry) — the same secret Lab 3's CI workflows used.

---
<br><br>

## 2: View the Skeleton
**Action:** Open the skeleton:
```bash
code sdk/agent_loop.py
```

The `import` block already names the SDK pieces you'll use — `query`, `ClaudeAgentOptions`, `AssistantMessage`, `ResultMessage`. The body of `run_agent()` is a placeholder and a `raise` that stops the program until you merge. You'll add the **options** (pre-approved tools plus a turn cap) and the **message loop**.

![skeleton view](./images/cc-se58.png?raw=true "skeleton view")

---
<br><br>

## 3: Diff, Merge, and Map It to the CLI
**Action:** Run:
```bash
code -d extra/agent_loop.txt sdk/agent_loop.py
```

The finished file (`extra/agent_loop.txt`) is on the **left**; your skeleton (`sdk/agent_loop.py`) is on the **right**. You'll see **one highlighted region** — the body of `run_agent()`. Copy the entire **left** side over the **right** (gutter arrow toward the right, or select-copy-paste) so nothing stays highlighted, then **save the right file** — the skeleton (Cmd/Ctrl+S) — and close the diff tab.

> **If the next step still says "still the skeleton":** a line didn't merge or the file wasn't saved. Re-open the diff, confirm **no** highlight remains, then save again.

Every piece of the merged `run_agent()` maps to something you've already used:

| SDK piece (now in your file) | CLI equivalent you've used |
|---|---|
| `query(prompt=..., options=...)` | `claude -p "<prompt>"` (Lab 3) |
| `ClaudeAgentOptions(allowed_tools=[...])` | `--allowedTools "..."` (Lab 3) |
| `ClaudeAgentOptions(max_turns=...)` | `--max-turns` / `claude_args` (Lab 3) |
| iterating `AssistantMessage` / `ToolUseBlock` / `ResultMessage` | `--output-format stream-json` events |

`query()` returns an async iterator; your `async for` loop prints `[claude]` lines for text and `[tool]` lines for each call (a `ToolUseBlock` carrying the tool's `name` and `input`), ending with a `ResultMessage` of stats.

![diff merge](./images/cc-se59.png?raw=true "diff merge")

---
<br><br>

## 4: Run Your Agent
**Action:** Run:
```bash
python3 sdk/agent_loop.py "What files are in the sdk directory? Answer in one sentence."
```

You'll see `[claude]` lines and likely one or more `[tool]` lines, then the `ResultMessage` stats: turns used, duration, final result.

> **`allowed_tools` is not an exhaustive whitelist.** You will often see a `[tool] Bash` line here even though `Bash` isn't in the list — Claude Code ships a built-in set of read-only commands (`ls`, `cat`, `git status`, ...) that never need approval. `allowed_tools` governs the calls that would otherwise stop and ask, which is exactly what step 5 shows with `Write`.

![sdk run](./images/cc-se60.png?raw=true "sdk run")

---
<br><br>

## 5: Force Multiple Turns, Then Try to Write
**Action:** Run a prompt that forces tool use:
```bash
python3 sdk/agent_loop.py "Find every TODO comment in the .py files under sdk/ and mcpserver/ and list them"
```
Watch the `[tool]` lines: the agent calls a read-only tool (`Grep`, usually more than once), gets results back, and only then answers. Each `[tool]` line is one trip around the loop; **Turns used** counts those trips.

![sdk run](./images/cc-se61.png?raw=true "sdk run")

Now try to make it write:
```bash
python3 sdk/agent_loop.py "Create a file named sdk_test.txt containing hello"
```
The write isn't blocked — it just isn't *pre-approved*, so with no human attached it can't proceed. Confirm nothing was created: `ls sdk_test.txt`.

![sdk run](./images/cc-se62.png?raw=true "sdk run")

---
<br><br>

## 6: View the Unattended Skeleton and How It Gates Every Tool
In the CLI an undecided tool call means *ask the human*. Unattended there is no human, so your code must decide — and must see **every** call.

**Action:** Open it:
```bash
code sdk/auto_agent.py
```
The gate is a **PreToolUse hook** — `gatekeeper()` — run by the CLI *before* each tool executes, returning a `permissionDecision` of `"allow"` or `"deny"`. Lab 2's idea, in Python, inside your own program.

![skeleton view](./images/cc-se70.png?raw=true "skeleton view")

> **Note:** SDK sessions start in `default` mode whatever your interactive CLI default is — the auto-mode default does not extend to programs you write. Permissions in code are not optional here.

> **What the SDK *does* pick up from disk.** By default, the same filesystem configuration the CLI reads: user, project and local settings, `CLAUDE.md`, and the skills, agents and commands in `.claude/` (omitting `setting_sources` equals `setting_sources=["user", "project", "local"]`). So your Lab 2 hook is still armed — it loads here and fires alongside the Python `gatekeeper()`. For an isolated agent, `setting_sources=[]` limits it to what you configure in code; Anthropic recommends that for multi-tenant deployments, since managed policy, `~/.claude.json` and auto-memory are read regardless.

> **Why a hook, and not `can_use_tool`?** `ClaudeAgentOptions` accepts a `can_use_tool` callback, but the CLI calls it only for tools that resolve to **"ask"** — it is skipped for anything already permitted by `allowed_tools`, `permission_mode` or your settings, so a destructive command in an environment that trusts `Bash` sails past it. A **PreToolUse hook fires on every call, no exceptions.**

The skeleton also provides a `prompt_stream()` generator: streaming the prompt is what lets the hook run interactively as the agent works.

---
<br><br>

## 7: Diff and Merge the Unattended Agent
**Action:** Run the diff below. The finished file (`extra/auto_agent.txt`) is on the **left**; your skeleton (`sdk/auto_agent.py`) is on the **right**. This time there are **two highlighted regions** — the `gatekeeper()` body and the `main()` body. Merge **both** from the left into the right, **save the right file** (the skeleton), and close:
```bash
code -d extra/auto_agent.txt sdk/auto_agent.py
```

![diff merge auto](./images/cc-se71.png?raw=true "diff merge auto")

---
<br><br>

## 8: Run It Unattended and Inspect the Output
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

## 9: Trigger the Deny Path
**Action:** In `sdk/auto_agent.py`, replace the **whole** `TASK = ( … )` block — all three lines, through the closing `)` — with this single line:
```python
TASK = "Use a Bash rm command to delete agent_report.md. Then say DONE."
```
(Replacing only the first line leaves the old string fragments behind and Python stops with an `IndentationError`.)

**Save your changes.** Run it again (`python3 sdk/auto_agent.py`). The PreToolUse hook sees the `Bash` call **before** it runs and returns `deny`, so the `rm` never executes. Watch for the deny line:
```
  [gatekeeper] DENIED: Bash -> 'rm -f agent_report.md'
```
(The exact command varies — `rm`, `rm -f`, whatever Claude reaches for. The hook matches on the tool, not the spelling.) Claude will usually explain that it couldn't delete the file, and it still says `DONE` because the task told it to — so **the `Result:` line proves nothing either way**. The proof is the deny line *and* the file still being there:
```bash
ls agent_report.md
```
It should still exist.

![gatekeeper run](./images/cc-se74.png?raw=true "gatekeeper run")

(Optional) If you want, you can change the TASK string back to the original one.

---
<br><br>

## 10: Connect It Back to the CLI — and Peek at What's Next
The CLI, the SDK and Lab 3's GitHub Action all run this same loop.

**Action:** Run the read-only program's CLI equivalent and compare:
```bash
claude -p "What files are in the sdk directory? Answer in one sentence." --output-format json | jq '{result: .result, num_turns: .num_turns, duration_ms: .duration_ms}'
```
The JSON fields mirror the `ResultMessage` attributes your program printed. Same loop, different driver.

> **Going further — memory across runs:** Lab 1's **auto-memory** (`~/.claude/projects/<project>/memory/`) loads into the SDK's system prompt at session start, so tomorrow's `auto_agent.py` run can pick up what yesterday's discovered. Catch: it records memories with the ordinary `Write` and `Edit` tools, so if `allowed_tools` omits `Write` it silently can't save. Auto-memory loads regardless of `setting_sources`; disable with `autoMemoryEnabled: false` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. See the [Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/overview).

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

> **Quick MCP recap (from the intro course):** an MCP server is a process Claude Code talks to over stdin/stdout (or HTTP), exposing *tools* Claude can call. Add one with `claude mcp add <name> -- <command>`, inspect it with `/mcp`; its tools are named `mcp__<server>__<tool>`. Today the server is yours.

---
<br><br>

## 1: Tour the Server Skeleton
FastMCP makes a server out of ordinary Python functions: decorate one with `@mcp.tool()` and its **docstring and type hints become the tool's documentation and input schema** — what Claude reads when choosing a tool.

**Action:** Open the skeleton:
```bash
code mcpserver/project_server.py
```

Already in place: the `FastMCP("project-health")` instance (that name becomes the `mcp__project-health__...` prefix), the `ROOT` path resolution, and the `mcp.run()` call that starts the stdio transport. The three tools are missing — that's your merge.

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
The diff is exactly the three `@mcp.tool()` functions:

- `run_tests()` — runs `app/test_app.py` and returns the PASS/FAIL output plus exit code
- `count_todos()` — counts TODO/FIXME comments per source file
- `project_stats()` — file and line counts by file type

**Action:** Run:
```bash
code -d extra/project_server.txt mcpserver/project_server.py
```

The finished file is on the **left**; your skeleton is on the **right**. There is **one highlighted region** — copy left over right so nothing remains highlighted, **save the right file** (Cmd/Ctrl+S), and close the diff tab.

As you merge, read the docstrings — each tells Claude *when* to reach for that tool ("Use this to find out whether the to-do API currently meets its contract...").

![diff merge server](./images/ccadv4.png?raw=true "diff merge server")

---
<br><br>

## 4: Start It Once by Hand
"Success" for a stdio server is **silence**: it waits for a client to speak JSON-RPC on stdin — no banner, no output.

**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

Nothing appears — correct. (If you see the skeleton message, the merge didn't save.) Stop it with `Ctrl+C`: a stdio server has no shutdown handler, so Python prints a long `KeyboardInterrupt` traceback on its way out — that's expected, not a failure. From now on Claude Code starts and stops this process for you.

---
<br><br>

## 5: Register It at Project Scope
Project scope writes the config to `.mcp.json` in the repo root — commit it and everyone who clones the project gets your server. (The `--` separates Claude's options from the server's command line.)

**Action:** Run:
```bash
claude mcp add project-health --scope project -- python3 mcpserver/project_server.py
```

Then look at the shareable artifact that just appeared:
```bash
cat .mcp.json
```

You'll see the server entry with its `command` and `args` — plain JSON, no secrets.

![mcp json](./images/cc-se16.png?raw=true "mcp json")

---
<br><br>

## 6: Health-Check the Connection
`claude mcp list` actually starts each server and reports whether it connects — your first diagnostic stop.

**Action:** Run:
```bash
claude mcp list
```

At **project scope** (`.mcp.json`) it shows as **⏸ Pending approval (run `claude` to approve)** — project-scoped servers stay unapproved until you accept them in a session, which you'll do next. (At *local* scope you'd see **✓ Connected**.) If you see a connection *error*, run the server by hand (step 4) and read the message — with your own server, *you* are the maintainer.

![mcp list](./images/cc-se13.png?raw=true "mcp list")

---
<br><br>

## 7: Start Claude and Approve Your Server
Because `.mcp.json` can arrive in a repo from *anyone*, Claude Code asks you to approve project-scoped servers before it will run them.

**Action:** Start Claude (*don't use* bypass mode here):
```bash
claude
```

When prompted to use/approve the MCP server(s) from `.mcp.json`, approve them.

![Approving the MCP server](./images/cc-se17.png?raw=true "Approving the MCP server")

---
<br><br>

## 8: Inspect It with /mcp
**Action:** Type:
```
/mcp
```

Hit *Enter*, select the **project-health** server and browse its three tools. Select one — it shows the **Full name** (`mcp__project-health__run_tests`) and a **Description** that is the docstring you merged in step 3, word for word. That docstring is the entire basis on which Claude decides to reach for this tool.

![mcp panel](./images/ccadv5.png?raw=true "mcp panel")

Use `Esc` to get back to the main prompt.

---
<br><br>

## 9: Drive the Server: Run the Test Suite
**Action:** Type:
```
Use the project-health server to run the test suite and summarize what's failing and why.
```

(In **manual** mode, approve the tool use.) Claude calls `mcp__project-health__run_tests`, gets your captured test output back, and explains the four contract violations — the ones `/triage` found in Lab 1, now through a tool you built.

![run tests tool](./images/ccadv6.png?raw=true "run tests tool")

---
<br><br>

## 10: Drive the Server: Full Health Report
**Action:** Type:
```
Using the project-health tools, give me a one-paragraph health report on this repo: test status, TODO count, and overall size.
```

You should see a line like **`Called project-health 2 times`**, then a synthesized report. The transcript collapses tool calls by default — press *Ctrl+o* to expand it and watch the real `mcp__project-health__...` names go by.

> **Tie-back to Lab 2:** those full tool names are what a hook matcher targets — `"matcher": "mcp__project-health__.*"` lets a PreToolUse hook govern *your own server's* tools the way it governed Edit/Write.

![health report](./images/ccadv7.png?raw=true "health report")

---
<br><br>

## 11: Where to Take It
Everything beyond this is more of the same pattern. (Reading only)

- **More tools:** anything a Python function can do — query a database, call an internal API, read a wiki — becomes a tool with one decorator and a good docstring.
- **Arguments:** add typed parameters (`def run_tests(pattern: str) -> str:`); FastMCP builds the input schema.
- **Beyond stdio:** the same code can serve HTTP (`claude mcp add --transport http <url>`).
- **Distribution:** `.mcp.json` in the repo (done!), or package it with a plugin for one-command team install.

---
<br><br>

## 12: Exit (and Optional Cleanup)

**Action:** Type `exit` to leave Claude. If you want to remove the server registration afterwards:
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
