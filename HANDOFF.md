# HANDOFF — cc-adv (Advanced Claude Code: True AI Productivity)

**Written:** 2026-07-10 · **Purpose:** full context for continuing work in a new conversation/model.

## Current state (authoritative)

| Artifact | Version | Notes |
|---|---|---|
| labs.md | **Revision 1.1 – 07/10/26** | 5 labs (see below); assumes intro course as prerequisite |
| Deck | **workshop-claude-code-adv_v1.2.pptx** (53 slides) | NEW file 07/10 — `_v1.pptx` and `_v1.1.pptx` are SUPERSEDED; delete after review |
| CHANGELOG.md | created 07/10 | First entry documents the 07/10 fixes |
| Also present | outline.md, description.md, anticipated-qa.md, app/ (Flask demo + tests), sdk/, mcpserver/, extra/ | Built 2026-07-07/08 in a separate session |

Labs: 1 Advanced Context/Custom Commands/Extended Thinking · 2 Hooks · 3 Headless & CI Automation · 4 Agent SDK (programmatic + unattended) · 5 Capstone: Build a Custom MCP Server.

## What was done on 2026-07-10

This course was authored recently (07/07–08) so it needed only light fixes, ported from live intro-course runs:

- **June 15 metering CANCELLED** — corrected on deck s27 (headless/CI) and s29 (Agent SDK credit). The separate SDK/headless/Actions metering never took effect.
- Model-indicator note loosened for the Sonnet 5 era + `/model` persistence tip (labs intro).
- `--model claude-sonnet-4-6` → `--model sonnet` in the Lab 3 GitHub Actions workflow and its claude_args table.
- Lab 2 step 10 (`! cat` audit log): added the suggested-path-line tip — while Claude Code's subtle path-suggestion line is showing, **Enter is silently ignored**; Esc clears it.
- `[Update - 2026-07-10]` speaker notes on the two edited slides; title slide → Version 1.2.

Explicitly checked and NOT applicable here (recorded in CHANGELOG): `#` memory shortcut, `/agents` wizard, manual-mode rename labs, rewind lab, skill-trigger lab, reviewer-format lab — this course has no steps exercising those flows. If a modes/memory recap slide is ever added, pull current wording from `ccode` deck v6.18+.

## Key product facts / conventions

See `ccode/HANDOFF.md` for the full list of product changes discovered this week (manual rename in v2.1.200, /agents & # removals, checkpointing semantics, backgrounded subagents, model-invoked skills, metering cancellation, `!`/suggestion-line Enter bug) and the working conventions — most importantly: **never edit decks in place** (OneDrive/AutoSave silently reverts; always save a new versioned filename + bump title slide + CHANGELOG).

## Where to pick up

1. **MISSING SCREENSHOTS**: labs.md references `ccadv1.png` … `ccadv7.png` — none exist in images/ (the 51 images there are reused ccode/cc-se shots). These seven were left pending when the course was built. Capture them during a live run-through.
2. **No live QA run yet**: this course has never been tested end-to-end in a Codespace. Run the lab-tester pass (fresh Codespace → all 5 labs), which is exactly how every intro-course issue was found. Pay attention to Lab 3 (headless flags on current build), Lab 4 (Agent SDK API currency — pip `claude-agent-sdk`), and Lab 5 (MCP server registration UX).
3. Delete superseded decks `workshop-claude-code-adv_v1.pptx` and `_v1.1.pptx` once v1.2 is confirmed.
4. anticipated-qa.md was generated at build time (07/07) — refresh after the fixes above if it references June 15 metering or old mode names.
5. Deck was authored post-rename, but do a quick pass for "default mode" phrasing on the modes-adjacent slides during the QA run to be safe.
