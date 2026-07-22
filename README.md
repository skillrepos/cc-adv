# Advanced Claude Code: True AI Productivity

## Go beyond the basics — custom commands, hooks, headless/CI automation, the Agent SDK, and your own MCP server

This 3-hour hands-on workshop picks up where the introductory Claude Code course leaves off. You'll harness Claude Code's agentic capabilities for complex, multi-step engineering workflows — creating reusable slash commands, enforcing policy with hooks, integrating Claude Code into CI/CD pipelines, driving the agent loop from Python with the Claude Agent SDK, and finishing with a capstone where you build a custom MCP server for a real-world use case.

**Prerequisites:** Completion of the introductory Claude Code workshop (skillrepos/ccode) or equivalent hands-on experience. A paid Claude account. Comfort with terminal-based workflows.

**NOTE: This is a hands-on workshop — bring a personal laptop (corporate ones may not allow the labs to work).**

These instructions will guide you through configuring the environment you'll use for the labs.

## 1. If you don't already have a paid Claude account, sign up for one at [claude.ai](https://claude.ai).

You **must** have a paid Claude account to use Claude Code.

<br><br>

## 2. Choose where you want to run Claude Code.

**Important note: Lab commands and screenshots reflect using terminal integration in Codespace/VS Code integration. Steps and functionality in other environments may vary!**

If you would like to use the GitHub Codespace zero-install option that runs in a browser, skip to step 6. Otherwise, continue with step 3.

<br><br>

## 3. Clone down the training repo locally from GitHub.

```
git clone https://github.com/skillrepos/cc-adv
```

<br><br>

## 4. If you want to install Claude Code on your local system (and are allowed to):

Go to [Get Started](https://code.claude.com/docs/en/overview#get-started), choose the **Terminal** tab and proceed with installation for your desired platform.

Then install the Python lab dependencies from the repo root:

```
python3 -m pip install -r requirements.txt
```

(ideally inside a virtual environment).

<br><br>

## 5. Go to the cloned repo, start Claude and authenticate as appropriate.

If in the terminal integration, change into your cloned directory and you can likely follow the directions in [STARTUP.md](./STARTUP.md) to complete this task. Otherwise, consult the online documentation.

<br><br>

---
> **STOP HERE if NOT using the GitHub Codespace environment.**

> **Directions for GitHub Codespace environment setup follow.**
---
<br><br>

## 6. Set codespace timeout

While logged in to GitHub, go to https://github.com/settings/codespaces. Set the default idle timeout to a larger value (like 90 minutes or more) so your codespace doesn't stop during lecture segments.

<br><br>

## 7. Start the codespace

From the repo page at https://github.com/skillrepos/cc-adv, click the green **Code** button, choose the **Codespaces** tab, and create a codespace on main. Give it a few minutes to build — the container installs Claude Code, creates a Python virtual environment, and installs the lab dependencies automatically.

<br><br>

## 8. Start Claude Code and authenticate

Open the terminal in the codespace and follow the steps in [STARTUP.md](./STARTUP.md).

<br><br>

## Repo layout

```
app/          Flask to-do API — the analysis target for several labs
              (4 of its behavior tests fail BY DESIGN — that's lab material)
sdk/          Agent SDK skeletons for Lab 4 (diff-merge with extra/)
mcpserver/    MCP server skeleton for the Lab 5 capstone (diff-merge with extra/)
extra/        Completed versions of skeleton files + environment config
labs.md       THE lab document — follow this during the workshop
outline.md    Course outline
```

## Troubleshooting

- **`pip: command not found`** — use `python3 -m pip ...` instead.
- **`ModuleNotFoundError: flask` (or `mcp`, `claude_agent_sdk`)** — run `python3 -m pip install -r requirements.txt` from the repo root, or make sure the `.venv` is activated (new terminals in the codespace activate it automatically).
- **A skeleton file prints "still the skeleton"** — the diff-merge didn't complete or the file wasn't saved. Re-open the diff, confirm no highlighted differences remain, and save the right-hand file.

## License

Materials in this repository are for educational use only by attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
