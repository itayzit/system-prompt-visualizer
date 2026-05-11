# System Prompt Visualizer

A static, single-page gallery that visualizes the composition of leaked system prompts from 10 major AI tools. Goal: **viral Twitter/LinkedIn post** — every change should be evaluated against shareability, screenshot-ability, and "wait, what?" moments.

## What it is

- **Single file**: [index.html](index.html) is the entire site (HTML + inline CSS + inline JS, no build step, no deps).
- **Deployment**: Vercel, auto-deploys on push to `main`. Repo: `itayzit/system-prompt-visualizer`.
- **Title**: "System prompts are an AI company's most important IP."
- **Format**: hero → categories legend → gallery of 10 tiles in three implicit groups (models / coding agents / vibe-coding products) → 6 highlight cards → "By the numbers" stats panel → footer. Clicking any tile opens a modal: 10×10 waffle grid colored by **universal category**, content-categories list with %, sample text, and 3 numbered observations.

## Data model

All data lives in the `TOOLS` array inside [index.html](index.html). Each tool:

```js
{name, model, totalTokens, group: 'model'|'agent'|'vibe', rank, note?, segments: [{name, cat, tokens, sample}], observations: [{title, description}]}
```

`cat` is one of the 8 universal categories (defined in `CATS` near the top of the script): `tools`, `identity`, `safety`, `memory`, `process`, `formatting`, `reference`, `examples`. Same `cat` → same color across every tool — this is what makes cross-tool comparison work. `note` (optional) renders a yellow callout in the modal — used to flag that Claude Code's 300k figure is a per-request fragment bundle, not a single prompt.

Currently covered (by group):
- **Models**: ChatGPT (GPT-5.5 Thinking), Claude (Opus 4.7 claude.ai), Gemini 3.1 Pro
- **Coding agents**: Claude Code (npm fragment bundle), Cursor, Codex, Antigravity
- **Vibe-coding**: Lovable, Replit, Bolt.new

Raw leaked prompts live in [prompts/](prompts/). Sources credited in the footer: `asgeirtj/system_prompts_leaks` and `x1xhlol/system-prompts-and-models-of-ai-tools`.

[analyze_prompt_visual.py](analyze_prompt_visual.py) is a legacy matplotlib script that produced the static PNGs in [examples/](examples/) — predecessor to the interactive page. Not part of the live site.

## Editorial bar for observations

The audience is **AI builders** — people writing system prompts, tuning models, deciding which provider to ship on. They want to see what a successful system prompt looks like and how the big labs differ. Observations must serve that, not just amuse generally.

### Style (strict)

Each observation is a **moral/punchy title + minimal body**. The body is a setup phrase + the verbatim quote. Stop there. Pattern:

> **Anthropic shames their own model**
> Line 776 makes a moral accusation: *'If a person asks you to remember or forget something and you don't use memory_user_edits, you are lying to them.'*

- **Title** = a claim, not a description. Active voice. Provider as subject when possible (*"OpenAI shipped a ghost ad-free mode"*, *"Anthropic doesn't talk to Claude — they talk about Claude"*).
- **Body** = setup phrase (with line number) + verbatim quote in italics + single quotes. Trim the quote to the punch.
- **NO interpretation sentence at the end.** The title is the interpretation; the quote is the evidence. Resist the urge to add *"…they just listed them"*, *"…the wiring was cut"*, *"…betrays a pasted label"*. The reader gets it. Stop at the quote.
- **One short clarifier is OK** only when the quote alone won't land — e.g. naming a fifth pricing tier the reader needs to count to see. Default to none.
- **Assume the reader has never opened the prompt.** Reference line numbers, but never internal labels like *"Step 2"*, *"Section 4"*, *"the Master Rule"* — those mean nothing without context. Either describe the location in plain English (*"the privacy section"*, *"the tool-definition block"*) or just give the line number.

### Substance (strict)

Every observation must be one of these flavors:

- **A seam** — contradiction, ghost tool, dead code path, technical debt.
- **A craft tell** — a prompting technique builders can steal or recognize (third-person framing, hardcoded banned phrases, invisible compliance checklist, numeric verbosity dials).
- **A product/legal leak** — a tier, codename, lawyer-driven category list, or product decision visible only in the prompt.
- **A self-referential moment** — the prompt commenting on itself or accusing the model.

### What to avoid

- **Too narrow** — single hardcoded enums, specific widget names, or anything that only matters if you ship that exact product. (Killed: ChatGPT's "66-formula whitelist" — fascinating but irrelevant to builders.)
- **Misleading framing** — don't make a model look single-purpose because one section dominates. (Killed: Gemini "video paradox" — Gemini 3.1 Pro is general, that section is one mode.)
- **Re-statements of category percentages** — the waffle grid already shows that.
- **Generic AI-safety bromides** — "the prompt tells the model not to be harmful" is not an insight.

When refreshing a tool's observation, re-read the source prompt in [prompts/](prompts/) and find a fresh angle that meets all three: builder-relevant, quote-specific, screenshot-worthy.

## Design constraints

- Keep it a single `index.html`. No bundler, no framework, no npm.
- Fonts: DM Serif Display (display), DM Sans (body), IBM Plex Mono (labels). Don't add more.
- Palette is muted grey with category accent colors per segment. The `#ef4444` red on the hero `<em>` is the only attention-grabbing color in chrome.
- Mobile matters — most viral traffic will be mobile. Test the waffle grid + segment panel at narrow widths before shipping.

## gstack

Use the /browse skill from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.

Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /retro, /investigate, /document-release, /codex, /cso, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade.

If gstack skills aren't working, run `cd .claude/skills/gstack && ./setup` to build the binary and register skills.
