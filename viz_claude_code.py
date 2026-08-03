# Treemaps of Claude Code's system prompt composition — one per model.
# Parses the leaked prompts in prompts/ directly, so numbers are always honest.
# Regenerate: uv run --with matplotlib --with squarify --with tiktoken python3 viz_claude_code.py
import re
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import squarify
import tiktoken

ENC = tiktoken.get_encoding("cl100k_base")
toks = lambda s: len(ENC.encode(s))

CATS = {
    'tools':     ('Tool definitions', '#3b82f6'),
    'process':   ('Process & method', '#f97316'),
    'memory':    ('Memory',           '#a855f7'),
    'identity':  ('Identity & env',   '#10b981'),
    'safety':    ('Safety & policy',  '#ef4444'),
}

MODELS = [
    ('opus-4.8', 'Opus 4.8',  'prompts/claude-code-opus-4.8.txt', 'July 2026'),
    ('fable-5',  'Fable 5',   'prompts/claude-code-fable-5.txt',  'July 2026'),
    ('opus-5',   'Opus 5',    'prompts/claude-code-opus-5.txt',   'July 2026'),
]

# section name -> (cell label, category, subtitle). Sections sharing a label merge.
GROUPS = {
    'Workflow':          ('Workflow tool', 'tools', 'orchestrates fleets of subagents'),
    'DesignSync':        ('DesignSync', 'tools', 'syncs design systems with claude.ai'),
    'Artifact':          ('Artifact', 'tools', 'publishes web pages to claude.ai'),
    'TaskCreate':        ('Task tracking\n(6 tools)', 'tools', 'shared to-do list for agents'),
    'TaskGet':           ('Task tracking\n(6 tools)', 'tools', ''),
    'TaskList':          ('Task tracking\n(6 tools)', 'tools', ''),
    'TaskOutput':        ('Task tracking\n(6 tools)', 'tools', ''),
    'TaskStop':          ('Task tracking\n(6 tools)', 'tools', ''),
    'TaskUpdate':        ('Task tracking\n(6 tools)', 'tools', ''),
    'Monitor':           ('Monitor', 'tools', 'watches long-running commands'),
    'EnterPlanMode':     ('Plan mode\n(2 tools)', 'tools', 'propose before touching code'),
    'ExitPlanMode':      ('Plan mode\n(2 tools)', 'tools', ''),
    'EnterWorktree':     ('Worktrees\n(2 tools)', 'tools', 'isolated git sandboxes'),
    'ExitWorktree':      ('Worktrees\n(2 tools)', 'tools', ''),
    'AskUserQuestion':   ('AskUserQuestion', 'tools', 'multiple-choice questions to user'),
    'CronCreate':        ('Cron jobs\n(3 tools)', 'tools', 'scheduled recurring runs'),
    'CronDelete':        ('Cron jobs\n(3 tools)', 'tools', ''),
    'CronList':          ('Cron jobs\n(3 tools)', 'tools', ''),
    'Read':              ('File tools\n(4 tools)', 'tools', 'Read · Edit · Write · Notebook'),
    'Edit':              ('File tools\n(4 tools)', 'tools', ''),
    'Write':             ('File tools\n(4 tools)', 'tools', ''),
    'NotebookEdit':      ('File tools\n(4 tools)', 'tools', ''),
    'ScheduleWakeup':    ('ScheduleWakeup', 'tools', 'timers to resume work later'),
    'EndConversation':   ('EndConversation', 'tools', 'lets Claude end the chat'),
    'Bash':              ('Bash', 'tools', 'runs shell commands'),
    'Agent':             ('Agent tool', 'tools', 'spawns subagents'),
    '__agents_roster__': ('Agent tool', 'tools', ''),
    'PushNotification':  ('Messaging\n(3 tools)', 'tools', 'pings users, agents & sessions'),
    'RemoteTrigger':     ('Messaging\n(3 tools)', 'tools', ''),
    'SendMessage':       ('Messaging\n(3 tools)', 'tools', ''),
    'WebFetch':          ('Web fetch\n& search', 'tools', ''),
    'WebSearch':         ('Web fetch\n& search', 'tools', ''),
    'ReportFindings':    ('ReportFindings', 'tools', 'posts code-review results'),
    'Skill':             ('Skills\n(/commands)', 'tools', 'catalog + how to run them'),
    '__skills_catalog__':('Skills\n(/commands)', 'tools', ''),
    'Communicating with the user': ('Communication\nrules', 'process', 'how to report to the user'),
    'Delivering work':   ('Delivering work\n& corrections', 'process', 'scope, ambiguity, self-correction'),
    'Corrections':       ('Delivering work\n& corrections', 'process', ''),
    'Harness':           ('Runtime\nrules', 'process', ''),
    'Session-specific guidance': ('Runtime\nrules', 'process', ''),
    'Context management':('Runtime\nrules', 'process', ''),
    'Scratchpad Directory': ('Runtime\nrules', 'process', ''),
    'Memory':            ('Memory\nsystem', 'memory', 'notes kept between sessions'),
    '__head__':          ('Identity &\nsession context', 'identity', 'who am I, what repo'),
    'Environment':       ('Identity &\nsession context', 'identity', ''),
    'gitStatus':         ('Identity &\nsession context', 'identity', ''),
    'claudeMd':          ('Identity &\nsession context', 'identity', ''),
    '__date_line__':     ('Identity &\nsession context', 'identity', ''),
    '__safety__':        ('Safety rules', 'safety', ''),
}

SAFETY_PARAS = [
    'IMPORTANT: Assist with authorized security testing',
    'For actions that are hard to reverse',
]


def extract_paragraph(text, start_marker):
    """Remove and return the paragraph beginning with start_marker."""
    i = text.find(start_marker)
    if i < 0:
        return text, ''
    j = text.find('\n\n', i)
    if j < 0:
        j = len(text)
    return text[:i] + text[j:], text[i:j]


def parse(path):
    raw = open(path).read()
    total = toks(raw)

    # pull the two safety paragraphs out of wherever they live
    safety_text = ''
    for marker in SAFETY_PARAS:
        raw, para = extract_paragraph(raw, marker)
        safety_text += para + '\n\n'

    # split on ## headers
    sections = []
    cur_name, cur = '__head__', []
    for line in raw.split('\n'):
        m = re.match(r'^## (.+)', line)
        if m:
            sections.append((cur_name, '\n'.join(cur)))
            cur_name, cur = m.group(1).strip().strip('`'), [line]
        else:
            cur.append(line)
    sections.append((cur_name, '\n'.join(cur)))

    # the trailing context block is captured under '## currentDate';
    # split out the agents roster and skills catalog inside it
    out = []
    for name, txt in sections:
        if name == 'currentDate':
            a = txt.find('# Agents')
            s = txt.find('# Skills')
            date_part = txt[:a if a >= 0 else (s if s >= 0 else len(txt))]
            out.append(('__date_line__', date_part))
            if a >= 0:
                out.append(('__agents_roster__', txt[a:s if s >= 0 else len(txt)]))
            if s >= 0:
                out.append(('__skills_catalog__', txt[s:]))
        else:
            out.append((name, txt))
    out.append(('__safety__', safety_text))

    # aggregate into cells
    cells = {}
    unmatched = 0
    for name, txt in out:
        t = toks(txt)
        if name not in GROUPS:
            unmatched += t
            if t > 40:
                print(f"  !! unmapped section: {name} ({t} tk)")
            continue
        label, cat, sub = GROUPS[name]
        if label not in cells:
            cells[label] = {'tokens': 0, 'cat': cat, 'sub': sub}
        cells[label]['tokens'] += t
        if sub and not cells[label]['sub']:
            cells[label]['sub'] = sub

    segs = [(lbl, d['tokens'], d['cat'], d['sub']) for lbl, d in cells.items()]
    segs.sort(key=lambda s: -s[1])
    ssum = sum(t for _, t, _, _ in segs)
    drift = total - ssum - unmatched
    assert abs(drift) < total * 0.02, f"{path}: drift {drift} tokens"
    return segs, total


def render(slug, model_name, segs, total, captured, cats=None):
    cats = cats or CATS
    cat_tot = defaultdict(int)
    for _, t, c, _ in segs:
        cat_tot[c] += t

    DPI = 150
    fig = plt.figure(figsize=(15, 9.4), facecolor='#eef0f4')
    ax = fig.add_axes([0.03, 0.04, 0.94, 0.78])
    ax.set_facecolor('#eef0f4')

    sizes = [t for _, t, _, _ in segs]
    colors = [cats[c][1] for _, _, c, _ in segs]
    rects = squarify.squarify(squarify.normalize_sizes(sizes, 100, 100), 0, 0, 100, 100)

    fig_w_in, fig_h_in = 15 * 0.94, 9.4 * 0.78
    px_per_x = fig_w_in * DPI / 100.0
    px_per_y = fig_h_in * DPI / 100.0
    PPP = DPI / 72.0

    def fit_font(txt, dx, dy, max_pt=21.0):
        lines = txt.split('\n')
        longest = max(len(s) for s in lines)
        nlines = len(lines)
        fs_w = 0.90 * dx * px_per_x / (longest * 0.60 * PPP)
        fs_h = 0.80 * dy * px_per_y / (nlines * 1.32 * PPP)
        return max(5.5, min(max_pt, fs_w, fs_h))

    for (label, tok, cat, sub), r, col in zip(segs, rects, colors):
        x, y, dx, dy = r['x'], r['y'], r['dx'], r['dy']
        ax.add_patch(plt.Rectangle((x, y), dx, dy, facecolor=col, edgecolor='#eef0f4',
                                   linewidth=2.5, alpha=0.94))
        area = dx * dy
        pct = tok / total * 100
        title = f"{label}\n{pct:.0f}%"
        show_tok = area > 400
        title_fs = fit_font(title, dx, dy * (0.62 if sub else 1.0))
        show_sub = bool(sub) and area > 220
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
            ax.text(x + dx - dx*0.03, y + dy - dy*0.035, f"{tok:,} tokens",
                    ha='right', va='bottom', fontsize=tok_fs,
                    color='white', alpha=0.55, linespacing=1.0)

    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.invert_yaxis(); ax.axis('off')

    fig.text(0.03, 0.955, f"What's inside Claude Code's system prompt — {model_name}",
             fontsize=25, color='#111111', fontweight='bold')
    fig.text(0.03, 0.908, f"captured {captured}  ·  {total:,} tokens  ·  blocks sized by tokens",
             fontsize=13.5, color='#5a5f68')

    lx = 0.03
    compact = len(cats) > 5
    leg_fs = 10.5 if compact else 12
    leg_adv = 0.0063 if compact else 0.0072
    for c, (lbl, col) in cats.items():
        pct = cat_tot[c] / total * 100
        fig.patches.append(mpatches.Rectangle((lx, 0.852), 0.016, 0.016,
                           transform=fig.transFigure, facecolor=col, edgecolor='none'))
        t = f"{lbl} {pct:.0f}%"
        fig.text(lx + 0.022, 0.853, t, fontsize=leg_fs, color='#333940', fontweight='bold')
        lx += 0.022 + leg_adv * len(t) + 0.014

    fig.text(0.03, 0.012, "Source: leaked Claude Code system prompt (asgeirtj/system_prompts_leaks) · tokens via tiktoken cl100k_base",
             fontsize=9, color='#8a8f98')

    out = f'examples/claude-code-{slug}-treemap.png'
    plt.savefig(out, dpi=DPI, facecolor='#eef0f4', bbox_inches='tight')
    plt.close(fig)
    return out


for slug, model_name, path, captured in MODELS:
    print(f"\n=== {model_name} ===")
    segs, total = parse(path)
    cat_tot = defaultdict(int)
    for _, t, c, _ in segs:
        cat_tot[c] += t
    print(f"Total: {total:,}")
    for c, (lbl, _) in CATS.items():
        print(f"  {lbl:<18} {cat_tot[c]:>6,}  {cat_tot[c]/total*100:5.1f}%")
    out = render(slug, model_name, segs, total, captured)
    print(f"Saved → {out}")


# ── Alt-color variant: split "tools" into functional families (Fable 5 only) ──
ALT_CATS = {
    'orch':    ('Orchestration', '#1d4ed8'),
    'code':    ('Coding & web',  '#3b82f6'),
    'ai':      ('claude.ai',     '#0891b2'),
    'user':    ('User I/O',      '#0d9488'),
    'process': ('Process',       '#f97316'),
    'memory':  ('Memory',        '#a855f7'),
    'identity':('Identity',      '#10b981'),
    'safety':  ('Safety',        '#ef4444'),
}
FAMILY = {
    'Workflow tool': 'orch', 'Agent tool': 'orch', 'Task tracking\n(6 tools)': 'orch',
    'Monitor': 'orch', 'ScheduleWakeup': 'orch', 'Cron jobs\n(3 tools)': 'orch',
    'Messaging\n(3 tools)': 'orch', 'EndConversation': 'orch',
    'Bash': 'code', 'File tools\n(4 tools)': 'code', 'Worktrees\n(2 tools)': 'code',
    'Plan mode\n(2 tools)': 'code', 'Web fetch\n& search': 'code',
    'Artifact': 'ai', 'DesignSync': 'ai',
    'AskUserQuestion': 'user', 'ReportFindings': 'user', 'Skills\n(/commands)': 'user',
}
segs, total = parse('prompts/claude-code-fable-5.txt')
alt_segs = [(lbl, t, FAMILY.get(lbl, c), sub) for lbl, t, c, sub in segs]
out = render('fable-5-alt', 'Fable 5', alt_segs, total, 'July 2026', cats=ALT_CATS)
print(f"Saved → {out}")
