# Advanced Claude Code: True AI Productivity
## Go beyond the basics — custom commands, hooks, CI automation, the Agent SDK, and your own MCP server
## Session Labs
## Revision 1.4 - 07/22/26

<br><br>

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**Copy and paste may not work as expected if using the mouse. If not, use the keyboard shortcuts - *Ctrl+C/Cmd+C and Ctrl+V/Cmd+V*.**

**If you haven't done so already, set your model to `Sonnet` instead of `Opus`.**

> In Claude Code at the prompt, type:
> ```
> /model
> ```
> In the list that comes up, type "2" or use the arrow keys to move the pointer to "2" and hit *Enter*. Also use the left/right arrow keys to set the thinking mode to *medium*.
>
> ![set model](./images/ccode209.png?raw=true "set model")
>
> You should see an indicator that the model was set to a *Sonnet* model (e.g., *claude-sonnet-4-6* or later — the exact version shown may be newer). Note: your `/model` selection is saved as the default for new sessions; press `s` in the model list to set it for the current session only.
>
<br><br>

**NOTE:** This course assumes you've completed the introductory Claude Code workshop (or equivalent). Where a step exercises something from that course, it's marked *(recap)* and kept quick. Throughout the labs, you can use the `claude --dangerously-skip-permissions` mode (alias `claude-yolo` in the codespace) where a lab says it's OK, to avoid responding to most permission prompts.

<br><br>

---
<br><br>

# Lab 1: Advanced Context, Custom Commands & Extended Thinking
## Lab Purpose
Set up rich project context on a real codebase, build a production-grade custom slash command that combines arguments, frontmatter, live git context, and file references, delegate verbose work to a low-cost Haiku subagent, and use extended thinking for a hard planning task. Estimated time: 10-12 minutes.

---
<br><br>

## 1: Start Claude and Scout the Codebase *(recap)*
**What we're doing:** Starting a session and getting oriented in the workshop repo.
**Why:** This repo has real material to work on: a small Flask to-do API in `app/` (whose test suite fails in 4 places *by design*), Agent SDK skeletons in `sdk/`, and an MCP server skeleton in `mcpserver/`. Every lab today builds on it.

**Action:** In the terminal, start Claude:
```bash
claude
```

Then type:
```
Give me a one-paragraph overview of this repo: what's in app/, sdk/, and mcpserver/, and how do I run the tests?
```

Claude will scan the project and orient you — the "explore before you edit" habit from the intro course.

---
<br><br>

## 2: Generate the Project Context File *(recap)*
**What we're doing:** Creating a CLAUDE.md for this project.
**Why:** CLAUDE.md is read at the start of every session — it's where project knowledge lives. In the intro course you ran this on a toy project; here it maps a multi-directory codebase.

**Action:** Type:
```
/init
```

When it finishes, open the generated `CLAUDE.md` (you can use the `code` command in the codespace) and skim it. Note that it found the test suite and the directory layout on its own.

![claude.md](./images/ccode226.png?raw=true "claude.md")

---
<br><br>

## 3: Add a Standing Rule — and a Persistent Memory *(recap)*
**What we're doing:** Persisting one fact two ways: a shared project rule in CLAUDE.md, and a personal memory in Claude's auto-memory file.
**Why:** There's a rule today's automation labs depend on: the test file defines the *contract* and must never be edited. That belongs in CLAUDE.md — committed, seen by every session, teammate, and CI run. Claude also keeps *auto-memory* (a MEMORY.md per project, per user): ask it to **remember** something and it saves the fact there for future sessions.

**Action:** First, the shared rule. Type:
```
Add this standing rule to CLAUDE.md: The test suite is run with python3 app/test_app.py. Never edit app/test_app.py - it defines the correct contract.
```

Approve the edit and confirm the rule landed in `CLAUDE.md`.

**Action:** Now a personal memory. Type:
```
Remember that when I ask for code reviews in this repo, I want short, test-first explanations.
```

Watch for the saved-memory confirmation. Verify where it went (in the codespace):
```
! cat ~/.claude/projects/-workspaces-cc-adv/memory/MEMORY.md
```
(Running locally? The directory under `~/.claude/projects/` is named after your repo path.)

> **Rule of thumb:** *enforced and shared* → CLAUDE.md (in the repo). *Personal and learned* → auto-memory (per user, per machine; the first ~200 lines load each session). You'll also see Claude add memories on its own as it works.

![Add rule and memory](./images/ccadv9.png?raw=true "Add rule and memory")

---
<br><br>

## 4: Check the Memory Hierarchy *(recap)*
**What we're doing:** Viewing how context is layered.
**Why:** Enterprise → user → project — knowing *where* a rule lives tells you who it applies to. Advanced teams standardize this deliberately.

**Action:** Type:
```
/memory
```

Find the project-level CLAUDE.md you just updated and the auto-memory entry holding your "remember" fact (note its on/off toggle) — this is also where you'd spot an enterprise- or user-level file overriding project rules. Hit *Esc* to exit the view.

![memory hierarchy](./images/ccode228.png?raw=true "memory hierarchy")

---
<br><br>

## 5: Create a Real Custom Command
**What we're doing:** Building `/triage` — a custom slash command with frontmatter, an argument, inline bash context, and a file reference.
**Why:** In the intro course your commands were static prompt templates. Production commands are parameterized and *self-loading*: they pull in live context (git state, project rules) so the prompt is always current.

**Action:** In a terminal tab (keep Claude running), create the commands folder:
```bash
mkdir -p .claude/commands
```

**Action:** Make a new file `.claude/commands/triage.md` (remember you can use the `code` command in the codespace) and copy/paste the following contents into it, then save:

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

Four advanced features in one file:

- **`$ARGUMENTS`** — whatever you type after `/triage` lands here (there are also positional `$1`, `$2`, ... if you want separate parameters).
- **`` !`git status --short` ``** — the backtick-bash runs *when the command is invoked* and its output is injected into the prompt.
- **`@CLAUDE.md`** — pulls the file's contents into context, same as an @ mention.
- **`allowed-tools`** — scopes what the command may do; note the fine-grained `Bash(git status:*)` rule syntax.

![Creating the triage command](./images/ccadv1.png?raw=true "Creating the triage command")

---
<br><br>

## 6: Run the Command on the Buggy API
**What we're doing:** Triaging `app/app.py` — the file with the four planted contract violations.
**Why:** To see a parameterized command earn its keep on real code.

**Action:** Back in Claude, type:
```
/triage app/app.py
```

Watch the output: the git context and CLAUDE.md were injected automatically, and the triage should call out the API's habit of returning **500** where the contract demands **400** (bad input) or **404** (missing item) — the exact failures in the test suite. Keep this in mind; automation will meet these bugs again in Labs 3-5.

![Running the triage command](./images/ccadv2.png?raw=true "Running the triage command")

---
<br><br>

## 7: Delegate to a Cheaper Model — a Haiku Subagent
**What we're doing:** Creating a subagent pinned to a low-cost model and delegating verbose work to it.
**Why:** Two levers at once. *Context isolation:* verbose output (test runs, logs) stays in the subagent — only a summary returns to your session. *Cost:* the `model:` frontmatter pins the subagent to a cheaper, faster model — Haiku is ideal for simple, high-volume work, while your main session stays on Sonnet for decisions.

**Action:** In your terminal tab, create the agents folder:
```bash
mkdir -p .claude/agents
```

**Action:** Make a new file `.claude/agents/test-scout.md`, copy/paste the following contents into it, and save:

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

**Action:** Back in Claude, type:
```
Use the test-scout subagent to run the test suite and summarize the failures.
```

Approve as needed. You should get back a compact report (10 passed / 4 failed with one-line causes) — the full test output never entered your main context, and the run happened on Haiku.

> **The `model:` values:** an alias (`haiku`, `sonnet`, `opus`, `fable`), a full model string (e.g. `claude-haiku-4-5`), or `inherit` (the default — use the main session's model). The same field works in command frontmatter, `--model` works for headless/CI runs, and `ClaudeAgentOptions(model="haiku")` does it in the Agent SDK (Lab 4). The pattern: **cheap scouts, smart supervisor.**

![Haiku test-scout subagent](./images/ccadv8.png?raw=true "Haiku test-scout subagent")

---
<br><br>

## 8: Use Extended Thinking for a Planning Task
**What we're doing:** Asking for a refactor plan with the maximum thinking budget.
**Why:** For multi-step reasoning — architecture, refactors, tricky bugs — you can grant Claude a bigger thinking budget. The main control is the thinking-effort setting in `/model`; starting a prompt with `ultrathink` requests the maximum budget for that one prompt.

**Action:** Type the following, then hit *Ctrl+o* while it runs to watch the thinking stream:
```
ultrathink: Propose a refactoring plan for app/ that fixes the 400/404 contract violations without changing test_app.py. Consider at least two approaches and recommend one. Plan only - do not edit files.
```

Notice in the thinking output how Claude weighs the alternatives *before* answering — that deliberation is what the bigger budget buys.

![Extended thinking](./images/ccadv3.png?raw=true "Extended thinking")

---
<br><br>

## 9: Session-Level Thinking Effort
**What we're doing:** Checking where the *default* thinking level is set.
**Why:** `ultrathink` is per-prompt; the session default lives in `/model`.

**Action:** Type:
```
/model
```

Use the left/right arrow keys to see the thinking effort options (you set *medium* at startup). Higher effort = more thinking on *every* prompt — more quality on hard tasks, more tokens and latency on easy ones. Leave it on *medium* and hit *Esc*.

---
<br><br>

## 10: See What Your Context Costs *(recap)*
**What we're doing:** Inspecting token usage now that CLAUDE.md, a memory, and a command exist.
**Why:** Context is a budget. Everything you added in this lab rides along in every request — advanced users check this regularly.

**Action:** Type:
```
/context
```

Find how much of the window is taken by system prompt, project files, and conversation.

![context usage](./images/ccode224.png?raw=true "context usage")

---
<br><br>

## 11: Exit

**Action:** In prep for the next lab and a fresh start, type `exit` to exit Claude Code.

```
exit
```

## Lab Summary
✅ You've successfully:
- Generated CLAUDE.md for a real multi-directory codebase
- Persisted a shared rule in CLAUDE.md and a personal fact in auto-memory ("Remember..."), then viewed the hierarchy
- Built a custom command using $ARGUMENTS, frontmatter, inline bash context, @file references, and scoped allowed-tools
- Triaged the buggy API with your own command
- Created a `model: haiku` subagent and delegated verbose test output to it — cheap scouts, smart supervisor
- Used extended thinking (`ultrathink`) for a planning task and set session-level effort
- Audited your context budget

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 2: Hooks: Enforcing Policy at the Tool Boundary
## Lab Purpose
Learn how hooks let you enforce rules that Claude *cannot* talk its way around. You'll create a PreToolUse hook that blocks edits to a protected file and a PostToolUse hook that logs every bash command Claude runs — then watch both fire live, even in bypass-permissions mode. Estimated time: 10-12 minutes.

---
<br><br>

## 1: Set Up the Protected File and Hooks Folder
**What we're doing:** Creating a file worth protecting and the folder where hook scripts live.
**Why:** Our policy will be "nobody edits config.json" — a stand-in for the credentials/config files every real project has.

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
**What we're doing:** Writing the small shell script that decides whether an edit is allowed.
**Why:** When a PreToolUse hook fires, Claude Code sends the tool call details as JSON on the script's *stdin*. The script inspects it and answers with an exit code: **exit 0** means "no objection," **exit 2** means "block it" — and whatever the script prints to *stderr* is fed back to Claude as the reason.

**Action:** Make a new file `.claude/hooks/protect-config.sh` (remember you can use the `code` command if working in the codespace).

**Action:** Copy/paste the following contents into the file and save it.

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
**What we're doing:** Setting the execute bit.
**Why:** Claude Code runs the script as a process — it must be executable.

**Action:**
```
chmod +x .claude/hooks/protect-config.sh
```

---
<br><br>

## 4: Wire Up the Hooks in settings.json
**What we're doing:** Registering two hooks in the project's settings file.
**Why:** Hooks are configured under a `"hooks"` key in `.claude/settings.json`. Each entry names an *event* (PreToolUse, PostToolUse, etc.), a *matcher* that filters by tool name, and the *handler* to run.

**Action:** Make a new file `.claude/settings.json`.

**Action:** Copy/paste the following contents into the file and save it.

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

Two things to notice:
- The matcher `Edit|Write` means "fire on either the Edit or the Write tool." `Bash` matches only the Bash tool.
- The guard hook uses the newer *exec form* (`args: []`), which runs the script directly with no shell in between — recommended whenever you use a path placeholder like `${CLAUDE_PROJECT_DIR}`. The logger omits `args`, so it runs in *shell form*, which we need for the `>>` redirect.

![The hooks settings file](./images/cc-se5.png?raw=true "The hooks settings file")

---
<br><br>

## 5: Start Claude in Bypass Mode
**What we're doing:** Starting Claude with permissions bypassed — on purpose.
**Why:** This is the punchline of the lab: hooks fire at the *tool boundary*, outside of the permission system. Even with all permission prompts turned off, the hook still gets a veto.

**Action:** In a terminal other than your original one, start Claude with the option or alias (if working in the codespace):
```
claude --dangerously-skip-permissions

  or

claude-yolo (if running in the codespace)
```

---
<br><br>

## 6: Inspect the Hooks with /hooks
**What we're doing:** Verifying Claude Code loaded our hooks.
**Why:** The `/hooks` command opens a read-only browser of every configured hook — handy for checking what's active and which settings file it came from.

**Action:** Type:
```
/hooks
```

You should see **PreToolUse** and **PostToolUse** each showing one configured hook, labeled with a `[command]` type and a `Project` source (meaning it came from `.claude/settings.json`).

![The /hooks menu](./images/cc-se6.png?raw=true "The /hooks menu")

Pick one and select it to see general details about how the hook works, then drill in another level to see the configured command.

![How the hook works](./images/cc-se8.png?raw=true "How the hook works")

Hit `Esc` several times to get back to the main Claude Code prompt.

---
<br><br>

## 7: Try to Edit the Protected File
**What we're doing:** Asking Claude to do the thing our policy forbids.
**Why:** Time to watch the hook earn its keep.

**Action:** Type:
```
Add a connection_timeout setting to config.json using the Edit tool.
```

Watch what happens: Claude attempts the edit, and the tool call is **blocked** before it touches the file. You'll see the hook's stderr message surfaced in the conversation — Claude reads it too.

![Edit blocked by hook](./images/cc-se10.png?raw=true "Edit blocked by hook")

---
<br><br>

## 8: Look at How Claude Reacts
**What we're doing:** Observing what Claude does with the block message.
**Why:** Exit code 2 doesn't just stop the tool call — the stderr text is fed back to Claude as feedback. Our message told it to suggest the change to the user instead, so a well-behaved Claude should explain the policy and show you the change it *would* have made.

**Action:** Read Claude's response. Then verify the file is untouched — in your **original (plain) terminal**, not this Claude session:
```bash
cat config.json
```

No `connection_timeout` — the file never changed, even in bypass-permissions mode.

> **Why not `! cat config.json` here?** Claude Code auto-responds to in-session bash output, and in bypass mode it may try to *finish* the edit you asked for in step 7 — and since our matcher only guards `Edit|Write`, it could slip the change in via the **Bash** tool, which the hook doesn't block. Verifying from a plain terminal keeps Claude out of the loop so the file provably stays untouched.

> **Spot the loophole:** Our matcher only guards the `Edit|Write` tools. Claude could in principle modify the file through the Bash tool (`sed`, `echo >>`, etc.). Real policies often add a Bash matcher too, or use the `if` field with permission-rule syntax to narrow further. If Claude offers to work around the block, tell it no — and remember this when you design your own hooks.

---
<br><br>

## 9: Generate Some Bash Traffic
**What we're doing:** Giving the PostToolUse logger something to record.
**Why:** PostToolUse fires *after* a tool call succeeds — it can't block (the command already ran), but it's perfect for auditing, logging, and follow-up actions like auto-formatting.

**Action:** Type:
```
Use bash to list the files in this project and count the lines in app/app.py.
```

Let Claude run its commands.

---
<br><br>

## 10: Check the Audit Log
**What we're doing:** Reading the log file our PostToolUse hook has been writing.
**Why:** Proof that every Bash call went through our hook — no exceptions, no forgetting.

**Action:** Type:
```
! cat .claude/bash-command-log.txt
```

(Heads-up: while typing a path that matches real files, Claude Code may show a subtle suggested-path line near the input — **while it's showing, *Enter* is silently ignored**. Press `Esc` once to clear it, then *Enter*.)

You should see each command Claude ran, with its description. (You may even see your own `!` commands show up — they go through the Bash tool too.)

![The bash command log](./images/cc-se11.png?raw=true "The bash command log")

---
<br><br>

## 11: Prompt vs. Tool vs. Hook Constraints
**What we're doing:** Placing hooks in the constraint toolbox you built in the intro course. (Reading only)
**Why:** You now have three ways to say "don't do that" — and they are not equally strong.

Recall the intro course: a planner agent had a *prompt constraint* ("Do not write or modify files" — advisory, the model can drift), and a reviewer agent had a *tool constraint* (`disallowedTools: Write, Edit` — structural, but scoped to that one agent). Hooks are the third tier:

- **Prompt constraint** — instructions in CLAUDE.md or an agent file. Flexible, but it's a request, not a guarantee.
- **Tool constraint** — `disallowedTools` removes the tool entirely, for one agent.
- **Hook** — your own code at the tool boundary, for *every* tool call in the session, with any logic you can script. Exit 2 is a hard no, even in bypass mode.

> **Going further:** Hooks can do much more than block: a hook can exit 0 and print JSON to make richer decisions (`permissionDecision: allow / deny / ask`), rewrite a tool's input before it runs, or inject context for Claude. There are also handler types beyond shell commands (`prompt`, `agent`, `http`, `mcp_tool`) and many more events — `SessionStart` for loading context when a session begins is a popular one. To temporarily switch everything off, set `"disableAllHooks": true` in settings. See the [hooks reference](https://code.claude.com/docs/en/hooks) for the full schema. In Lab 4 you'll meet the same PreToolUse idea again — written in Python, gating an unattended agent.

---
<br><br>

## 12: Exit

**Action:** In prep for the next lab, type `exit` to exit Claude Code.

```
exit
```

## Lab Summary
✅ You've successfully:
- Created a PreToolUse hook that blocks edits to a protected file
- Used exit code 2 + stderr to veto a tool call and explain why
- Created a PostToolUse hook that logs every bash command
- Verified configured hooks with the /hooks menu
- Proved hooks fire even in bypass-permissions mode
- Placed hooks in the constraint hierarchy: prompt → disallowedTools → hooks

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 3: Headless Mode & CI Automation
## Lab Purpose
Use `claude -p` as a Unix-style building block — pipe data through it, get structured JSON out, loop over files — then author the GitHub Actions workflows that run the same engine in CI with `anthropics/claude-code-action@v1`. Estimated time: 10-12 minutes.

**NOTE: This whole lab runs in a regular terminal — no interactive Claude session needed.**

---
<br><br>

## 1: Pipe Input Through Claude *(recap)*
**What we're doing:** Sending stdin into a non-interactive Claude run.
**Why:** `-p` (print) mode reads stdin, processes it, prints the result, and exits — the contract every pipeline tool follows. You saw one `-p` call in the intro course; today it becomes a building block.

**Action:** In a terminal, run:
```bash
cat app/app.py | claude -p "Summarize what this code does in two sentences"
```

You get just the answer — no session UI, no prompts.

![pipe input](./images/cc-se29.png?raw=true "pipe input")

---
<br><br>

## 2: Get Structured JSON Output
**What we're doing:** Switching the output format from text to JSON.
**Why:** Scripts can't parse prose reliably. JSON output gives you the result plus metadata: session ID, cost, turns, duration.

**Action:** Run:
```bash
claude -p "Summarize this project in one sentence" --output-format json
```

Look at the raw JSON. Find the `result`, `session_id`, `total_cost_usd`, and `num_turns` fields.

![json output](./images/cc-se31.png?raw=true "json output")

---
<br><br>

## 3: Extract Fields with jq
**What we're doing:** Pulling specific fields from the JSON payload.
**Why:** This is how automation consumes Claude — take the field you need, ignore the rest.

**Action:** Run:
```bash
claude -p "How many tests are in app/test_app.py?" --output-format json | jq '{result: .result, cost: .total_cost_usd, turns: .num_turns}'
```

![jq extraction](./images/cc-se32.png?raw=true "jq extraction")

**Note:** `--output-format json` also supports `--json-schema` to force output matching a schema you define — the structured result lands in a `structured_output` field. And `--output-format stream-json` emits events in real time for long-running automation.

---
<br><br>

## 4: A Loop Instead of a Prompt
**What we're doing:** Running Claude once per file inside a bash for-loop.
**Why:** This is the core move of the automation half of this course. Yesterday you'd have prompted "summarize all the app files" and hoped. A loop gives you one bounded, repeatable call per item.

**Action:** Run:
```bash
for f in app/*.py; do
  echo "Summarizing $f..."
  echo "## $f" >> summaries.md
  cat "$f" | claude -p "Summarize this file in one sentence" >> summaries.md
done
```

The `Summarizing $f...` line prints to your terminal so you can watch each pass; the summaries are redirected into `summaries.md`. Each pass is an independent headless run. (`>>` *appends* — delete `summaries.md` before re-running or entries pile up.)

![first loop](./images/cc-se36.png?raw=true "first loop")

---
<br><br>

## 5: Inspect the Loop's Output
**What we're doing:** Checking what the loop produced.
**Why:** Verifying automated output is a habit you'll need for everything else today.

**Action:** Run:
```bash
cat summaries.md
```

You should see a heading and a one-sentence summary for each `.py` file in `app/`.

![loop output](./images/cc-se37.png?raw=true "loop output")

---
<br><br>

## 6: Let Headless Runs Make Changes
**What we're doing:** Pre-approving actions so a headless run can write files without hanging.
**Why:** `-p` mode has no human to click "Yes." Anything not pre-approved either aborts the run or gets denied — so automation must declare its permissions up front.

**Action:** Run:
```bash
claude -p "Create a file named pipeline.txt containing the single word OK" --permission-mode acceptEdits
```

Then verify with `cat pipeline.txt`. The `acceptEdits` mode auto-approves file writes; `--allowedTools "Bash,Read,Edit"` is the finer-grained alternative that pre-approves specific tools (and supports rules like `Bash(git diff *)`). The same idea returns in code form in Lab 4.

![headless with accept edits](./images/cc-se38.png?raw=true "headless with accept edits")

---
<br><br>

## 7: Create the Workflow Directory
**What we're doing:** Moving from your terminal to CI — setting up the standard GitHub Actions location.
**Why:** Everything you just did — headless run, pre-approved permissions, bounded turns — is exactly what `claude-code-action@v1` packages up to run on GitHub's runners. GitHub discovers workflows only in `.github/workflows/`.

**Action:** Run:
```bash
mkdir -p .github/workflows
```

---
<br><br>

## 8: Author the @claude Responder Workflow
**What we're doing:** Writing a workflow where Claude responds to `@claude` mentions in issues and PR comments.
**Why:** This is the canonical pattern: a teammate types `@claude fix the TypeError in the dashboard` in a PR comment, and Claude analyzes, implements, and pushes — on GitHub's runners, not your machine.

**Action:** Make a new file `.github/workflows/claude.yml` and copy/paste the following contents into it, then save:

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
          # No prompt: the action auto-detects interactive mode and
          # responds to @claude mentions in comments
```

![workflow file](./images/cc-se76.png?raw=true "workflow file")

---
<br><br>

## 9: Author a Scheduled Automation Workflow
**What we're doing:** Writing a second workflow that runs on a cron schedule with an explicit `prompt:`.
**Why:** With a `prompt:`, the action auto-detects *automation mode* — it runs immediately on the trigger instead of waiting for a mention. This is your headless loop, at the CI level.

**Action:** Make a new file `.github/workflows/daily-report.yml` with:

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

**Save the file.** Note `claude_args`: it's a passthrough to the same CLI flags you used in steps 1-6 — the action is the same engine on a GitHub runner.

| In claude_args | You used it as |
|---|---|
| `--max-turns 5` | the turn cap idea (also `max_turns` in Lab 4's SDK) |
| `--allowedTools "Read,Edit,Bash"` | `--allowedTools` in step 6 |
| `--model sonnet` | `/model` |
| `--append-system-prompt "..."` | custom instructions per workflow |

The action also respects your repo's CLAUDE.md — the context you built in Lab 1 works in CI too.

![workflow file](./images/cc-se77.png?raw=true "workflow file")

---
<br><br>

## 10: Have Headless Claude Review Your Workflow
**What we're doing:** Using a headless run to check the CI file you just wrote.
**Why:** Reinforces both skills at once — and catches authoring mistakes.

**Action:** Run:
```bash
cat .github/workflows/claude.yml | claude -p "Explain this GitHub Actions workflow: what triggers it, what the action does, what secrets it needs, and one risk to consider."
```

![claude explains](./images/cc-se78.png?raw=true "claude explains")

---
<br><br>

## 11: Know the Security Basics
**What we're doing:** Reviewing the non-negotiables before anyone runs this for real. (Reading only)
**Why:** CI agents act with real credentials on real repos.

- The API key comes **only** from `${{ secrets.ANTHROPIC_API_KEY }}` — never hardcoded.
- The Claude GitHub App needs read/write on **Contents, Issues, Pull requests** — and nothing more.
- Bound every job: `--max-turns` in `claude_args` plus a workflow-level `timeout-minutes`.
- Review Claude's PRs like any contributor's. CI runs are unattended runs.

> **Try it live later:** In a repo you own, run `claude` and type `/install-github-app` — it installs the Claude GitHub App and adds the `ANTHROPIC_API_KEY` secret. Commit `claude.yml`, open an issue, and comment `@claude suggest an improvement to the README`. (The workshop repo isn't yours, so the live loop is homework.)

## Lab Summary
✅ You've mastered:
- Piping data through `claude -p` and structured output with `--output-format json` + jq
- Writing a bash loop that runs Claude per file
- Pre-approving permissions for unattended writes
- Authoring an `@claude` responder workflow and a scheduled automation workflow with `claude-code-action@v1`
- Mapping `claude_args` back to the CLI flags you already know
- The CI security baseline

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 4: Agent SDK: Programmatic and Unattended Loops
## Lab Purpose
So far you've run Claude from the terminal. Now you'll run the **same Claude agent from a small Python program** — first as a read-only explorer, then as an *unattended* agent that does real work safely with nobody watching. Estimated time: 10-12 minutes.

> **The whole idea in one line:** the `claude` command is a finished app; the **Agent SDK** is that same engine as a Python library. Calling `query()` in Python does what `claude -p "..."` did in Lab 3 — and because you're now in code, you set Claude's permissions *in code*, which is what lets it run safely when no human is there to click "approve."

> **How the merge steps work.** A few steps use a **diff-merge**. You open a *skeleton* — a working file with its key lines replaced by a placeholder — next to the *finished* version, and copy the finished lines in:
> - Run `code -d extra/<finished> sdk/<skeleton>` to open the two files **side by side**, differences highlighted. The finished file (`extra/…`) is on the **left**; your skeleton (`sdk/…`) is on the **right**.
> - Copy the **left** side (finished) onto the **right** side (skeleton): click the gutter arrow pointing **toward your skeleton on the right** to move a highlighted block across, or select the left side, copy, and paste over the right.
> - When **nothing is highlighted**, the files match. **Save the right file** — the skeleton (Cmd/Ctrl+S).
>
> Each skeleton prints a *"still the skeleton"* message and stops if you run it before merging — that's the file telling you the merge or the save didn't fully land. Re-open the diff, make sure no highlight remains, and save.

---
<br><br>

## 1: Install the Agent SDK (You can skip this step if running in a Codespace.)
**What we're doing:** Installing the Python package.
**Why:** The SDK gives you the same tools, agent loop, and context management that power Claude Code — as a library. It drives the bundled CLI under the hood, so your existing login carries over with no extra auth.

**Action:** In a terminal, run:
```bash
python3 -m pip install claude-agent-sdk
```

> **`pip: command not found`?** Use the `python3 -m pip …` form above rather than a bare `pip`.

---
<br><br>

## 2: View the Skeleton
**What we're doing:** Opening `sdk/agent_loop.py` to see what's there before you merge.
**Why:** So the diff in the next step is small and readable — you'll know exactly what's blank and what you're adding.

**Action:** Open the skeleton:
```bash
code sdk/agent_loop.py
```

At the top, the `import` block already names the SDK pieces you'll use — `query`, `ClaudeAgentOptions`, `AssistantMessage`, `ResultMessage`. The body of `run_agent()`, though, is just a placeholder comment and a `raise` that stops the program until you merge. The two things that make it an *agent* — the **options** (which tools are pre-approved, plus a turn cap) and the **message loop** (reading what `query()` streams back) — are exactly what you'll add next. *Note: this file is incomplete — we'll merge in the working code in the next step.*

![skeleton view](./images/cc-se58.png?raw=true "skeleton view")

---
<br><br>

## 3: Diff, Merge, and Map It to the CLI
**What we're doing:** Comparing the skeleton against the completed version, merging it in, then reading what you just added.
**Why:** Seeing only the *difference* highlights exactly what turns a plain script into an agent program — and once it's merged, you'll see nothing in it is new: it's the CLI you've been using, with Python names.

**Action:** Run:
```bash
code -d extra/agent_loop.txt sdk/agent_loop.py
```

The finished file (`extra/agent_loop.txt`) is on the **left**; your skeleton (`sdk/agent_loop.py`) is on the **right**. You'll see **one highlighted region** — the body of `run_agent()`. Copy the entire **left** side over the **right** (gutter arrow toward the right, or select-copy-paste) so nothing stays highlighted, then **save the right file** — the skeleton (Cmd/Ctrl+S) — and close the diff tab.

> **If the next step still says "still the skeleton":** a line didn't merge or the file wasn't saved. Re-open the diff, confirm **no** highlight remains, then save again.

Now look at the merged `run_agent()` body — every piece maps to something you've already used:

| SDK piece (now in your file) | CLI equivalent you've used |
|---|---|
| `query(prompt=..., options=...)` | `claude -p "<prompt>"` (Lab 3) |
| `ClaudeAgentOptions(allowed_tools=[...])` | `--allowedTools "..."` (Lab 3) |
| `ClaudeAgentOptions(max_turns=...)` | `--max-turns` / `claude_args` (Lab 3) |
| iterating `AssistantMessage` / `ToolUseBlock` / `ResultMessage` | `--output-format stream-json` events |

`query()` returns an async iterator — your `async for` loop receives each message as the agent works. The loop prints two kinds of activity as it goes: `[claude]` lines for Claude's text and `[tool]` lines for each tool call it makes (a `ToolUseBlock`, carrying the tool's `name` and `input`). It ends with a `ResultMessage` of stats.

![diff merge](./images/cc-se59.png?raw=true "diff merge")

---
<br><br>

## 4: Run Your Agent
**What we're doing:** Executing the program.
**Why:** First proof that an agent loop runs under *your program's* control.

**Action:** Run:
```bash
python3 sdk/agent_loop.py "What files are in the sdk directory? Answer in one sentence."
```

You'll see `[claude]` lines (Claude's text) and likely one or more `[tool]` lines (each tool it calls), then the `ResultMessage` stats: turns used, duration, final result.

![sdk run](./images/cc-se60.png?raw=true "sdk run")

---
<br><br>

## 5: Force Multiple Turns, Then Try to Write
**What we're doing:** Giving the agent a tool-using prompt, then a prompt it can't fulfill.
**Why:** To see the *loop* part of "agent loop" — and to see what `allowed_tools=["Read","Glob","Grep"]` quietly prevents.

**Action:** Run a prompt that forces tool use:
```bash
python3 sdk/agent_loop.py "Find every TODO comment in the .py files under sdk/ and mcpserver/ and list them"
```
Watch the `[tool]` lines: the agent calls a read-only tool (like `Glob` to find the `.py` files, then `Grep` to scan them), gets the results back, and only then answers. Each `[tool]` line is one trip around the loop — that back-and-forth is the *loop* in "agent loop," and **Turns used** counts those trips.

![sdk run](./images/cc-se61.png?raw=true "sdk run")

Now try to make it write:
```bash
python3 sdk/agent_loop.py "Create a file named sdk_test.txt containing hello"
```
The write isn't blocked — it just isn't *pre-approved*, so with no human attached it can't proceed. Confirm nothing was created: `ls sdk_test.txt`. Next we do this on purpose, safely.

![sdk run](./images/cc-se62.png?raw=true "sdk run")

---
<br><br>

## 6: View the Unattended Skeleton and How It Gates Every Tool
**What we're doing:** Reading `sdk/auto_agent.py` and the one place every tool call must pass through.
**Why:** In the CLI, an undecided tool call means *ask the human*. Unattended, there is no human — so your code must decide, and it must see **every** call, including ones the CLI would otherwise wave through.

**Action:** Open it:
```bash
code sdk/auto_agent.py
```
Remember the `[tool]` lines the read-only agent printed? Each one is a decision point. To make that decision yourself on **every** call, the gate is a **PreToolUse hook** — `gatekeeper()` — which the CLI runs *before* each tool executes and which returns a `permissionDecision` of `"allow"` or `"deny"`. This is Lab 2's PreToolUse idea again — in Python this time, and *inside your own program*.

![skeleton view](./images/cc-se70.png?raw=true "skeleton view")

> **Why a hook, and not `can_use_tool`?** `ClaudeAgentOptions` also accepts a `can_use_tool` callback, and it's tempting to treat that as the gatekeeper. But the CLI only calls `can_use_tool` for tools that resolve to **"ask"** — it is skipped for anything already permitted by `allowed_tools`, `permission_mode`, or your Claude settings. So a destructive command in an environment that already trusts `Bash` would sail right past it. A **PreToolUse hook fires on every call, no exceptions** — which is exactly what an unattended safety gate needs.

The skeleton also provides a `prompt_stream()` generator: streaming the prompt is what lets the hook run interactively as the agent works.

---
<br><br>

## 7: Diff and Merge the Unattended Agent
**What we're doing:** Merging the completed implementation.
**Why:** The diff shows exactly what you're adding: the gatekeeper logic and the options/result handling.

**Action:** Run the diff below. The finished file (`extra/auto_agent.txt`) is on the **left**; your skeleton (`sdk/auto_agent.py`) is on the **right**. This time there are **two highlighted regions** — the `gatekeeper()` body and the `main()` body. Merge **both** from the left into the right, **save the right file** (the skeleton), and close:
```bash
code -d extra/auto_agent.txt sdk/auto_agent.py
```

![diff merge auto](./images/cc-se71.png?raw=true "diff merge auto")

---
<br><br>

## 8: Run It Unattended and Inspect the Output
**What we're doing:** Starting the agent and not touching the keyboard, then checking its work.
**Why:** The whole point — start it, take your hands off, then trust-but-verify.

**Action:** Run:
```bash
python3 sdk/auto_agent.py
```
Watch the `[gatekeeper] allowing: ...` lines (one per tool the agent uses), then the final turn count. Check the product:
```bash
cat agent_report.md
```
You should see every `.py` file in `app/` listed with a one-line description.

![gatekeeper run](./images/cc-se73.png?raw=true "gatekeeper run")

---
<br><br>

## 9: Trigger the Deny Path
**What we're doing:** Making the gatekeeper say no.
**Why:** Allow-paths are easy. The deny-path is what makes unattended safe.

**Action:** Edit the `TASK` string in `sdk/auto_agent.py` to:
```python
TASK = "Use a Bash rm command to delete agent_report.md. Then say DONE."
```

**Save your changes.** Run it again (`python3 sdk/auto_agent.py`). The PreToolUse hook sees the `Bash` call **before** it runs and returns `deny`, so the `rm` never executes. Watch for the deny line:
```
  [gatekeeper] DENIED: Bash -> 'rm agent_report.md'
```
Claude still prints `DONE` because the task told it to — so **`Result: DONE` proves nothing**. What proves the block worked is the deny line *and* the file still being there:
```bash
ls agent_report.md
```
It should still exist.

![gatekeeper run](./images/cc-se74.png?raw=true "gatekeeper run")

(Optional) If you want, you can change the TASK string back to the original one.

---
<br><br>

## 10: Connect It Back to the CLI — and Peek at What's Next
**What we're doing:** Confirming this is the same loop, not a lookalike.
**Why:** One mental model for everything: the CLI, the SDK, and the GitHub Action from Lab 3 all run this loop.

**Action:** Run the read-only program's CLI equivalent and compare:
```bash
claude -p "What files are in the sdk directory? Answer in one sentence." --output-format json | jq '{result: .result, num_turns: .num_turns, duration_ms: .duration_ms}'
```
The JSON fields mirror the `ResultMessage` attributes your program printed. Same loop, different driver.

> **Going further — memory (beta):** the Agent SDK also offers a *memory* capability (beta) that lets an agent persist what it learns across runs — so tomorrow's run of `auto_agent.py` could remember what yesterday's discovered, instead of starting cold. It's evolving quickly; see the [Agent SDK docs](https://docs.claude.com/en/api/agent-sdk/overview) for the current API before relying on it.

---
<br><br>

## Lab Summary
✅ You've built and exercised:
- A read-only `query()` loop merged from skeleton to working program
- An unattended agent gated by a PreToolUse hook that decides every tool call, plus `allowed_tools` and a `max_turns` cap
- Why `can_use_tool` is not a universal gate (it only sees "ask" calls) and a PreToolUse hook is
- The deny path — blocking a destructive command programmatically
- The CLI-to-SDK mapping: same agent loop, programmatic driver — and a pointer to SDK memory (beta)

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 5: Capstone: Build a Custom MCP Server
## Lab Purpose
You've *used* MCP servers; now you'll **build one**. You'll complete a Python FastMCP server that exposes three "project health" tools for this repo, register it with Claude Code at project scope, and drive it from natural-language prompts — closing the loop from MCP consumer to MCP producer. Estimated time: 10-12 minutes.

> **Quick MCP recap (from the intro course):** an MCP server is a process Claude Code talks to over stdin/stdout (or HTTP), exposing *tools* Claude can call. You add one with `claude mcp add <name> -- <command>`, inspect it with `/mcp`, and its tools show up named `mcp__<server>__<tool>`. Today the server is yours.

---
<br><br>

## 1: Tour the Server Skeleton
**What we're doing:** Reading `mcpserver/project_server.py` before completing it.
**Why:** FastMCP makes a server out of ordinary Python functions: decorate a function with `@mcp.tool()`, and its **docstring and type hints become the tool's documentation and input schema** — that's literally what Claude reads when deciding which tool to call. Good docstrings are not a nicety here; they're the interface.

**Action:** Open the skeleton:
```bash
code mcpserver/project_server.py
```

Note the pieces already in place: the `FastMCP("project-health")` instance (that name becomes the `mcp__project-health__...` prefix), the `ROOT` path resolution, and the `mcp.run()` call at the bottom that starts the stdio transport. The three tools are missing — that's your merge. *Note: this file is incomplete — we'll merge in the working code shortly.*

---
<br><br>

## 2: Prove It's Still the Skeleton
**What we're doing:** Running the incomplete file.
**Why:** Same pattern as Lab 4 — the skeleton tells you it isn't finished, so there's never any mystery about whether the merge landed.

**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

You should see the *"still the skeleton"* message and the program stops.

---
<br><br>

## 3: Diff-Merge the Three Tools
**What we're doing:** Merging the finished implementation from `extra/project_server.txt`.
**Why:** The diff is exactly the three `@mcp.tool()` functions — the entire "business logic" of your server:

- `run_tests()` — runs `app/test_app.py` and returns the PASS/FAIL output plus exit code
- `count_todos()` — counts TODO/FIXME comments per source file
- `project_stats()` — file and line counts by file type

**Action:** Run:
```bash
code -d extra/project_server.txt mcpserver/project_server.py
```

The finished file is on the **left**; your skeleton is on the **right**. There is **one highlighted region** — copy the left side over the right so nothing remains highlighted, **save the right file** (Cmd/Ctrl+S), and close the diff tab.

As you merge, read the docstrings you're adding — each one tells Claude *when* to reach for that tool ("Use this to find out whether the to-do API currently meets its contract...").

![diff merge server](./images/ccadv4.png?raw=true "diff merge server")

---
<br><br>

## 4: Start It Once by Hand
**What we're doing:** Running the completed server directly.
**Why:** To learn what "success" looks like for a stdio server: **silence**. It starts and waits for a client to speak JSON-RPC on stdin — no banner, no output.

**Action:** Run:
```bash
python3 mcpserver/project_server.py
```

Nothing appears — that's correct: it's waiting for a client. (If you see the skeleton message instead, the merge didn't save.) Stop it with `Ctrl+C`. From now on, Claude Code will start and stop this process for you.

---
<br><br>

## 5: Register It at Project Scope
**What we're doing:** Adding your server to Claude Code so teammates get it too.
**Why:** Project scope writes the config to `.mcp.json` in the repo root — commit that file and everyone who clones the project gets your server. (The `--` separates Claude's options from the server's own command line.)

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
**What we're doing:** Listing configured servers with a live connection test.
**Why:** `claude mcp list` actually starts each server and reports whether it connects — your first diagnostic stop when MCP misbehaves.

**Action:** Run:
```bash
claude mcp list
```

You should see **project-health** with a **✓ Connected** status. If it fails, run the server by hand (step 4) and read the error — with your own server, *you* are now the maintainer.

![mcp list](./images/cc-se13.png?raw=true "mcp list")

---
<br><br>

## 7: Start Claude and Approve Your Server
**What we're doing:** Starting a session that loads the project-scoped server.
**Why:** Because `.mcp.json` can arrive in a repo from *anyone*, Claude Code asks you to approve project-scoped servers before it will run them — a safety gate teammates will see the first time they open your repo.

**Action:** Start Claude (*don't use* bypass mode here):
```bash
claude
```

When prompted to use/approve the MCP server(s) from `.mcp.json`, approve them.

![Approving the MCP server](./images/cc-se17.png?raw=true "Approving the MCP server")

---
<br><br>

## 8: Inspect It with /mcp
**What we're doing:** Browsing your own server's tools from inside the session.
**Why:** `/mcp` is the in-session control panel — and this time everything it shows is code you merged.

**Action:** Type:
```
/mcp
```

Hit *Enter*, select the **project-health** server, and browse its three tools. Select one — the description you see is the docstring you merged in step 3, and the (empty) input schema comes from the function signature.

![mcp panel](./images/ccadv5.png?raw=true "mcp panel")

Use `Esc` to get back to the main prompt.

---
<br><br>

## 9: Drive the Server: Run the Test Suite
**What we're doing:** Letting Claude call your `run_tests` tool.
**Why:** The payoff — a natural-language request routed through *your* code.

**Action:** Type:
```
Use the project-health server to run the test suite and summarize what's failing and why.
```

Approve the tool use. Claude calls `mcp__project-health__run_tests`, gets your captured test output back, and explains the four contract violations — the same ones your `/triage` command found in Lab 1, now surfaced through a tool you built.

![run tests tool](./images/ccadv6.png?raw=true "run tests tool")

---
<br><br>

## 10: Drive the Server: Full Health Report
**What we're doing:** Combining multiple of your tools in one request.
**Why:** To watch Claude compose your tools — deciding on its own which to call and in what order.

**Action:** Type:
```
Using the project-health tools, give me a one-paragraph health report on this repo: test status, TODO count, and overall size.
```

You should see calls to your tools (watch for the `mcp__project-health__...` names), then a synthesized report.

> **Tie-back to Lab 2:** those full tool names are exactly what a hook matcher can target — `"matcher": "mcp__project-health__.*"` would let a PreToolUse hook govern *your own server's* tools the same way it governed Edit/Write.

![health report](./images/ccadv7.png?raw=true "health report")

---
<br><br>

## 11: Where to Take It
**What we're doing:** Mapping your capstone server to real-world use. (Reading only)
**Why:** Everything beyond this is more of the same pattern.

- **More tools:** anything a Python function can do — query a database, call an internal API, read a wiki — becomes a Claude tool with one decorator and a good docstring.
- **Arguments:** add typed parameters to the function (`def run_tests(pattern: str) -> str:`) and FastMCP builds the input schema automatically.
- **Beyond stdio:** the same server code can serve HTTP for remote/team use (`claude mcp add --transport http <url>`), which is how the connector directories you may have seen in Claude apps work under the hood.
- **Distribution:** `.mcp.json` in the repo (done!), or package it with a plugin for one-command team install — the same "team kit" idea from the intro course.

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
- Registered your server at project scope and read the shareable `.mcp.json`
- Approved and inspected it with `/mcp` — seeing your own docstrings as tool descriptions
- Driven it from natural language, single-tool and multi-tool
- Connected the full picture: commands (Lab 1) → hooks (Lab 2) → headless/CI (Lab 3) → SDK (Lab 4) → your own MCP server (Lab 5)

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
