# Quote cards for the Claude Code X thread — same visual language as the treemaps.
# Regenerate: uv run --with matplotlib python3 viz_quote_cards.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BG = '#eef0f4'
DARK = '#111111'
GRAY = '#5a5f68'
LIGHT = '#8a8f98'
BLUE = '#3b82f6'
ORANGE = '#f97316'
RED = '#ef4444'

# ── Card A: Fable 5 vs Opus 5 psychology ──────────────────────────────
fig = plt.figure(figsize=(15, 8.4), facecolor=BG)

fig.text(0.04, 0.93, "Same tools. Different coaching.", fontsize=27, color=DARK, fontweight='bold')
fig.text(0.04, 0.875, "Claude Code ships byte-identical tool definitions to both models — the only per-model difference is ~1,500 tokens of behavioral prose.",
         fontsize=12.5, color=GRAY)

cols = [
    (0.04, BLUE, 'FABLE 5', 'coached for autonomy', [
        '“You are operating autonomously. The user is not\nwatching in real time … asking ‘Want me to…?’ or\n‘Shall I…?’ will block the work.”',
        '“Before ending your turn, check your last paragraph.\nIf it is … a promise about work you have not done\n(‘I’ll…’, ‘let me know when…’), do that work now.”',
        '“Do not stop because the context or session is long.”',
    ]),
    (0.53, ORANGE, 'OPUS 5', 'coached against rumination', [
        '“Don’t add apologies or preambles, don’t be overly\nself-critical, and don’t ruminate … or tally past errors.”',
        '“A follow-up question about your earlier work is not,\nby itself, a signal that you got something wrong.”',
        '“Scaling the work down is the user’s call, not yours.”',
    ]),
]

for x0, color, name, tagline, quotes in cols:
    fig.patches.append(mpatches.Rectangle((x0, 0.775), 0.017, 0.028,
                       transform=fig.transFigure, facecolor=color, edgecolor='none'))
    fig.text(x0 + 0.026, 0.778, name, fontsize=17, color=DARK, fontweight='bold')
    fig.text(x0 + 0.026 + 0.012*len(name), 0.7795, f'— {tagline}', fontsize=13, color=GRAY, style='italic')
    for q, y in zip(quotes, [0.68, 0.47, 0.26]):
        fig.text(x0, y, q, fontsize=13.5, color=DARK, va='top', linespacing=1.45)

fig.text(0.04, 0.035, "Source: leaked Claude Code system prompts, July 2026 (asgeirtj/system_prompts_leaks) · quotes verbatim, trimmed with ellipses",
         fontsize=9.5, color=LIGHT)

plt.savefig('examples/claude-code-psychology-card.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close(fig)
print("Saved → examples/claude-code-psychology-card.png")

# ── Card B: the Mythos paragraph ──────────────────────────────────────
fig = plt.figure(figsize=(15, 7.2), facecolor=BG)

fig.text(0.04, 0.90, "Buried at the end of Fable 5's prompt:", fontsize=15, color=GRAY)

lines = [
    ('“Claude Fable 5 and Claude Mythos 5 share the same', DARK),
    ('underlying model. Claude Fable 5 is our most intelligent', DARK),
    ('generally available model, and includes additional safety', DARK),
    ('measures for dual-use capabilities, while Claude Mythos 5', DARK),
    ('is available without those measures', RED),
    ('to only approved organizations.”', RED),
]
y = 0.76
for txt, col in lines:
    fig.text(0.04, y, txt, fontsize=23, color=col, fontweight='bold', va='top', linespacing=1.3)
    y -= 0.107

fig.text(0.04, 0.075, "— Claude Code system prompt (Fable 5), captured July 2026",
         fontsize=13, color=GRAY, style='italic')
fig.text(0.04, 0.025, "Source: asgeirtj/system_prompts_leaks · quote verbatim",
         fontsize=9.5, color=LIGHT)

plt.savefig('examples/claude-code-mythos-card.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close(fig)
print("Saved → examples/claude-code-mythos-card.png")


# ── Card C: cache-billing awareness ───────────────────────────────────
fig = plt.figure(figsize=(15, 7.2), facecolor=BG)

fig.text(0.04, 0.90, "From the section teaching Claude to schedule its own wake-ups:", fontsize=15, color=GRAY)

lines = [
    ('\u201cThis session\u2019s requests use a 1-hour Anthropic', DARK),
    ('prompt-cache TTL \u2026 scheduling extra wakeups just to', DARK),
    ('keep the cache warm is pure waste \u2014 never do that.', DARK),
    ('If the session enters usage overage, later', RED),
    ('requests drop to the 5-minute TTL.\u201d', RED),
]
y = 0.76
for txt, col in lines:
    fig.text(0.04, y, txt, fontsize=23, color=col, fontweight='bold', va='top', linespacing=1.3)
    y -= 0.107

fig.text(0.04, 0.16, "The model is told your billing state. It schedules its own sleep around your invoice.",
         fontsize=14, color=GRAY, style='italic')
fig.text(0.04, 0.075, "\u2014 Claude Code system prompt (Fable 5), ScheduleWakeup tool, captured July 2026",
         fontsize=13, color=GRAY, style='italic')
fig.text(0.04, 0.025, "Source: asgeirtj/system_prompts_leaks \u00b7 quote verbatim",
         fontsize=9.5, color=LIGHT)

plt.savefig('examples/claude-code-cache-card.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close(fig)
print("Saved → examples/claude-code-cache-card.png")


# ── Card D: the diff view (for thread part 2) ─────────────────────────
MONO = 'DejaVu Sans Mono'
FOLD_BG, FOLD_FG = '#dbeafe', '#1e40af'
ADD_BG, ADD_FG = '#dcfce7', '#15803d'

fig = plt.figure(figsize=(15, 7.4), facecolor=BG)
fig.text(0.04, 0.945, "$ diff claude-code/{opus-4.8, fable-5, opus-5}.prompt",
         fontsize=15, color=GRAY, family=MONO)

LINES = [
    ('fold', '@@ ~29,500 tokens of tool definitions \u2014 identical @@'),
    ('gap', ''),
    ('head', '+ Fable 5 only'),
    ('add',  '+   an autonomy doctrine                    (+300 tokens)'),
    ('add',  '+   expanded communication rules             (872 tokens)'),
    ('add',  '+   the Claude Mythos 5 identity paragraph'),
    ('gap', ''),
    ('head', '+ Opus 5 only'),
    ('add',  '+   ## Delivering work                       (394 tokens)'),
    ('add',  '+   ## Corrections                           (296 tokens)'),
    ('gap', ''),
    ('head', '+ Both Claude 5 models \u2014 missing from Opus 4.8'),
    ('add',  '+   EndConversation, a tool to end the chat  (904 tokens)'),
]

y = 0.855
LH = 0.057
for kind, txt in LINES:
    if kind == 'gap':
        y -= LH * 0.55
        continue
    bg = FOLD_BG if kind == 'fold' else ADD_BG
    fg = FOLD_FG if kind == 'fold' else (DARK if kind == 'add' else ADD_FG)
    fig.patches.append(mpatches.Rectangle((0.03, y - 0.012), 0.94, LH * 0.88,
                       transform=fig.transFigure, facecolor=bg, edgecolor='none'))
    fig.text(0.045, y, txt, fontsize=15.5, color=fg, family=MONO,
             fontweight='bold' if kind in ('head', 'fold') else 'normal', va='center')
    y -= LH

fig.text(0.04, 0.075, "\u2014 Claude Code system prompts, captured July 2026 \u00b7 section names & token counts from the prompts",
         fontsize=12.5, color=GRAY, style='italic')
fig.text(0.04, 0.03, "Source: asgeirtj/system_prompts_leaks",
         fontsize=9.5, color=LIGHT)

plt.savefig('examples/claude-code-diff-card.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close(fig)
print("Saved → examples/claude-code-diff-card.png")
