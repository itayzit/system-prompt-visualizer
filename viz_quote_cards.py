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

# ── Card A: Fable 5 vs Opus 5 psychology (diff-card visual language) ──
MONO_A = 'DejaVu Sans Mono'
F_HDR_BG, F_HDR_FG, F_LINE_BG = '#dbeafe', '#1e40af', '#e9f0fc'
O_HDR_BG, O_HDR_FG, O_LINE_BG = '#ffedd5', '#9a3412', '#fdf3e7'

fig = plt.figure(figsize=(15, 7.5), facecolor=BG)
fig.text(0.04, 0.945, "$ diff claude-code/{fable-5, opus-5}.prompt   # behavior sections only",
         fontsize=15, color=GRAY, family=MONO_A)

A_LINES = [
    ('fhdr', '@@ Fable 5 \u2014 coached for autonomy @@'),
    ('fq', '+ "You are operating autonomously. The user is not'),
    ('fq', '+  watching in real time \u2026 asking \u2018Want me to\u2026?\u2019'),
    ('fq', '+  will block the work."'),
    ('fq', '+ "Do not stop because the context or session is long."'),
    ('gap', ''),
    ('ohdr', '@@ Opus 5 \u2014 coached against rumination @@'),
    ('oq', '+ "Don\u2019t add apologies or preambles, don\u2019t be overly'),
    ('oq', '+  self-critical, and don\u2019t ruminate \u2026 or tally past errors."'),
    ('oq', '+ "A follow-up question about your earlier work is not,'),
    ('oq', '+  by itself, a signal that you got something wrong."'),
    ('oq', '+ "Scaling the work down is the user\u2019s call, not yours."'),
]

y = 0.845
LH = 0.0605
for kind, txt in A_LINES:
    if kind == 'gap':
        y -= LH * 0.55
        continue
    bg = {'fhdr': F_HDR_BG, 'fq': F_LINE_BG, 'ohdr': O_HDR_BG, 'oq': O_LINE_BG}[kind]
    fg = {'fhdr': F_HDR_FG, 'fq': DARK, 'ohdr': O_HDR_FG, 'oq': DARK}[kind]
    fig.patches.append(mpatches.Rectangle((0.03, y - 0.012), 0.94, LH * 0.88,
                       transform=fig.transFigure, facecolor=bg, edgecolor='none'))
    fig.text(0.045, y, txt, fontsize=15.5, color=fg, family=MONO_A,
             fontweight='bold' if kind.endswith('hdr') else 'normal', va='center')
    y -= LH

fig.text(0.04, 0.10, "Tool definitions are identical between the two models \u2014 the coaching is the diff.",
         fontsize=13, color=GRAY, style='italic')
fig.text(0.04, 0.058, "\u2014 Claude Code system prompts, captured July 2026 \u00b7 quotes verbatim",
         fontsize=12.5, color=GRAY, style='italic')
fig.text(0.04, 0.022, "Source: asgeirtj/system_prompts_leaks",
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
