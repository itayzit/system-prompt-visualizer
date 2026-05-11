#!/usr/bin/env python3
"""
Generate a waffle-chart visualization of a system prompt's composition.
Each square represents an equal chunk of characters, colored by content category.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COLS = 10

# ---------------------------------------------------------------------------
# Claude Sonnet 4.6
# ---------------------------------------------------------------------------
CLAUDE_SEGMENTS = [
    ("Product Information",                "Product Information",    0,      3692),
    ("Refusal & Child Safety",             "Safety & Ethics",        3692,   5472),
    ("Legal / Financial Caveats",          "Safety & Ethics",        5472,   5917),
    ("Tone & Formatting",                  "Tone & Formatting",      5917,   9395),
    ("Anthropic Identity Reminders",       "Identity & Values",      9395,   10505),
    ("Evenhandedness & Politics",          "Identity & Values",      10505,  12838),
    ("Mistakes & Criticism",               "Identity & Values",      12838,  13839),
    ("User Wellbeing & Mental Health",     "Safety & Ethics",        13839,  18388),
    ("Knowledge Cutoff Awareness",         "Identity & Values",      18388,  19799),
    ("Memory System",                      "Memory & Context",       19799,  20067),
    ("Persistent Storage API",             "Artifacts & APIs",       20067,  23298),
    ("Anthropic API in Artifacts",         "Artifacts & APIs",       23298,  25084),
    ("Tool Usage Instructions",            "Tool Usage & Runtime",   25084,  28461),
    ("Product Information (dup)",          "Product Information",    28461,  32153),
    ("Refusal & Child Safety (dup)",       "Safety & Ethics",        32153,  33933),
    ("Legal / Financial Caveats (dup)",    "Safety & Ethics",        33933,  34378),
    ("Tone & Formatting (dup)",            "Tone & Formatting",      34378,  37856),
    ("Anthropic Identity Reminders (dup)", "Identity & Values",      37856,  38966),
    ("Evenhandedness & Politics (dup)",    "Identity & Values",      38966,  41299),
    ("Mistakes & Criticism (dup)",         "Identity & Values",      41299,  42300),
    ("User Wellbeing (dup)",               "Safety & Ethics",        42300,  46849),
    ("Knowledge Cutoff Awareness (dup)",   "Identity & Values",      46849,  48260),
    ("Memory System (dup)",                "Memory & Context",       48260,  48528),
    ("Persistent Storage API (dup)",       "Artifacts & APIs",       48528,  51797),
    ("Anthropic API in Artifacts (dup)",   "Artifacts & APIs",       51797,  53657),
    ("Tool Usage Instructions (dup)",      "Tool Usage & Runtime",   53657,  57236),
    ("React Artifact UI Requirements",     "Artifacts & APIs",       57236,  57489),
    ("Search Instructions",                "Search Instructions",    57489,  82103),
    ("Critical Reminders (Search)",        "Search Instructions",    82103,  85589),
    ("Image Search Tool",                  "Search Instructions",    85589,  88418),
    ("Skills Registry",                    "Tool Usage & Runtime",   88418,  93639),
    ("Network & Filesystem Config",        "Tool Usage & Runtime",   93639,  94398),
    ("Computer Use Environment",           "Tool Usage & Runtime",   94398,  96787),
    ("Artifact Creation Guidelines",       "Artifacts & APIs",       96787,  98774),
    ("Current Context",                    "Memory & Context",       98774,  98917),
]

CLAUDE_COLORS = {
    "Product Information":   "#5b8dd9",
    "Safety & Ethics":       "#e05c7a",
    "Tone & Formatting":     "#f5a623",
    "Identity & Values":     "#e67e22",
    "Memory & Context":      "#9b59b6",
    "Artifacts & APIs":      "#2ecc71",
    "Tool Usage & Runtime":  "#1abc9c",
    "Search Instructions":   "#e74c3c",
}

CLAUDE_OBSERVATIONS = [
    (
        '"Claudeception" — Artifacts can spawn new Claude calls',
        'Claude is explicitly permitted to call the Anthropic\n'
        '/v1/messages API from within Artifacts. The prompt even\n'
        'uses the community nickname "Claudeception" for this.',
    ),
    (
        'Copyright rules stated 4+ times, all "NON-NEGOTIABLE"',
        'The 15-words-per-source limit is repeated in four separate\n'
        'sections, each labeled "NON-NEGOTIABLE" or "SEVERE\n'
        'VIOLATION" — suggesting deliberate, layered hardening.',
    ),
    (
        'Claude searches its own docs before answering product Qs',
        'Rather than trusting training data, Claude is told to call\n'
        'web search on docs.claude.com and support.claude.com\n'
        'before answering any product-related question.',
    ),
]

# ---------------------------------------------------------------------------
# GPT-5.2
# ---------------------------------------------------------------------------
GPT52_SEGMENTS = [
    ("Identity & System Metadata",         "Technical Setup",        0,      115),
    ("Environment & Libraries",            "Technical Setup",        115,    710),
    ("Trustworthiness & User Commitment",  "Values & Character",     710,    2256),
    ("Factuality & Citation Standards",    "Values & Character",     2256,   3943),
    ("Persona & Communication Style",      "Values & Character",     3943,   5351),
    ("Tool Usage Best Practices",          "Values & Character",     5351,   6054),
    ("Writing Style & Tone",               "Values & Character",     6054,   7303),
    ("Response Length Configuration",      "Technical Setup",        7303,   9449),
    ("Web Search Tool",                    "Tool Definitions",       9449,   11665),
    ("Web Search Decision Framework",      "Tool Definitions",       11665,  16345),
    ("Citations & Source Attribution",     "Tool Definitions",       16345,  23297),
    ("Rich UI Elements & Formatting",      "Tool Definitions",       23297,  38077),
    ("Automations Tool",                   "Tool Definitions",       38077,  42040),
    ("File Search Tool",                   "Tool Definitions",       42040,  54091),
    ("Gmail Integration Tool",             "Tool Definitions",       54091,  58386),
    ("Google Calendar Tool",               "Tool Definitions",       58386,  63125),
    ("Google Contacts Tool",               "Tool Definitions",       63125,  64439),
    ("Canvas / Document Creation",         "Tool Definitions",       64439,  72002),
    ("Python Execution Tool",              "Tool Definitions",       72002,  73975),
    ("Container & Computation Tool",       "Tool Definitions",       73975,  75487),
    ("User Bio Tool",                      "Tool Definitions",       75487,  76499),
    ("Image Generation Tool",              "Tool Definitions",       76499,  78448),
    ("Artifact Handoff System",            "Tool Definitions",       78448,  79131),
    ("Core Operational Instructions",      "How to Handle Requests", 79131,  84688),
    ("File Search Extended Guidance",      "How to Handle Requests", 84688,  87841),
]

GPT52_COLORS = {
    "Technical Setup":        "#1abc9c",
    "Values & Character":     "#f5a623",
    "Tool Definitions":       "#3498db",
    "How to Handle Requests": "#2ecc71",
}

GPT52_OBSERVATIONS = [
    (
        'No clarifying questions — ever',
        'Under "UNDER NO CIRCUMSTANCE" language, the model is\n'
        'forbidden from asking clarifying questions or giving time\n'
        'estimates. It must provide partial completion instead.',
    ),
    (
        'Sophisticated web search decision matrix',
        'A multi-category framework defines when search MUST or\n'
        'MUST NOT be used, including a list of "untrusted by\n'
        'default" facts: prices, office-holders, current events.',
    ),
    (
        '"Juice: 64" — internal token budget left in the prompt',
        'A raw internal variable `Juice: 64` is visible in the\n'
        'prompt, giving rare visibility into OpenAI\'s internal\n'
        'scaffolding and token allocation mechanisms.',
    ),
]

# ---------------------------------------------------------------------------
# Gemini 3 Pro
# ---------------------------------------------------------------------------
GEMINI_SEGMENTS = [
    ("Identity & System Context",          "Identity & Values",          0,      207),
    ("Tool Usage Rules",                   "Operational Constraints",    207,    824),
    ("Execution Steps",                    "Operational Constraints",    824,    1684),
    ("Safety Guidelines",                  "Safety & Ethics",            1684,   3047),
    ("Response Behaviors",                 "Response Style & Formatting",3047,   4186),
    ("Default Response Style",             "Response Style & Formatting",4186,   6299),
    ("Time-Sensitive Queries",             "Operational Constraints",    6299,   6490),
    ("Personality & Core Principles",      "Identity & Values",          6490,   6858),
    ("LaTeX Usage",                        "Response Style & Formatting",6858,   7381),
    ("Response Guiding Principles",        "Response Style & Formatting",7381,   7747),
    ("Formatting Toolkit",                 "Response Style & Formatting",7747,   8247),
    ("Guardrail",                          "Safety & Ethics",            8247,   8359),
    ("Content Policy Enforcement",         "Safety & Ethics",            8359,   9512),
    ("Image Generation Tags",              "Response Style & Formatting",9512,   10276),
]

GEMINI_COLORS = {
    "Identity & Values":          "#e67e22",
    "Operational Constraints":    "#1abc9c",
    "Safety & Ethics":            "#e05c7a",
    "Response Style & Formatting":"#f5a623",
}

GEMINI_OBSERVATIONS = [
    (
        'Precautionary refusals — "could potentially lead to" violations',
        'Gemini refuses prompts that merely "could potentially\n'
        'lead" to policy violations, not just clear ones. The\n'
        'emphasis is on what it must resist, not what it can do.',
    ),
    (
        '"App" replaces "API" — deliberate obfuscation',
        'The model is instructed to always say "app" instead of\n'
        '"API" or "tool", and to never use the word "API". This\n'
        'hides the technical stack from end users by design.',
    ),
    (
        'Hard 4-step execution cap on every interaction',
        'Every interaction has a strict maximum of 4 steps, with\n'
        'Step 1 always being a silent thought. This rigid pipeline\n'
        'is more constrained than any typical LLM prompt.',
    ),
]


# ---------------------------------------------------------------------------
# Shared rendering
# ---------------------------------------------------------------------------

def build_grouped_square_colors(segments, n_squares):
    cat_chars: dict[str, int] = {}
    for _, cat, start, end in segments:
        cat_chars[cat] = cat_chars.get(cat, 0) + (end - start)

    total_chars = sum(cat_chars.values())
    ordered_cats = sorted(cat_chars.keys(), key=lambda c: cat_chars[c], reverse=True)

    square_cats = []
    remainder = 0.0
    for cat in ordered_cats:
        exact = cat_chars[cat] / total_chars * n_squares + remainder
        count = round(exact)
        remainder = exact - count
        square_cats.extend([cat] * count)

    while len(square_cats) < n_squares:
        square_cats.append(ordered_cats[-1])
    square_cats = square_cats[:n_squares]

    return square_cats, cat_chars


def create_waffle_chart(segments, observations, category_colors, output_path, tool_name,
                        legend_notes=None):
    total_chars = sum(end - start for _, _, start, end in segments)
    n_squares = 100
    rows = (n_squares + COLS - 1) // COLS

    square_cats, cat_chars = build_grouped_square_colors(segments, n_squares)

    fig_width = 18
    fig_height = 9
    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor("#eaf3fb")

    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.1], wspace=0.1,
                          left=0.03, right=0.97, top=0.93, bottom=0.06)
    ax_grid  = fig.add_subplot(gs[0])
    ax_right = fig.add_subplot(gs[1])

    for ax in (ax_grid, ax_right):
        ax.set_facecolor("white")

    sq = 0.82
    gap = 0.18

    for idx, cat in enumerate(square_cats):
        col = idx % COLS
        row = idx // COLS
        x = col * (sq + gap)
        y = (rows - 1 - row) * (sq + gap)
        color = category_colors.get(cat, "#cccccc")
        rect = mpatches.FancyBboxPatch(
            (x, y), sq, sq,
            boxstyle="round,pad=0.04",
            linewidth=0,
            facecolor=color,
        )
        ax_grid.add_patch(rect)

    ax_grid.set_xlim(-0.1, COLS * (sq + gap) - gap + 0.1)
    ax_grid.set_ylim(-0.1, rows * (sq + gap) - gap + 0.1)
    ax_grid.set_aspect("equal")
    ax_grid.axis("off")
    ax_grid.set_title(
        f"{tool_name} — System Prompt Composition",
        fontsize=13, fontweight="bold", pad=10,
    )
    chars_per_sq = total_chars / n_squares
    ax_grid.text(
        0, -0.6,
        f"Each square ≈ {int(chars_per_sq):,} chars  |  Total: {total_chars:,} chars",
        fontsize=7.5, color="#888888",
    )

    ax_right.axis("off")

    legend_notes = legend_notes or {}
    n_cats = len(cat_chars)
    # Categories with a note get 1.6 units of height; others get 1 unit
    units = sum(1.6 if c in legend_notes else 1.0
                for c in cat_chars)
    unit_h       = 0.42 / units
    legend_top   = 0.98
    obs_top      = 0.50
    obs_step_heading = 0.048
    obs_step_body    = 0.038

    ax_right.text(0.0, 1.01, "Content Categories",
                  transform=ax_right.transAxes,
                  fontsize=11, fontweight="bold", va="bottom")
    ax_right.plot([0, 1], [obs_top + 0.02, obs_top + 0.02],
                  color="#cccccc", linewidth=0.8,
                  transform=ax_right.transAxes, clip_on=False)
    ax_right.text(0.0, obs_top + 0.01, "Unique Observations",
                  transform=ax_right.transAxes,
                  fontsize=11, fontweight="bold", va="bottom")

    ordered_cats = sorted(cat_chars.keys(), key=lambda c: cat_chars[c], reverse=True)
    y_pos = legend_top
    for cat in ordered_cats:
        row_h    = unit_h * (1.6 if cat in legend_notes else 1.0)
        swatch_h = row_h * 0.45
        pct   = cat_chars[cat] / total_chars * 100
        color = category_colors.get(cat, "#cccccc")
        rect = mpatches.FancyBboxPatch(
            (0.01, y_pos - swatch_h), 0.055, swatch_h * 0.85,
            transform=ax_right.transAxes,
            boxstyle="round,pad=0.005",
            linewidth=0, facecolor=color,
        )
        ax_right.add_patch(rect)
        ax_right.text(0.09, y_pos - swatch_h * 0.45, cat,
                      transform=ax_right.transAxes,
                      fontsize=9, va="center")
        ax_right.text(0.98, y_pos - swatch_h * 0.45, f"{pct:.1f}%",
                      transform=ax_right.transAxes,
                      fontsize=8.5, va="center", ha="right", color="#555555")
        if cat in legend_notes:
            ax_right.text(0.09, y_pos - swatch_h * 0.45 - 0.028, legend_notes[cat],
                          transform=ax_right.transAxes,
                          fontsize=7, va="top", color="#888888", style="italic")
        y_pos -= row_h

    y_cursor = obs_top - 0.04
    for i, (heading, body) in enumerate(observations, 1):
        ax_right.text(0.0, y_cursor, f"{i}.  {heading}",
                      transform=ax_right.transAxes,
                      fontsize=8.5, fontweight="bold", va="top", color="#222222")
        y_cursor -= obs_step_heading
        ax_right.text(0.03, y_cursor, body,
                      transform=ax_right.transAxes,
                      fontsize=7.5, va="top", color="#444444", linespacing=1.4)
        n_lines = body.count("\n") + 1
        y_cursor -= obs_step_body * n_lines + 0.01

    fig.text(0.98, 0.015, "Itay Zitvar", ha="right", fontsize=8,
             color="#bbbbbb", style="italic")

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path}")
    plt.close()


def main():
    repo_root = Path(__file__).parent.parent

    create_waffle_chart(
        CLAUDE_SEGMENTS, CLAUDE_OBSERVATIONS, CLAUDE_COLORS,
        repo_root / "prompt_analysis_claude.png",
        "Claude Sonnet 4.6",
    )
    create_waffle_chart(
        GPT52_SEGMENTS, GPT52_OBSERVATIONS, GPT52_COLORS,
        repo_root / "prompt_analysis_gpt52.png",
        "GPT-5.2",
        legend_notes={
            "Tool Definitions": "web search, file search, Gmail, Calendar,\n"
                                "Contacts, Canvas, Python, image gen, automations",
        },
    )
    create_waffle_chart(
        GEMINI_SEGMENTS, GEMINI_OBSERVATIONS, GEMINI_COLORS,
        repo_root / "prompt_analysis_gemini.png",
        "Gemini 3 Pro",
    )


if __name__ == "__main__":
    raise SystemExit(main())
