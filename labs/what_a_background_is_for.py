"""INTERACTION LAB — how does the background interact with the TEXT?

Ashley, 2026-07-10: *"We need to stop playing with colours and start understanding how the
background interacts with the text. The colour doesn't really matter as long as it's not
massively ugly."*

He is right, and the colour work was a trap: it was measurable, so it felt like progress.
Contrast is a FLOOR to clear, not a thing to optimise. One ground (indigo), readable, move on.

THE REAL QUESTION. Our doctrine says a background either MEANS something or RECEDES. By that
standard the abstract node field we built encodes NOTHING — the nodes connect to nothing. It is
chartjunk with a good haircut. So: what can a background legitimately encode?

Everything here is derived FROM THE SLIDE'S OWN CONTENT. Nothing is ambient. Each device is
labelled with what it encodes, and the ones that encode nothing are named as decoration so we
can kill them honestly.

    A. TYPE IS THE GROUND      the words themselves form the field
       ghost      the key noun, set enormous behind      encodes: the subject
       knockout   type cut out of the colour field       encodes: nothing (pure style)

    B. THE GROUND MARKS THE MEANING     it points at the words
       cue        one phrase highlighted, Mayer signalling  encodes: what matters most
       invert     payload half flips ground/ink             encodes: the turn from claim to result

    C. THE GROUND IS THE STRUCTURE      it draws the sentence's shape
       triple     artefact -> function -> result, as an actual connected graph
                                                            encodes: the three beats and their relation
       accrue     each slide adds ONE node to a graph that grows across the deck; the last slide
                  is the whole operation                    encodes: that the builds compose into a system

`accrue` is the one that answers "do nodes connect?" honestly: a node earns its place only when
the edge means something. Here an edge means "this build feeds that one".

Usage, from the labs folder:
    python3 what_a_background_is_for.py      (on Windows: python what_a_background_is_for.py)
"""
from __future__ import annotations

import html
import json
import math
import sys
import webbrowser
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "_gallery"
# The example slides that travel with this file, so it runs the moment it is cloned.
SPEC = HERE / "example-slides.json"
W, H = 1080, 1350

# Colour is settled. Readable, not ugly. It is not the subject of this lab.
GROUND, INK, ACC, ACC_DIM = "#3A2BD9", "#FFFFFF", "#CCFF00", "#8FA0F0"

SLIDE = dict(
    idx="Build 1",
    title="A client database that fills itself",
    does="Every call and message logs itself as it happens, so I type nothing up.",
    bold="I own it outright.",
    rest="It surfaced a renewal I had let slip, and I reached the client in time.",
    key="itself",
    # the three beats, named, for the structural devices
    artefact="client database",
    function="logs itself",
    result="renewal reached",
)

# The real dependency graph of the seven builds. An edge means "feeds".
# This is the thing an honest node diagram would encode.
BUILDS = ["client database", "meeting triage", "video cutter", "carousel renderer",
          "fold preview", "visualiser studio", "book ingestion"]
EDGES = [(0, 1), (1, 5), (2, 5), (3, 4), (6, 0), (0, 3)]


def esc(s):
    return html.escape(s)


# ---------------------------------------------------------------------------
# DEVICES. Each returns (svg_layer, body_html, encodes, verdict)
# ---------------------------------------------------------------------------
def dev_ghost():
    layer = f'<div class="ghost">{esc(SLIDE["key"])}</div>'
    return layer, _body(), "the subject of the sentence, made the field", "MEANS something"


def dev_knockout():
    layer = ""
    body = f'''<div class="inner">
      <div class="idx">{esc(SLIDE["idx"])}</div>
      <div class="title ko">{esc(SLIDE["title"])}</div>
      <div class="does">{esc(SLIDE["does"])}</div>
      <div class="got"><b>{esc(SLIDE["bold"])}</b> {esc(SLIDE["rest"])}</div>
    </div>'''
    return layer, body, "nothing — the type is merely reversed", "DECORATION (style, not meaning)"


def dev_cue():
    body = f'''<div class="inner">
      <div class="idx">{esc(SLIDE["idx"])}</div>
      <div class="title">{esc(SLIDE["title"])}</div>
      <div class="does">{esc(SLIDE["does"])}</div>
      <div class="got"><span class="cue"><b>{esc(SLIDE["bold"])}</b></span> {esc(SLIDE["rest"])}</div>
    </div>'''
    return "", body, "which single phrase carries the payload (Mayer signalling)", "MEANS something"


def dev_invert():
    body = f'''<div class="inner nop">
      <div class="top">
        <div class="idx">{esc(SLIDE["idx"])}</div>
        <div class="title">{esc(SLIDE["title"])}</div>
      </div>
      <div class="pay">
        <div class="does">{esc(SLIDE["does"])}</div>
        <div class="got"><b>{esc(SLIDE["bold"])}</b> {esc(SLIDE["rest"])}</div>
      </div>
    </div>'''
    return "", body, "the turn: claim above the line, consequence below it", "MEANS something"


def dev_triple():
    """The sentence's own structure, drawn. artefact -> function -> result."""
    a, f, r = SLIDE["artefact"], SLIDE["function"], SLIDE["result"]
    y = 980
    layer = f'''<svg class="lay" viewBox="0 0 {W} {H}">
      <line x1="150" y1="{y}" x2="530" y2="{y}" stroke="{ACC}" stroke-width="4" marker-end="url(#a)"/>
      <line x1="620" y1="{y}" x2="960" y2="{y}" stroke="{ACC}" stroke-width="4" marker-end="url(#a)"/>
      <defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="{ACC}"/></marker></defs>
      <circle cx="110" cy="{y}" r="16" fill="{ACC}"/>
      <circle cx="575" cy="{y}" r="16" fill="{ACC}"/>
      <circle cx="1000" cy="{y}" r="16" fill="{ACC}"/>
      <text x="110" y="{y+52}" fill="{INK}" font-size="30" font-family="Segoe UI, Helvetica Neue">{esc(a)}</text>
      <text x="500" y="{y-34}" fill="{ACC}" font-size="28" font-family="Consolas, Menlo">{esc(f)}</text>
      <text x="880" y="{y+52}" fill="{INK}" font-size="30" font-family="Segoe UI, Helvetica Neue">{esc(r)}</text>
    </svg>'''
    body = f'''<div class="inner">
      <div class="idx">{esc(SLIDE["idx"])}</div>
      <div class="title">{esc(SLIDE["title"])}</div>
      <div class="does short">{esc(SLIDE["does"])}</div>
    </div>'''
    return layer, body, "the three beats and the relation between them", "MEANS something (Larkin & Simon: relational info)"


def dev_accrue(step=3):
    """A graph that GROWS across the deck. Slide n lights node n. Edges mean 'feeds'."""
    cx, cy, R = W / 2, 900, 300
    pts = [(cx + R * math.cos(2 * math.pi * i / 7 - math.pi / 2),
            cy + R * math.sin(2 * math.pi * i / 7 - math.pi / 2)) for i in range(7)]
    edges = "".join(
        f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" '
        f'stroke="{ACC if max(a,b) < step else ACC_DIM}" stroke-opacity="{0.9 if max(a,b) < step else 0.20}" stroke-width="3"/>'
        for a, b in EDGES)
    nodes = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{20 if i < step else 12}" '
        f'fill="{ACC if i < step else "transparent"}" stroke="{ACC_DIM}" stroke-width="3" '
        f'fill-opacity="{1 if i < step else 0}"/>'
        for i, (x, y) in enumerate(pts))
    label = f'<text x="{cx}" y="{cy+8}" fill="{INK}" font-size="30" font-family="Consolas, Menlo" text-anchor="middle" opacity=".8">{step} of 7 built</text>'
    layer = f'<svg class="lay" viewBox="0 0 {W} {H}">{edges}{nodes}{label}</svg>'
    body = f'''<div class="inner">
      <div class="idx">{esc(SLIDE["idx"])}</div>
      <div class="title">{esc(SLIDE["title"])}</div>
    </div>'''
    return layer, body, "NOTHING a reader can decode — the nodes are UNLABELLED", "DECORATION — a diagram making a false promise"


def dev_ambient():
    """The control. What we currently ship. Included so the test can condemn our own work."""
    import random
    r = random.Random(9)
    pts = [(r.uniform(0, W), r.uniform(0, H)) for _ in range(30)]
    lines = "".join(
        f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{ACC}" stroke-opacity=".18" stroke-width="1.4"/>'
        for i, a in enumerate(pts) for b in pts[i + 1:] if math.dist(a, b) < 240)
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{ACC}" fill-opacity=".5"/>' for x, y in pts)
    return f'<svg class="lay">{lines}{dots}</svg>', _body(), "NOTHING. the nodes connect nothing.", "DECORATION — chartjunk. Our own current build."



def dev_numeral():
    """The evidence-backed default for a list slide.

    Carousel visual-grammar research: the item NUMERAL as the largest element anchors a
    type-only slide AND signals position, so no illustration is needed. Combined with
    signalling (Mayer, g~0.38 — strongest for low-prior-knowledge readers, i.e. a cold
    scroller) on the ONE verdict phrase. Zero added objects. Nothing to misread.
    """
    layer = f'<div class="bignum">1</div>'
    body = f'''<div class="inner">
      <div class="idx">of 7 builds</div>
      <div class="title">{esc(SLIDE["title"])}</div>
      <div class="does">{esc(SLIDE["does"])}</div>
      <div class="got"><span class="cue"><b>{esc(SLIDE["bold"])}</b></span> {esc(SLIDE["rest"])}</div>
    </div>'''
    return layer, body, "which item this is, of how many — and the one phrase that carries the payload", "MEANS something (numeral = position; cue = signalling)"


def dev_named_graph():
    """A network that actually earns it: NAMED nodes, <=7, ONE relationship highlighted.

    Belongs on the FINAL slide, not on an item slide. It answers a question the prose does
    not: how the seven builds compose into one operation (Larkin & Simon: relational info).
    """
    import math as _m
    cx, cy, R = W / 2, 760, 250
    pts = [(cx + R * _m.cos(2 * _m.pi * i / 7 - _m.pi / 2),
            cy + R * _m.sin(2 * _m.pi * i / 7 - _m.pi / 2)) for i in range(7)]
    short = ["database", "meetings", "video", "carousels", "preview", "studio", "books"]
    edges = "".join(
        f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" '
        f'stroke="{ACC if (a,b)==(0,1) else ACC_DIM}" stroke-opacity="{1 if (a,b)==(0,1) else .35}" '
        f'stroke-width="{5 if (a,b)==(0,1) else 2}"/>' for a, b in EDGES)
    nodes = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{ACC}"/>'
        f'<text x="{x:.0f}" y="{y + (46 if y > cy else -28):.0f}" fill="{INK}" font-size="27" '
        f'font-family="Segoe UI, Helvetica Neue" text-anchor="middle">{n}</text>'
        for (x, y), n in zip(pts, short))
    layer = f'<svg class="lay" viewBox="0 0 {W} {H}">{edges}{nodes}</svg>'
    body = '''<div class="inner">
      <div class="idx">All seven</div>
      <div class="title">They feed each other.</div>
    </div>'''
    return layer, body, "how the seven builds compose into one operation; the lit edge = 'feeds'", "MEANS something — but ONLY on the final slide, and only NAMED"


def _body():
    return f'''<div class="inner">
      <div class="idx">{esc(SLIDE["idx"])}</div>
      <div class="title">{esc(SLIDE["title"])}</div>
      <div class="does">{esc(SLIDE["does"])}</div>
      <div class="got"><b>{esc(SLIDE["bold"])}</b> {esc(SLIDE["rest"])}</div>
    </div>'''


DEVICES = {
    "numeral":  dev_numeral,
    "named_graph": dev_named_graph,
    "ghost":    dev_ghost,
    "cue":      dev_cue,
    "invert":   dev_invert,
    "triple":   dev_triple,
    "accrue":   dev_accrue,
    "knockout": dev_knockout,
    "ambient":  dev_ambient,
}

CSS = f"""
 body {{ margin:0 }}
 .slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; background:{GROUND}; color:{INK};
   font-family:"Segoe UI",Arial,sans-serif; }}
 .lay {{ position:absolute; inset:0; width:100%; height:100%; z-index:1; }}
 .ghost {{ position:absolute; z-index:1; right:-70px; top:150px; font-size:500px; font-weight:900;
   line-height:.8; color:{ACC}; opacity:.16; letter-spacing:-.04em; }}
 .inner {{ position:relative; z-index:3; height:100%; display:flex; flex-direction:column; padding:84px 76px 132px; }}
 .idx {{ font-family:Consolas,Menlo,monospace; font-size:26px; letter-spacing:.34em; text-transform:uppercase; color:{ACC}; margin-bottom:24px; }}
 .title {{ font-size:92px; font-weight:800; line-height:1.02; letter-spacing:-.01em; }}
 .does {{ margin-top:92px; font-size:42px; line-height:1.34; font-weight:600; max-width:900px; }}
 .does.short {{ margin-top:60px; max-width:820px; }}
 .got {{ margin-top:22px; font-size:36px; line-height:1.36; max-width:900px; }}
 .got b {{ color:{ACC}; font-weight:800; }}
 .cue {{ background:{ACC}; color:{GROUND}; padding:.02em .16em; box-decoration-break:clone; }}
 .cue b {{ color:{GROUND}; }}
 .title.ko {{ color:{GROUND}; background:{ACC}; box-decoration-break:clone; padding:.04em .16em; margin-left:-.16em; }}
 .inner.nop {{ padding:0 }}
 .inner.nop .top {{ flex:1; padding:84px 76px 40px; display:flex; flex-direction:column; justify-content:center; }}
 .inner.nop .pay {{ background:{INK}; color:{GROUND}; padding:56px 76px 140px; }}
 .inner.nop .pay .does {{ margin-top:0 }}
 .inner.nop .pay .got b {{ color:#5C7300; }}
 .bignum {{ position:absolute; z-index:1; right:40px; bottom:40px; font-size:640px; font-weight:900;
   line-height:.72; color:{ACC}; opacity:.17; letter-spacing:-.06em; }}
 .brand {{ position:absolute; z-index:4; left:76px; bottom:56px; font-family:Consolas,Menlo,monospace;
   font-size:19px; letter-spacing:.18em; text-transform:uppercase; color:{INK}; opacity:.85; }}
 .brand i {{ display:block; font-style:normal; font-size:14px; letter-spacing:.3em; color:{ACC}; }}
"""


def main():
    OUT.mkdir(exist_ok=True)
    meta = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, fn in DEVICES.items():
            layer, body, encodes, verdict = fn()
            doc = (f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>"
                   f"<div class='slide'>{layer}{body}"
                   f"<div class='brand'>Your Name<i>Your Business</i></div></div>")
            f = OUT / f"_int-{name}.html"; f.write_text(doc, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(180)
            pg.locator(".slide").screenshot(path=str(OUT / f"int-{name}.png"))
            meta[name] = (encodes, verdict)
            print(f"  {name:9} {verdict}")
        b.close()

    cards = "".join(f'''
  <figure class="{'bad' if meta[n][1].startswith('DECORATION') else 'good'}">
    <img src="int-{n}.png">
    <figcaption><b>{n}</b>
      <span class="enc"><i>encodes:</i> {esc(meta[n][0])}</span>
      <span class="ver">{esc(meta[n][1])}</span>
    </figcaption>
  </figure>''' for n in DEVICES)

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Background × text</title><style>
 body{{margin:0;background:#0f0f10;color:#eee;font-family:Segoe UI,Arial,sans-serif;padding:26px 30px 80px}}
 h1{{font-size:21px;margin:0 0 4px}} p.l{{color:#9a9a9a;font-size:13px;max-width:960px;line-height:1.55;margin:0 0 20px}}
 .grid{{display:flex;flex-wrap:wrap;gap:22px}} figure{{margin:0;width:250px}}
 img{{display:block;width:100%;border-radius:6px;border:1px solid #333}}
 figure.bad img{{outline:2px solid #a33;outline-offset:2px}}
 figcaption b{{display:block;font-size:14px;margin-top:8px}}
 .enc{{display:block;color:#9a9a9a;font-size:12px;margin:3px 0}} .enc i{{color:#666}}
 .ver{{display:block;font-size:12px;margin-top:3px}}
 figure.good .ver{{color:#7fd18b}} figure.bad .ver{{color:#e07a7a}}
</style></head><body>
<h1>How the background interacts with the text</h1>
<p class="l">Colour is settled and is not the subject here: one ground, readable, not ugly. Every device below is derived from <b>the slide's own words</b>. The rule from our doctrine is that a background either <b>means something</b> or it recedes — so each is labelled with what it actually encodes. The two outlined in red encode nothing. One of them is <b>what we currently ship</b>: an ambient node field whose nodes connect nothing. It is included so the test can condemn our own work.</p>
<div class="grid">{cards}</div>
</body></html>"""
    out = OUT / "background-x-text.html"
    out.write_text(doc, encoding="utf-8")
    print(f"\nsheet -> {out}")
    # Opens the page in the member's own default browser.
    if webbrowser.open(out.as_uri()):
        print("opened in your browser")


if __name__ == "__main__":
    main()
