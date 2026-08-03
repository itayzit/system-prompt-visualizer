# Treemap of Claude Code's system prompt composition.
# Regenerate: uv run --with matplotlib --with squarify python3 viz_claude_code.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import squarify
from collections import defaultdict

CATS = {
    'tools':     ('Tool definitions', '#3b82f6'),
    'process':   ('Process & method', '#f97316'),
    'memory':    ('Memory',           '#a855f7'),
    'identity':  ('Identity & env',   '#10b981'),
    'safety':    ('Safety & policy',  '#ef4444'),
}

# (label, tokens, category, subtitle) — tiktoken cl100k_base on the real Opus 4.8 prompt.
# Read / Edit / Write kept consecutive so they render adjacent.
# subtitle='' for self-explanatory blocks.
SEGMENTS = [
    ('Workflow tool',              4775, 'tools',   'orchestrates fleets of subagents'),
    ('Tool &\nskill catalog', 1660, 'tools', 'names of tools loadable on demand'),
    ('AskUserQuestion',            1237, 'tools',   'multiple-choice questions to user'),
    ('Agent tool',                 1157, 'tools',   'spawns a single subagent'),
    ('ScheduleWakeup',              898, 'tools',   'timers to resume work later'),
    ('Browser\nautomation',         694, 'process', 'Chrome control rules'),
    ('Bash',                        659, 'tools',   'runs shell commands'),
    ('Read',                        460, 'tools',   ''),
    ('Edit',                        269, 'tools',   ''),
    ('Write',                       177, 'tools',   ''),
    ('Memory\nsystem',              476, 'memory',  'notes kept between sessions'),
    ('Session\nguidance',           417, 'process', 'rules for this session'),
    ('Skill',                       402, 'tools',   'runs /slash-commands'),
    ('SendUserFile',                361, 'tools',   'delivers files to user'),
    ('ToolSearch',                  358, 'tools',   'loads deferred tools'),
    ('Identity\n& env',             393, 'identity','who am I, what machine'),
    ('Runtime\nrules',              209, 'process', ''),
    ('Confirm risky\nactions',      180, 'safety',  ''),
]

total = sum(t for _, t, _, _ in SEGMENTS)
cat_tot = defaultdict(int)
for _, t, c, _ in SEGMENTS:
    cat_tot[c] += t
print(f"Total: {total:,}")
for c, (lbl, _) in CATS.items():
    print(f"  {lbl:<18} {cat_tot[c]:>6,}  {cat_tot[c]/total*100:5.1f}%")

DPI = 150
fig = plt.figure(figsize=(15, 9.4), facecolor='#eef0f4')
ax = fig.add_axes([0.03, 0.04, 0.94, 0.78])
ax.set_facecolor('#eef0f4')

sizes = [t for _, t, _, _ in SEGMENTS]
colors = [CATS[c][1] for _, _, c, _ in SEGMENTS]
rects = squarify.squarify(squarify.normalize_sizes(sizes, 100, 100), 0, 0, 100, 100)

fig_w_in, fig_h_in = 15 * 0.94, 9.4 * 0.78
px_per_x = fig_w_in * DPI / 100.0
px_per_y = fig_h_in * DPI / 100.0
PPP = DPI / 72.0  # px per point

def fit_font(txt, dx, dy, max_pt=21.0):
    lines = txt.split('\n')
    longest = max(len(s) for s in lines)
    nlines = len(lines)
    cell_w_px = dx * px_per_x
    cell_h_px = dy * px_per_y
    fs_w = 0.90 * cell_w_px / (longest * 0.60 * PPP)
    fs_h = 0.80 * cell_h_px / (nlines * 1.32 * PPP)
    return max(5.5, min(max_pt, fs_w, fs_h))

for (label, tok, cat, sub), r, col in zip(SEGMENTS, rects, colors):
    x, y, dx, dy = r['x'], r['y'], r['dx'], r['dy']
    ax.add_patch(plt.Rectangle((x, y), dx, dy, facecolor=col, edgecolor='#eef0f4',
                               linewidth=2.5, alpha=0.94))
    area = dx * dy
    pct = tok / total * 100

    title = f"{label}\n{pct:.0f}%"
    # canvas is 100x100 = 10,000 area units; tokens only on genuinely big cells
    show_tok = area > 400
    # decide whether the subtitle fits: need enough vertical room beyond the title
    title_fs = fit_font(title, dx, dy * (0.62 if sub else 1.0))
    show_sub = bool(sub) and area > 2.2
    if show_sub:
        sub_fs = min(title_fs * 0.62, fit_font(sub, dx, dy * 0.30, max_pt=11.0))
        if sub_fs < 5.5:
            show_sub = False
    tok_fs = min(title_fs * 0.52, 12.0)

    if show_sub:
        ax.text(x + dx/2, y + dy*0.42, title, ha='center', va='center',
                fontsize=title_fs, color='white', fontweight='bold', linespacing=1.1)
        ax.text(x + dx/2, y + dy*0.80, sub, ha='center', va='center',
                fontsize=sub_fs, color='white', alpha=0.75, style='italic', linespacing=1.05)
    else:
        fs = fit_font(title, dx, dy)
        ax.text(x + dx/2, y + dy/2, title, ha='center', va='center',
                fontsize=fs, color='white', fontweight='bold', linespacing=1.1)
    if show_tok:
        # small muted count tucked in the bottom-right corner, out of everything's way
        ax.text(x + dx - dx*0.03, y + dy - dy*0.035, f"{tok:,} tokens",
                ha='right', va='bottom', fontsize=tok_fs,
                color='white', alpha=0.55, linespacing=1.0)

ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.invert_yaxis(); ax.axis('off')

fig.text(0.03, 0.955, "What's inside Claude Code's system prompt",
         fontsize=27, color='#111111', fontweight='bold')
fig.text(0.03, 0.908, "Opus 4.8  ·  captured May 2026  ·  14,787 tokens  ·  blocks sized by tokens",
         fontsize=13.5, color='#5a5f68')

lx = 0.03
for c, (lbl, col) in CATS.items():
    pct = cat_tot[c] / total * 100
    fig.patches.append(mpatches.Rectangle((lx, 0.852), 0.016, 0.016,
                       transform=fig.transFigure, facecolor=col, edgecolor='none'))
    t = f"{lbl} {pct:.0f}%"
    fig.text(lx + 0.022, 0.853, t, fontsize=12, color='#333940', fontweight='bold')
    lx += 0.022 + 0.0072 * len(t) + 0.018

fig.text(0.03, 0.012, "Source: leaked Claude Code system prompt (asgeirtj/system_prompts_leaks) · tokens via tiktoken cl100k_base",
         fontsize=9, color='#8a8f98')

out = 'examples/claude-code-treemap.png'
plt.savefig(out, dpi=DPI, facecolor='#eef0f4', bbox_inches='tight')
print(f"Saved → {out}")
