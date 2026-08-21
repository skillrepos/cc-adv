# HANDOFF — cc-adv (Advanced Claude Code: True AI Productivity)

**Written:** 2026-07-10 · **Last updated:** 2026-08-20 (labs 1.9 / deck v1.7) · **Purpose:** full context for continuing work in a new conversation/model.

## Current state (authoritative)

| Artifact | Version | Notes |
|---|---|---|
| labs.md | **Revision 1.9 – 08/20/26** | 5 labs (see below); assumes intro course as prerequisite |
| Deck | **workshop-claude-code-adv_v1.7.pptx** (63 slides / 55 visible) | NEW file 08/20 — v1 through v1.6 are SUPERSEDED |
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

## 2026-08-20 — August currency pass (labs 1.8 / deck v1.6)

Run alongside the same pass on `ccode` (Rev 6.21). Full detail in CHANGELOG.md. The headlines:

- **A regression worth remembering.** The July 10 entry claims the cancelled June-15 separate-metering note was "corrected on deck s27 and s29". It was **still on three slides** in v1.5 (32, 34, 44) — the July fix caught two and missed one, and slide numbers had shifted. Now removed from all three and confirmed by a whole-deck regex sweep. **When you retire a claim, grep the entire deck for it.**
- **NEW deck slide 18, "Custom Commands Are Skills Now"** — the largest content gap. Commands merged into skills; both file forms create the same `/name`.
- **ultrathink was described wrongly** on slide 20 and in Lab 1: it is a per-turn in-context nudge, **not** a max-budget trigger, and the effort level sent to the API is unchanged.
- Pricing, the SDK memory framing, and the setup URL corrected; `ultrareview` verified and extended with `--post`.
- Lab 4 gained the `setting_sources` fact and the **Lab 2 hook fires inside the Lab 4 agent** tie-in.

### Verified-current product facts specific to this course (2026-08-20)

- **Agent SDK: omitting `setting_sources` is equivalent to `["user","project","local"]`.** The SDK loads CLAUDE.md, skills, agents, hooks and settings from `.claude/` just like the CLI. Filesystem hooks and programmatic `hooks=` callbacks run side by side in the same lifecycle. `setting_sources=[]` is the isolation switch, but managed policy, `~/.claude.json` and auto-memory are read regardless — Anthropic's multi-tenant guidance is `setting_sources=[]` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- **Libraries pinned and tested:** `claude-agent-sdk` 0.1.73 and `mcp` 1.27.0. Every API the labs use still exists (`ClaudeSDKClient` exists too, despite what some summaries claim). No code changes were needed.
- `claude ultrareview [target]` is current: `--json`, `--timeout <minutes>` (30-min default), `--post` to comment on a GitHub PR (v2.1.227+). Exits 0/1 so CI can branch on it.
- `/sandbox` **is** a real command (macOS/Linux/WSL2; not native Windows). The deck references sandboxing twice as the enforcement layer without ever explaining it.
- Prompt cache is keyed by **model and effort level**; changing either mid-session forces a full uncached turn, and Claude Code now asks you to confirm an effort change. Subagents get their own 5-minute cache; forks inherit the parent's.
- Agent teams remain experimental and off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), are a **CLI** feature not an SDK one, and are unavailable in `-p`. Dynamic workflows / `ultracode` are now documented and GA on paid plans.

### All four gaps CLOSED in labs 1.9 / deck v1.7 (2026-08-20)

Sandboxing (slide 28), prompt cache (35), agent teams (56) and dynamic workflows (57) are now in the deck, and Lab 1 step 6 exercises the SKILL.md form. Time was paid for by hiding four slides (13, 44, 50, 58) — visible count unchanged at 55. See CHANGELOG.

**Timing to watch on the next live run.** The arithmetic says flat, but it is untested: the four new slides are ~11–12 min of new lecture against ~10 min of trims, and Agent Teams is the one most likely to run long because it reliably generates "can we use this?" questions. If the course runs over, the next-cheapest trims are the two remaining SDK conceptual slides (the section still makes the same-loop point across three slides) and "Claude Code on the Web".

**Lab 1 step 6 has one live dependency worth verifying in a Codespace:** Claude Code only watches skill directories that existed at session start, so step 4 creates `.claude/skills` before the step-5 restart. If the hot-reload demo fails in the room, the fallback line tells students to restart once — but confirm the happy path works before delivery, because the whole point of the step is that no restart is needed.

## Key product facts / conventions

See `ccode/HANDOFF.md` for the full list of product changes discovered this week (manual rename in v2.1.200, /agents & # removals, checkpointing semantics, backgrounded subagents, model-invoked skills, metering cancellation, `!`/suggestion-line Enter bug) and the working conventions — most importantly: **never edit decks in place** (OneDrive/AutoSave silently reverts; always save a new versioned filename + bump title slide + CHANGELOG).

## Where to pick up

1. **MISSING SCREENSHOTS**: labs.md references `ccadv1.png` … `ccadv7.png` — none exist in images/ (the 51 images there are reused ccode/cc-se shots). These seven were left pending when the course was built. Capture them during a live run-through.
2. **No live QA run yet**: this course has never been tested end-to-end in a Codespace. Run the lab-tester pass (fresh Codespace → all 5 labs), which is exactly how every intro-course issue was found. Pay attention to Lab 3 (headless flags on current build), Lab 4 (Agent SDK API currency — pip `claude-agent-sdk`), and Lab 5 (MCP server registration UX).
3. Delete superseded decks `workshop-claude-code-adv_v1.pptx` and `_v1.1.pptx` once v1.2 is confirmed.
4. anticipated-qa.md was generated at build time (07/07) — refresh after the fixes above if it references June 15 metering or old mode names.
5. Deck was authored post-rename, but do a quick pass for "default mode" phrasing on the modes-adjacent slides during the QA run to be safe.
