"""Carousel DESIGN EXPLORATION — a variety of directions, same content, judged side by side.

Ashley, 2026-07-10: *"For these carousels I don't think we have to stick so hard to the branding
conventions. Go for maximum readability in the scroll. A variety of colours, designs, as long as we
keep the Outliers branding somewhere. This whole golden white thing is played out. The images can be
more AI-esque. Nodes. Visualisations we've used before. I'm not a fan of a generated image on the
background that could be done by a real picture. I'm a lot more interested in the abstract. Treat it
like we treated the branding: go through a variety of options."*

So: no FLUX photos. Every background here is PROCEDURAL and abstract — generated as inline SVG from
a fixed seed, so it renders free, instantly, deterministically, and could never be mistaken for a
photograph. Each theme is a complete visual system: palette, type, and its own background language.

Usage, from the labs folder:
    python3 ten_design_systems.py      (on Windows: python ten_design_systems.py)
    builds the contact sheet of every theme and opens it
"""
from __future__ import annotations

import html
import re
import json
import math
import random
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
# An example set of slides that travels with this file, so it runs the moment it is
# cloned. Replace it with your own and keep the same shape.
SPEC = HERE / "example-slides.json"

W, H = 1080, 1350


# ---------------------------------------------------------------------------
# Procedural background languages. Each returns an SVG string. Seeded => stable.
# ---------------------------------------------------------------------------
def bg_nodes(t, seed=1):
    r = random.Random(seed)
    pts = [(r.uniform(0, W), r.uniform(0, H)) for _ in range(34)]
    lines = []
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            d = math.dist(a, b)
            if d < 250:
                o = max(0.04, 0.42 - d / 620)
                lines.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{t["accent"]}" stroke-opacity="{o:.2f}" stroke-width="1.4"/>')
    dots = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2.5,7):.1f}" fill="{t["accent"]}" fill-opacity="{r.uniform(.35,.95):.2f}"/>'
        for x, y in pts)
    glow = f'<circle cx="{W*0.72:.0f}" cy="{H*0.28:.0f}" r="420" fill="url(#g)"/>'
    return f'''<defs><radialGradient id="g"><stop offset="0" stop-color="{t["accent"]}" stop-opacity=".16"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient></defs>{glow}{"".join(lines)}{dots}'''


def bg_mesh(t, seed=2):
    r = random.Random(seed)
    blobs = "".join(
        f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H):.0f}" r="{r.uniform(280,560):.0f}" fill="url(#m{i})"/>'
        for i in range(5))
    defs = "".join(
        f'<radialGradient id="m{i}"><stop offset="0" stop-color="{c}" stop-opacity=".55"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
        for i, c in enumerate([t["accent"], t["accent2"], t["accent"], t["accent2"], t["accent"]]))
    return f"<defs>{defs}</defs>{blobs}"


def bg_grid(t, seed=3):
    step = 60
    v = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{t["accent"]}" stroke-opacity=".13" stroke-width="1"/>' for x in range(0, W, step))
    h = "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{t["accent"]}" stroke-opacity=".13" stroke-width="1"/>' for y in range(0, H, step))
    r = random.Random(seed)
    marks = "".join(
        f'<rect x="{r.randrange(0,W,step)}" y="{r.randrange(0,H,step)}" width="{step*r.randint(1,3)}" height="{step}" fill="{t["accent"]}" fill-opacity=".10"/>'
        for _ in range(9))
    return v + h + marks


def bg_circuit(t, seed=4):
    r = random.Random(seed)
    paths = []
    for _ in range(16):
        x, y = r.randrange(0, W, 40), r.randrange(0, H, 40)
        d = f"M{x} {y}"
        for _ in range(r.randint(2, 5)):
            if r.random() < .5:
                x += r.choice([-1, 1]) * r.randrange(40, 200, 40)
            else:
                y += r.choice([-1, 1]) * r.randrange(40, 200, 40)
            d += f" L{x} {y}"
        paths.append(f'<path d="{d}" fill="none" stroke="{t["accent"]}" stroke-opacity=".28" stroke-width="2"/>')
        paths.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{t["accent2"]}" fill-opacity=".8"/>')
    return "".join(paths)


def bg_iso(t, seed=5):
    r = random.Random(seed)
    cells = []
    for i in range(10):
        for j in range(14):
            if r.random() < .30:
                continue
            cx = 120 + i * 96 - j * 34
            cy = 180 + j * 82 + i * 26
            hgt = r.choice([0, 0, 18, 34, 60])
            op = r.uniform(.12, .55)
            col = t["accent2"] if hgt > 30 else t["accent"]
            cells.append(
                f'<polygon points="{cx},{cy-hgt} {cx+52},{cy+26-hgt} {cx},{cy+52-hgt} {cx-52},{cy+26-hgt}" '
                f'fill="{col}" fill-opacity="{op:.2f}"/>')
    return "".join(cells)


def bg_bars(t, seed=6):
    r = random.Random(seed)
    bars = []
    x = 0
    while x < W:
        bw = r.randrange(24, 90, 6)
        bh = r.uniform(80, H * 0.8)
        bars.append(f'<rect x="{x}" y="{H-bh:.0f}" width="{bw-8}" height="{bh:.0f}" fill="{r.choice([t["accent"],t["accent2"]])}" fill-opacity="{r.uniform(.08,.32):.2f}"/>')
        x += bw
    return "".join(bars)


def bg_rings(t, seed=7):
    r = random.Random(seed)
    out = []
    for _ in range(16):
        cx, cy = r.uniform(0, W), r.uniform(0, H)
        for k in range(r.randint(2, 5)):
            out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{40+k*38}" fill="none" stroke="{t["accent"]}" stroke-opacity="{max(.05,.34-k*.06):.2f}" stroke-width="1.6"/>')
    return "".join(out)


def bg_flow(t, seed=8):
    r = random.Random(seed)
    paths = []
    for i in range(22):
        y = r.uniform(0, H)
        d = f"M-40 {y:.0f}"
        for x in range(0, W + 120, 120):
            y += r.uniform(-70, 70)
            d += f" Q{x+60} {y+r.uniform(-50,50):.0f} {x+120} {y:.0f}"
        paths.append(f'<path d="{d}" fill="none" stroke="{r.choice([t["accent"],t["accent2"]])}" stroke-opacity="{r.uniform(.10,.40):.2f}" stroke-width="{r.uniform(1,3.4):.1f}"/>')
    return "".join(paths)


def bg_blocks(t, seed=9):
    r = random.Random(seed)
    out = []
    for _ in range(7):
        bw, bh = r.randrange(200, 620, 40), r.randrange(120, 460, 40)
        out.append(f'<rect x="{r.randrange(-80,W-100,40)}" y="{r.randrange(-60,H-100,40)}" width="{bw}" height="{bh}" fill="{r.choice([t["accent"],t["accent2"]])}" fill-opacity="{r.uniform(.10,.30):.2f}"/>')
    return "".join(out)


def bg_none(t, seed=0):
    return ""


# ---------------------------------------------------------------------------
# THEMES. Palette + type + background language. All keep an Outliers mark.
# ---------------------------------------------------------------------------
SERIF = '"Constantia", Constantia, Georgia, serif'
GROTESK = '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
MONO = '"Consolas", ui-monospace, monospace'

# LAYOUTS. A direction is a palette AND a way of arranging a slide. Ten of each, paired,
# so the gallery shows ten genuinely different designs rather than one design ten times.
#   stack    — title top, payload bottom (the incumbent)
#   centre   — everything optically centred, generous air, statement-first
#   numeral  — huge ghost numeral behind, content left-aligned over it
#   panel    — solid accent panel holds the payload, title floats above
#   fullbleed— title fills the slide, payload is a tight footer strip
#   inset    — a card floating inside the slide, framed
#   rail     — index runs vertically up the left edge, content offset right
#   band     — a colour band across the middle carries the payload
#   split    — top half title on ground, bottom half inverted (ink/bg swapped)
#   ticket   — dashed rule separates title from payload, monospace docket feel
LAYOUTS = ("stack", "centre", "numeral", "panel", "fullbleed", "inset", "rail", "band", "split", "ticket")


# ⛔ CUT 2026-07-10 — these violated Ashley's own prior ruling and were generated in error.
# The visualiser HOUSE-STYLE bans the matrix/terminal aesthetic because it "reads as
# 'for engineers'" — precisely the register that repels the rung-1 buyer we are writing for.
# The 2026-07-10 relaxation sanctioned colour/layout VARIETY; it did not repeal the AVOID list.
#   "circuit"   — near-black-green, mono, neon traces, self-described "terminal energy"
#   "blueprint" — mono, schematic grid, self-described "engineer register"
# Retained here as a record of what was rejected and why. Do not reinstate.
CUT_DIRECTIONS = {
    "circuit":   "matrix/terminal aesthetic — HOUSE-STYLE avoid list",
    "blueprint": "engineer register — HOUSE-STYLE avoid list",
}

THEMES = {
    "hallmark":   dict(name="Hallmark (current)", bg="#151515", ink="#F3EEE3", dim="#B9B2A4",
                       accent="#C9A25B", accent2="#B08A3E", font=SERIF, idx=MONO, bgfn=bg_none,
                       layout="stack", note="the incumbent, for comparison"),
    "signal":     dict(name="Signal — node graph", bg="#0A0F1C", ink="#EAF2FF", dim="#8FA3C4",
                       accent="#4DA3FF", accent2="#7CF5D5", font=GROTESK, idx=MONO, bgfn=bg_nodes,
                       layout="numeral", note="fleet as a network; AI-native"),
    "ember":      dict(name="Ember — mesh", bg="#12060C", ink="#FFF1EC", dim="#C79B96",
                       accent="#FF5C39", accent2="#FFB03A", font=GROTESK, idx=MONO, bgfn=bg_mesh,
                       layout="fullbleed", note="warm, high heat, thumb-stopping"),
    "foundry":    dict(name="Foundry — isometric", bg="#0E1016", ink="#F2F4F8", dim="#9AA1B2",
                       accent="#8B7BFF", accent2="#E0D5FF", font=GROTESK, idx=MONO, bgfn=bg_iso,
                       layout="inset", note="reuses the visualiser's iso-city look"),
    "ledger":     dict(name="Ledger — data bars", bg="#101418", ink="#F6F7F5", dim="#9BA49E",
                       accent="#F2C14E", accent2="#5FBF8C", font=GROTESK, idx=MONO, bgfn=bg_bars,
                       layout="band", note="numbers register; measurement"),
    "paper":      dict(name="Paper — light editorial", bg="#F5F1E8", ink="#141414", dim="#5C5A53",
                       accent="#1F5AE0", accent2="#E03B2F", font=SERIF, idx=MONO, bgfn=bg_rings,
                       layout="centre", note="LIGHT. maximum contrast in a dark feed"),
    "press":      dict(name="Press — brutalist", bg="#FFFFFF", ink="#000000", dim="#3A3A3A",
                       accent="#FF3B2F", accent2="#0033FF", font=GROTESK, idx=MONO, bgfn=bg_blocks,
                       layout="split", note="loudest legibility; zero decoration"),
    "current":    dict(name="Current — flow lines", bg="#0B0B10", ink="#F4F4FA", dim="#9C9CAC",
                       accent="#00E5FF", accent2="#FF2E93", font=GROTESK, idx=MONO, bgfn=bg_flow,
                       layout="panel", note="movement; work flowing without you"),
}


def seal(t, scale=1.0):
    s = 46 * scale
    return (f'<svg width="{s:.0f}" height="{s:.0f}" viewBox="0 0 190 190">'
            f'<circle cx="95" cy="95" r="88" stroke="{t["ink"]}" stroke-width="7" fill="none"/>'
            f'<circle cx="95" cy="95" r="46" stroke="{t["ink"]}" stroke-width="22" fill="none"/>'
            f'<circle cx="158" cy="31" r="13" fill="{t["accent"]}"/></svg>')


def slide_html(t, s, total, scale=1.0):
    role = s.get("role", "item")
    lay = t.get("layout", "stack")
    bg = t["bgfn"](t)
    svg = f'<svg class="bgsvg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">{bg}</svg>'

    n = len(s.get("title", ""))
    tcls = "t-xl" if (role == "cover" and n <= 34) else ("t-lg" if n <= 46 else "t-md")

    idx = f'<div class="idx">{html.escape(str(s["idx"]))}</div>' if s.get("idx") else ""
    title = f'<div class="title {tcls}">{html.escape(s["title"])}</div>' if s.get("title") else ""
    kick = f'<div class="kicker">{html.escape(s["kicker"])}</div>' if s.get("kicker") else ""
    does = f'<div class="does">{html.escape(s["does"])}</div>' if s.get("does") else ""
    got = f'<div class="got">{s["got"]}</div>' if s.get("got") else ""
    cta = f'<div class="cta">{html.escape(s["cta"])}</div>' if s.get("cta") else ""
    payload = does + got + cta

    # the big ghost numeral, for the `numeral` layout
    num = ""
    if lay == "numeral" and s.get("idx"):
        d = "".join(c for c in str(s["idx"]) if c.isdigit()) or "0"
        num = f'<div class="ghost">{d}</div>'

    head = idx + title + kick

    # A cover has no payload. Layouts built around a payload container (a coloured panel, an
    # inverted half, a band) must not render an empty strip of colour where nothing lives.
    if not payload.strip():
        inner = f'<div class="mid">{head}</div>'
        corner = ('<div class="swipe">swipe &rarr;</div>' if role == "cover"
                  else f'<div class="count">{s["n"]} / {total}</div>')
        return (f'<div class="slide lay-{lay} role-{role} nopay">{svg}<div class="inner">{inner}</div>'
                f'<div class="brand">{seal(t)}<div class="bn">Your Name<small>Your Business</small></div></div>{corner}</div>')

    if lay == "panel":
        inner = f'<div class="top">{head}</div><div class="pane">{payload}</div>'
    elif lay == "band":
        inner = f'<div class="top">{head}</div><div class="bandbox">{payload}</div>'
    elif lay == "inset":
        inner = f'<div class="card">{head}<div class="pay">{payload}</div></div>'
    elif lay == "split":
        inner = f'<div class="half a">{head}</div><div class="half b">{payload}</div>'
    elif lay == "ticket":
        inner = f'<div class="top">{head}</div><div class="rule"></div><div class="pay">{payload}</div>'
    elif lay == "rail":
        inner = f'<div class="railidx">{html.escape(str(s.get("idx","")))}</div><div class="body">{title}{kick}{payload}</div>'
    elif lay == "fullbleed":
        inner = f'<div class="top">{idx}{title}</div><div class="foot">{kick}{payload}</div>'
    elif lay == "centre":
        inner = f'<div class="mid">{head}{payload}</div>'
    elif lay == "numeral":
        inner = f'{num}<div class="over">{head}{payload}</div>'
    else:  # stack
        inner = head + payload

    corner = ('<div class="swipe">swipe &rarr;</div>' if role == "cover"
              else f'<div class="count">{s["n"]} / {total}</div>')
    return (f'<div class="slide lay-{lay} role-{role}">{svg}<div class="inner">{inner}</div>'
            f'<div class="brand">{seal(t)}<div class="bn">Your Name<small>Your Business</small></div></div>{corner}</div>')


def prefix_css(text: str, pre: str) -> str:
    """Namespace every rule in a theme's CSS so themes can sit on one page."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^(\s*)(\.[^{]+?)\s*\{(.*)$", line)
        out.append(f"{m.group(1)}{pre} {m.group(2).strip()} {{{m.group(3)}" if m else line)
    return "\n".join(out)


def css(t, scale=1.0):
    k = scale
    return f"""
  .slide {{ width:{W*k:.0f}px; height:{H*k:.0f}px; position:relative; overflow:hidden;
            background:{t['bg']}; color:{t['ink']}; font-family:{t['font']};
            display:flex; flex-direction:column; }}
  .bgsvg {{ position:absolute; inset:0; width:100%; height:100%; }}
  .inner {{ position:relative; z-index:2; flex:1; display:flex; flex-direction:column;
            padding:{84*k:.0f}px {72*k:.0f}px {126*k:.0f}px; }}
  .idx {{ font-family:{t['idx']}; font-size:{25*k:.0f}px; letter-spacing:.3em; text-transform:uppercase;
          color:{t['accent']}; margin-bottom:{24*k:.0f}px; font-weight:600; }}
  .title {{ font-weight:800; line-height:1.02; letter-spacing:-.01em; }}
  .t-xl {{ font-size:{112*k:.0f}px; }} .t-lg {{ font-size:{82*k:.0f}px; }} .t-md {{ font-size:{62*k:.0f}px; }}
  .kicker {{ font-size:{36*k:.0f}px; line-height:1.3; color:{t['accent']}; margin-top:{30*k:.0f}px; font-weight:500; }}
  .does {{ padding-top:{30*k:.0f}px; font-size:{40*k:.0f}px; line-height:1.32; color:{t['ink']}; max-width:{900*k:.0f}px; font-weight:600; }}
  .got {{ margin-top:{22*k:.0f}px; font-size:{33*k:.0f}px; line-height:1.36; color:{t['dim']}; max-width:{900*k:.0f}px; }}
  .got b {{ color:{t['accent']}; font-weight:800; }}
  .cta {{ font-family:{t['idx']}; font-size:{30*k:.0f}px; letter-spacing:.22em; text-transform:uppercase; color:{t['accent']}; margin-top:{40*k:.0f}px; font-weight:700; }}

  /* ---- layouts: each direction arranges the slide its own way ---- */
  .lay-stack .inner {{ justify-content:flex-start; }}
  .lay-stack .does {{ margin-top:{56*k:.0f}px; }}

  .lay-centre .inner {{ justify-content:center; align-items:center; text-align:center; }}
  .lay-centre .does, .lay-centre .got {{ max-width:{820*k:.0f}px; }}

  .lay-numeral .inner {{ justify-content:center; }}
  .lay-numeral .ghost {{ position:absolute; right:{-30*k:.0f}px; top:{40*k:.0f}px; font-size:{620*k:.0f}px;
        font-weight:900; line-height:.8; color:{t['accent']}; opacity:.14; z-index:0; font-family:{t['idx']}; }}
  .lay-numeral .over {{ position:relative; z-index:2; }}

  .lay-panel .inner {{ justify-content:space-between; padding-bottom:0; }}
  .lay-panel .pane {{ background:{t['accent']}; color:{t['bg']}; margin:0 {-72*k:.0f}px; padding:{54*k:.0f}px {72*k:.0f}px {150*k:.0f}px; }}
  .lay-panel .pane .does {{ color:{t['bg']}; padding-top:0; }}
  .lay-panel .pane .got {{ color:{t['bg']}; opacity:.82; }}
  .lay-panel .pane .got b {{ color:{t['bg']}; }}
  .lay-panel .pane .cta {{ color:{t['bg']}; }}

  .lay-fullbleed .inner {{ justify-content:space-between; }}
  .lay-fullbleed .title {{ font-size:{126*k:.0f}px; line-height:.98; }}
  .lay-fullbleed .foot {{ border-top:{3*k:.0f}px solid {t['accent']}; padding-top:{28*k:.0f}px; }}

  .lay-inset .inner {{ justify-content:center; padding:{56*k:.0f}px; }}
  .lay-inset .card {{ border:{2*k:.0f}px solid {t['accent']}; background:rgba(0,0,0,.34);
        padding:{56*k:.0f}px {52*k:.0f}px; backdrop-filter:blur(2px); }}
  .lay-inset .pay {{ margin-top:{34*k:.0f}px; }}

  .lay-rail .inner {{ flex-direction:row; align-items:stretch; padding-left:{56*k:.0f}px; }}
  .lay-rail .railidx {{ writing-mode:vertical-rl; transform:rotate(180deg); font-family:{t['idx']};
        font-size:{26*k:.0f}px; letter-spacing:.34em; text-transform:uppercase; color:{t['accent']};
        border-right:{2*k:.0f}px solid {t['accent']}; padding-right:{22*k:.0f}px; margin-right:{40*k:.0f}px; }}
  .lay-rail .body {{ display:flex; flex-direction:column; justify-content:center; flex:1; }}

  .lay-band .inner {{ justify-content:center; }}
  .lay-band .bandbox {{ background:{t['bg']}; border-top:{4*k:.0f}px solid {t['accent']};
        border-bottom:{4*k:.0f}px solid {t['accent']}; margin:{40*k:.0f}px {-72*k:.0f}px 0;
        padding:{44*k:.0f}px {72*k:.0f}px; }}

  .lay-split .inner {{ padding:0; }}
  .lay-split .half {{ padding:{72*k:.0f}px; }}
  .lay-split .half.a {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
  .lay-split .half.b {{ background:{t['ink']}; color:{t['bg']}; padding-bottom:{140*k:.0f}px; }}
  .lay-split .half.b .does {{ color:{t['bg']}; padding-top:0; }}
  .lay-split .half.b .got {{ color:{t['bg']}; opacity:.78; }}
  .lay-split .half.b .got b, .lay-split .half.b .cta {{ color:{t['accent']}; }}

  .lay-ticket .inner {{ justify-content:flex-start; }}
  .lay-ticket .rule {{ border-top:{2*k:.0f}px dashed {t['accent']}; margin:{40*k:.0f}px 0; opacity:.6; }}
  .lay-ticket .pay {{ }}

  /* the cover never carries a payload, so let its title breathe */
  .role-cover .inner {{ justify-content:center; }}
  .nopay .inner {{ justify-content:center; }}
  .nopay .mid {{ display:flex; flex-direction:column; }}

  /* Inverted payload panels swallow the brand mark, which is ink-coloured. On those layouts
     the mark sits ON the panel, so it must be drawn in the ground colour instead. */
  .lay-panel .brand svg circle, .lay-split .brand svg circle {{ stroke:{t['bg']}; }}
  .lay-panel .brand svg circle:last-child, .lay-split .brand svg circle:last-child {{ fill:{t['bg']}; stroke:none; }}
  .lay-panel .brand .bn, .lay-split .brand .bn {{ color:{t['bg']}; }}
  .lay-panel .brand .bn small, .lay-split .brand .bn small {{ color:{t['bg']}; opacity:.75; }}
  .lay-panel .count, .lay-split .count {{ color:{t['bg']}; opacity:.7; }}
  /* ...but a cover has no panel, so the mark reverts to ink */
  .lay-panel.nopay .brand svg circle, .lay-split.nopay .brand svg circle {{ stroke:{t['ink']}; }}
  .lay-panel.nopay .brand svg circle:last-child, .lay-split.nopay .brand svg circle:last-child {{ fill:{t['accent']}; stroke:none; }}
  .lay-panel.nopay .brand .bn, .lay-split.nopay .brand .bn {{ color:{t['ink']}; }}
  .lay-panel.nopay .brand .bn small, .lay-split.nopay .brand .bn small {{ color:{t['accent']}; }}
  .brand {{ position:absolute; z-index:3; left:{72*k:.0f}px; bottom:{50*k:.0f}px; display:flex; align-items:center; gap:{14*k:.0f}px; }}
  .brand svg {{ width:{46*k:.0f}px; height:{46*k:.0f}px; }}
  .bn {{ font-family:{t['idx']}; font-size:{19*k:.0f}px; letter-spacing:.16em; text-transform:uppercase; color:{t['ink']}; opacity:.9; line-height:1.2; }}
  .bn small {{ display:block; font-size:{14*k:.0f}px; letter-spacing:.28em; color:{t['accent']}; }}
  .count, .swipe {{ position:absolute; z-index:3; right:{72*k:.0f}px; bottom:{56*k:.0f}px;
            font-family:{t['idx']}; font-size:{21*k:.0f}px; letter-spacing:.2em; }}
  .count {{ color:{t['dim']}; }} .swipe {{ color:{t['accent']}; }}
"""


def gallery():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    slides = spec["slides"]
    pick = [slides[0], slides[2], slides[-1]]  # cover, an item, the CTA
    total = len(slides)
    scale = 0.30

    blocks, scoped = [], []
    for key, t in THEMES.items():
        pre = f"th-{key}"
        cards = "".join(slide_html(t, s, total, scale) for s in pick)
        blocks.append(f"""
<section class="theme">
  <h2>{html.escape(t['name'])} <span class="key">{key}</span></h2>
  <p class="note">{html.escape(t['note'])}</p>
  <div class="row {pre}">{cards}</div>
</section>""")
        scoped.append(prefix_css(css(t, scale), f".{pre}"))

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Carousel design directions</title>
<style>
 body {{ margin:0; background:#191919; color:#eee; font-family:{GROTESK}; padding:28px 32px 90px; }}
 h1 {{ font-size:22px; margin:0 0 6px; }}
 .lede {{ color:#9a9a9a; font-size:13.5px; max-width:900px; margin:0 0 28px; line-height:1.5; }}
 section.theme {{ margin-bottom:38px; }}
 section.theme h2 {{ font-size:16px; margin:0 0 2px; font-weight:600; }}
 section.theme .key {{ font:12px {MONO}; color:#8a8a8a; margin-left:8px; }}
 section.theme .note {{ color:#8f8f8f; font-size:12.5px; margin:0 0 12px; }}
 .row {{ display:flex; gap:16px; }}
 {"".join(scoped)}
</style></head><body>
<h1>Carousel design directions</h1>
<p class="lede">Same content in every one, so you are judging the design and not the copy. Cover, one build slide, and the CTA. All backgrounds are generated abstractly from code, not photographs. Every option keeps the Outliers mark bottom-left.</p>
{"".join(blocks)}
</body></html>"""
    out = HERE / "_gallery" / "carousel-directions.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"gallery -> {out}")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "gallery"
    if cmd == "gallery":
        p = gallery()
        # Opens the page in the member's own default browser.
        if webbrowser.open(p.as_uri()):
            print("opened in your browser")
