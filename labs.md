# Advanced Claude Code: True AI Productivity
## Go beyond the basics — custom commands, hooks, CI automation, the Agent SDK, and your own MCP server
## Session Labs
## Revision 1.10 - 08/21/26

<br><br>

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**Copy and paste may not work as expected if using the mouse. If not, use the keyboard shortcuts - *Ctrl+C/Cmd+C and Ctrl+V/Cmd+V*.**

**If you haven't done so already, set your model to `Sonnet` instead of `Opus`.**

> In Claude Code at the prompt, type:
> ```
> /model
> ```
> In the list that comes up, use the up/down arrow keys to move the pointer to *Sonnet* and hit *Enter*. **Select by name, not by number** — the menu order shifts as models are added (the list carries Opus 5 and, on some accounts, Fable 5). Each row also shows that model's price per million tokens. Also use the **left/right** arrow keys to set the **effort level** to *medium* (it defaults to *high*).
>
> ![set model](./images/ccode209.png?raw=true "set model")
>
> You should see an indicator that the model was set to a *Sonnet* model (currently *Sonnet 5* / `claude-sonnet-5` — the exact version shown may be newer) with *medium* effort. Note: your `/model` selection is saved as the default for new sessions; press `s` in the model list to set it for the current session only.
>
> **Today's ladder:** Haiku 4.5 $1/$5 per million tokens · Sonnet 5 $2/$10 · Opus 5 $5/$25 · Fable 5 $10/$50. Sonnet 5, Opus 5 and Fable 5 all carry a 1M-token context window at standard rates, so above Haiku you buy judgment, speed, and knowledge recency (Opus 5's cutoff is May 2026 against January 2026 for Sonnet 5 and Fable 5).
>
<br><br>

**NOTE:** This course assumes you've completed the introductory Claude Code workshop (or equivalent). Steps that exercise something from that course are marked *(recap)* and kept quick. Since **August 14, 2026** your sessions start in **auto mode** on Pro, Max, and Team plans, so most permission prompts are already gone — a background classifier approves routine actions and stops for risky ones. Where a lab says it's OK, `claude --dangerously-skip-permissions` (alias `claude-yolo` in the codespace) removes the remaining checks as well.

<br><br>

---
<br><br>

# Lab 1: Advanced Context, Custom Commands & Extended Thinking
## Lab Purpose
Build project context on a real codebase, a parameterized custom command, a skill, and a low-cost Haiku subagent, and use extended thinking. Estimated time: 10-12 minutes.

---
<br><br>

## 1: Start Claude and Scout the Codebase *(recap)*
The repo holds a Flask to-do API in `app/` (its test suite fails in 4 places *by design*), Agent SDK skeletons in `sdk/`, and an MCP server skeleton in `mcpserver/`.

**Action:** In the terminal, start Claude:
```bash
claude
```

Then type:
```
Give me a one-paragraph overview of this repo: what's in app/, sdk/, and mcpserver/, and how do I run the tests?
```

---
<br><br>

## 2: Generate the Project Context File *(recap)*
CLAUDE.md is read at the start of every session.

**Action:** Type:
```
/init
```

In **manual** mode `/init` first asks **"Do you want to create CLAUDE.md?"** — choose option 1 (Yes); in **auto** mode (the default) it just creates it without asking. Open the generated `CLAUDE.md` (the `code` command works in the codespace) and skim it.

![claude.md](./images/ccode226.png?raw=true "claude.md")

---
<br><br>

## 3: Persist a Rule, a Memory — and See the Hierarchy *(recap)*
One fact, two homes: a shared rule in CLAUDE.md (committed, repo-wide) and a personal fact in *auto-memory* (a MEMORY.md per project, per user).

**Action:** First, the shared rule. Type:
```
Add this standing rule to CLAUDE.md: The test suite is run with python3 app/test_app.py. Never edit app/test_app.py - it defines the correct contract.
```

Approve the edit and confirm the rule landed in `CLAUDE.md`.

**Action:** Now a personal memory. Type:
```
Remember that when I ask for code reviews in this repo, I want short, test-first explanations.
```

Watch for the saved-memory confirmation, then verify where it went (in the codespace):
```
! cat ~/.claude/projects/-workspaces-cc-adv/memory/MEMORY.md
```
(Running locally? The directory under `~/.claude/projects/` is named after your repo path.)

> **Rule of thumb:** *enforced and shared* → CLAUDE.md; *personal and learned* → auto-memory (per user, per machine; the first ~200 lines load each session).

![Add rule and memory](./images/ccadv9.png?raw=true "Add rule and memory")

**Action:** Now see how the layers stack. Type:
```
/memory
```

The view lists **Auto-memory**, **Project memory** (`./CLAUDE.md`) and **User memory** (`~/.claude/CLAUDE.md`), plus an option to open the auto-memory folder. Hit *Esc* to exit.

![memory hierarchy](./images/ccode228.png?raw=true "memory hierarchy")

---
<br><br>

## 4: Create a Real Custom Command
**Action:** In a terminal tab (keep Claude running), create the folders:
```bash
mkdir -p .claude/commands .claude/skills
```

**Action:** Create `.claude/commands/triage.md` (the `code` command works in the codespace) with these contents, and save:

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

- **`$ARGUMENTS`** — text typed after `/triage`; positional `$1`, `$2`, ... also work.
- **`` !`git status --short` ``** — runs *when the command is invoked*; its output is injected into the prompt.
- **`@CLAUDE.md`** — pulls the file into context, same as an @ mention.
- **`allowed-tools`** — scopes what the command may do; note the fine-grained `Bash(git status:*)` syntax.

![Creating the triage command](./images/ccadv1.png?raw=true "Creating the triage command")

---
<br><br>

## 5: Run the Command on the Buggy API
**Action:** Claude Code loads custom commands at **startup**, so your running session doesn't know `/triage` yet (it would say *"Unknown command: /triage"*). Restart Claude — `exit`, then `claude`. Then type:
```
/triage app/app.py
```

In **manual** mode, the first time you invoke a project command Claude asks **"Use skill 'triage'?"** — approve it (option 1). In **auto** mode (the default) the skill loads without asking.

Git context and CLAUDE.md are injected automatically. The triage should flag the API returning **500** where the contract demands **400** (bad input) or **404** (missing item) — the failures automation meets again in Labs 3-5.

![Running the triage command](./images/ccadv2.png?raw=true "Running the triage command")

---
<br><br>

## 6: Turn the Command Into a Skill — Without Restarting
Custom commands have **merged into skills**: `.claude/commands/triage.md` and `.claude/skills/triage/SKILL.md` both create `/triage`, and the frontmatter means the same in both.

**Action:** In your terminal tab (leave Claude running):
```bash
mkdir -p .claude/skills/triage
mv .claude/commands/triage.md .claude/skills/triage/SKILL.md
```

**Action:** Now, **without restarting Claude**, run it against a different file:
```
/triage app/datastore.py
```

It works: **Claude Code watches skill directories and picks up adds, edits and removals inside the current session.** Commands and agents do not.

> **If `/triage` isn't found**, restart Claude once — the watcher only follows directories that already existed at session start, which is why we created `.claude/skills` earlier.

> **The folder also buys you:** supporting files beside `SKILL.md` (a `scripts/` helper makes results deterministic); `disable-model-invocation: true` for user-only skills (leave it off and Claude may load the skill itself when your request matches the description); `context: fork` for its own subagent; `background: true` to detach. A personal skill in `~/.claude/skills/` beats a project one; a project skill named `code-review` replaces the bundled `/code-review`.

---
<br><br>

## 7: Delegate to a Cheaper Model — a Haiku Subagent
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

**Action:** A new agent isn't picked up until Claude restarts (the running session says *"There's no test-scout agent type available"*). Restart — `exit`, then `claude`. Then type:
```
Use the test-scout subagent to run the test suite and summarize the failures.
```

Approve as needed; the subagent runs in the background and asks before running `python3 app/test_app.py`. You get a compact report (10 passed / 4 failed with causes), run on Haiku, with the full test output kept out of your main context.

> **`model:` values:** an alias (`haiku`, `sonnet`, `opus`, `fable`), a full model string (`claude-haiku-4-5`), or `inherit` (the default). Same field in command frontmatter; `--model` for headless/CI; `ClaudeAgentOptions(model="haiku")` in the SDK (Lab 4). **Cheap scouts, smart supervisor.**

![Haiku test-scout subagent](./images/ccadv8.png?raw=true "Haiku test-scout subagent")

---
<br><br>

## 8: Use Extended Thinking for a Planning Task
The **effort level** in `/model` is your session-wide dial; `ultrathink` anywhere in a prompt asks for deeper reasoning **on that turn only**.

> **What `ultrathink` does:** Claude Code adds an in-context instruction to think harder; the effort level sent to the API is *unchanged*, so it stacks on whatever you set. **Not** keywords: "think", "think hard", "think more" — ordinary prompt text.

**Action:** Type the following, then hit *Ctrl+o* while it runs to watch the thinking stream:
```
ultrathink: Propose a refactoring plan for app/ that fixes the 400/404 contract violations without changing test_app.py. Consider at least two approaches and recommend one. Plan only - do not edit files.
```

![Extended thinking](./images/ccadv3.png?raw=true "Extended thinking")

---
<br><br>

## 9: Session-Level Effort
The session default lives in `/model` — or in `/effort`, which sets it directly without opening the model picker.

**Action:** Type:
```
/model
```

Use the left/right arrow keys to see the effort options: **low · medium · high · xhigh · max** (`high` is the default). Leave it on *medium* and hit *Esc*.

> **Also:** `/effort ultracode` is a Claude Code *setting*, not a model level — it runs at `xhigh` with a dynamic multi-agent workflow. And **changing effort mid-session invalidates your prompt cache** (keyed by model *and* effort), so Claude Code asks you to confirm. Set model and effort once, at the top of a session.

---
<br><br>

## 10: See What Your Context Costs *(recap)*
Everything you added in this lab rides along in every request.

**Action:** Type:
```
/context
```

Find how much of the window is taken by system prompt, project files, and conversation.

> **Companion:** `/usage` answers "what have I spent?" and on a paid plan breaks usage down **by attribution** — skills, subagents, plugins, each MCP server. Try it now; remember it in Lab 5.

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
- Generated CLAUDE.md for a multi-directory codebase
- Persisted a shared rule and a personal auto-memory; viewed both with `/memory`
- Built `/triage` with `$ARGUMENTS`, inline bash context, `@file` references and scoped `allowed-tools`
- Converted it to a **skill** — hot-reloaded without a restart
- Delegated verbose test output to a `model: haiku` subagent
- Used `ultrathink` and set session-level effort
- Audited your context budget

<br><br>
---
## END OF LAB
---
<br><br>

# Lab 2: Hooks: Enforcing Policy at the Tool Boundary
## Lab Purpose
Create a PreToolUse hook that blocks edits to a protected file and a PostToolUse hook that logs every bash command, then watch both fire — even in auto and bypass-permissions modes. Estimated time: 10-12 minutes.

---
<br><br>

## 1: Set Up the Protected File and Hooks Folder
The policy: nobody edits `config.json` — a stand-in for the credentials/config files every real project has.

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

---
<br><br>

## 6: Inspect the Hooks with /hooks
**Action:** Type:
```
/hooks
```

You should see **PreToolUse** and **PostToolUse** each showing one hook, with a `[command]` type and a `Project` source (from `.claude/settings.json`).

![The /hooks menu](./images/cc-se6.png?raw=true "The /hooks menu")

Select one to see how the hook works, then drill in another level to see the configured command.

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

No `connection_timeout` — the file never changed, even in bypass-permissions mode.

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

(Heads-up: while typing a path that matches real files, Claude Code may show a subtle suggested-path line near the input — **while it's showing, *Enter* is silently ignored**. Press `Esc` once to clear it, then *Enter*.)

You should see each command Claude ran, with its description. (Your own `!` commands appear too — they go through the Bash tool.)

![The bash command log](./images/cc-se11.png?raw=true "The bash command log")

---
<br><br>

## 11: Prompt vs. Tool vs. Hook Constraints
Four ways to say "don't do that," and they are not equally strong. (Reading only)

- **Prompt constraint** — CLAUDE.md or agent-file instructions: a request, not a guarantee.
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

# Lab 3: Headless Mode & CI Automation
## Lab Purpose
Use `claude -p` as a Unix-style building block — pipe data through it, get JSON out, loop over files — then author the GitHub Actions workflows that run the same engine in CI with `anthropics/claude-code-action@v1`. Estimated time: 10-12 minutes.

**NOTE: This whole lab runs in a regular terminal — no interactive Claude session needed.**

---
<br><br>

## 1: Pipe Input Through Claude *(recap)*
`-p` (print) mode reads stdin, processes it, prints the result, and exits.

**Action:** In a terminal, run:
```bash
cat app/app.py | claude -p "Summarize what this code does in two sentences"
```

You get just the answer — no session UI, no prompts.

![pipe input](./images/cc-se29.png?raw=true "pipe input")

---
<br><br>

## 2: Get Structured JSON Output
JSON output gives you the result plus metadata: session ID, cost, turns, duration.

**Action:** Run:
```bash
claude -p "Summarize this project in one sentence" --output-format json
```

Find the `result`, `session_id`, `total_cost_usd`, and `num_turns` fields.

![json output](./images/cc-se31.png?raw=true "json output")

---
<br><br>

## 3: Extract Fields with jq
**Action:** Run:
```bash
claude -p "How many tests are in app/test_app.py?" --output-format json | jq '{result: .result, cost: .total_cost_usd, turns: .num_turns}'
```

![jq extraction](./images/cc-se32.png?raw=true "jq extraction")

**Note:** `--output-format json` also supports `--json-schema`, forcing output to match a schema you define — the result lands in a `structured_output` field. `--output-format stream-json` emits events in real time for long-running automation.

---
<br><br>

## 4: A Loop Instead of a Prompt
A loop gives you one bounded, repeatable call per item.

**Action:** Run:
```bash
for f in app/*.py; do
  echo "Summarizing $f..."
  echo "## $f" >> summaries.md
  cat "$f" | claude -p "Summarize this file in one sentence" >> summaries.md
done
```

`Summarizing $f...` prints to your terminal; the summaries are redirected into `summaries.md`. Each pass is an independent headless run. (`>>` *appends* — delete `summaries.md` before re-running or entries pile up.)

![first loop](./images/cc-se36.png?raw=true "first loop")

---
<br><br>

## 5: Inspect the Loop's Output
**Action:** Run:
```bash
cat summaries.md
```

You should see a heading and a one-sentence summary for each `.py` file in `app/`.

![loop output](./images/cc-se37.png?raw=true "loop output")

---
<br><br>

## 6: Let Headless Runs Make Changes
`-p` mode has no human to click "Yes": anything not pre-approved aborts or is denied, so automation must declare its permissions up front.

> **The August 2026 auto-mode default does not rescue you here.** Interactive sessions start in auto mode on Pro/Max/Team, but `claude -p` and the Agent SDK start in `default` — so pre-approving permissions stays mandatory for anything unattended.

**Action:** Run:
```bash
claude -p "Create a file named pipeline.txt containing the single word OK" --permission-mode acceptEdits
```

Verify with `cat pipeline.txt`. `acceptEdits` auto-approves file writes; `--allowedTools "Bash,Read,Edit"` is the finer-grained alternative (and supports rules like `Bash(git diff *)`). The same idea returns in code in Lab 4.

> **Two more CI flags.** `--permission-mode dontAsk` runs *only* what your `permissions.allow` rules and the read-only command set cover, denying the rest instead of prompting. `--bare` skips auto-discovery of hooks, skills, plugins, MCP servers and CLAUDE.md, making a CI run reproducible across machines.

![headless with accept edits](./images/cc-se38.png?raw=true "headless with accept edits")

---
<br><br>

## 7: Create the Workflow Directory
GitHub discovers workflows only in `.github/workflows/`.

**Action:** Run:
```bash
mkdir -p .github/workflows
```

---
<br><br>

## 8: Author the @claude Responder Workflow
The canonical pattern: a teammate comments `@claude fix the TypeError in the dashboard` on a PR, and Claude analyzes, implements and pushes on GitHub's runners.

**Action:** Create `.github/workflows/claude.yml` with these contents, and save:

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
With a `prompt:`, the action auto-detects *automation mode* — it runs immediately on the trigger instead of waiting for a mention.

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

**Save the file.** `claude_args` is a passthrough to the same CLI flags you used in steps 1-6.

| In claude_args | You used it as |
|---|---|
| `--max-turns 5` | the turn cap idea (also `max_turns` in Lab 4's SDK) |
| `--allowedTools "Read,Edit,Bash"` | `--allowedTools` in step 6 |
| `--model sonnet` | `/model` |
| `--append-system-prompt "..."` | custom instructions per workflow |

The action also respects your repo's CLAUDE.md, so the Lab 1 context works in CI too.

![workflow file](./images/cc-se77.png?raw=true "workflow file")

---
<br><br>

## 10: Have Headless Claude Review Your Workflow
**Action:** Run:
```bash
cat .github/workflows/claude.yml | claude -p "Explain this GitHub Actions workflow: what triggers it, what the action does, what secrets it needs, and one risk to consider."
```

![claude explains](./images/cc-se78.png?raw=true "claude explains")

---
<br><br>

## 11: Know the Security Basics
CI agents act with real credentials on real repos. (Reading only)

- The API key comes **only** from `${{ secrets.ANTHROPIC_API_KEY }}` — never hardcoded.
- The Claude GitHub App needs read/write on **Contents, Issues, Pull requests** and nothing more.
- Bound every job: `--max-turns` in `claude_args` plus a workflow-level `timeout-minutes`.
- Review Claude's PRs like any contributor's.

> **Try it live later:** in a repo you own, run `claude` and type `/install-github-app` — it installs the Claude GitHub App and adds the `ANTHROPIC_API_KEY` secret. Commit `claude.yml`, open an issue, and comment `@claude suggest an improvement to the README`. (The workshop repo isn't yours, so this is homework.)

## Lab Summary
✅ You've mastered:
- Piping data through `claude -p`, with `--output-format json` + jq
- A bash loop that runs Claude per file
- Pre-approving permissions for unattended writes
- An `@claude` responder and a scheduled workflow with `claude-code-action@v1`
- Mapping `claude_args` to the CLI flags you know
- The CI security baseline

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

![sdk run](./images/cc-se60.png?raw=true "sdk run")

---
<br><br>

## 5: Force Multiple Turns, Then Try to Write
**Action:** Run a prompt that forces tool use:
```bash
python3 sdk/agent_loop.py "Find every TODO comment in the .py files under sdk/ and mcpserver/ and list them"
```
Watch the `[tool]` lines: the agent calls a read-only tool (`Glob`, then `Grep`), gets results back, and only then answers. Each `[tool]` line is one trip around the loop; **Turns used** counts those trips.

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
**Action:** Edit the `TASK` string in `sdk/auto_agent.py` to:
```python
TASK = "Use a Bash rm command to delete agent_report.md. Then say DONE."
```

**Save your changes.** Run it again (`python3 sdk/auto_agent.py`). The PreToolUse hook sees the `Bash` call **before** it runs and returns `deny`, so the `rm` never executes. Watch for the deny line:
```
  [gatekeeper] DENIED: Bash -> 'rm agent_report.md'
```
Claude still prints `DONE` because the task told it to, so **`Result: DONE` proves nothing**. The proof is the deny line *and* the file still being there:
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

Nothing appears — correct. (If you see the skeleton message, the merge didn't save.) Stop it with `Ctrl+C`. From now on Claude Code starts and stops this process for you.

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

Hit *Enter*, select the **project-health** server and browse its three tools. Select one — the description is the docstring you merged in step 3; the (empty) input schema comes from the function signature.

![mcp panel](./images/ccadv5.png?raw=true "mcp panel")

Use `Esc` to get back to the main prompt.

---
<br><br>

## 9: Drive the Server: Run the Test Suite
**Action:** Type:
```
Use the project-health server to run the test suite and summarize what's failing and why.
```

Approve the tool use. Claude calls `mcp__project-health__run_tests`, gets your captured test output back, and explains the four contract violations — the ones `/triage` found in Lab 1, now through a tool you built.

![run tests tool](./images/ccadv6.png?raw=true "run tests tool")

---
<br><br>

## 10: Drive the Server: Full Health Report
**Action:** Type:
```
Using the project-health tools, give me a one-paragraph health report on this repo: test status, TODO count, and overall size.
```

You should see calls to your tools (watch for the `mcp__project-health__...` names), then a synthesized report.

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
- Connected the picture: commands → hooks → headless/CI → SDK → your own MCP server

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
