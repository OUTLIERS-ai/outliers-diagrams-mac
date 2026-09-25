"""FEED LAB — what actually breaks a LinkedIn feed, and can the background mould to the words?

Ashley, 2026-07-10: *"I'm less interested in sticking with the branding colours. We've got the
opportunity now to test what colours stick out the most on a feed and we absolutely should. We
should consider how the background fits with the words. Can we create a background that fits with
the words so that certain words are exaggerated, or the colour changes, or the background moulds
with the words? I think we've got a possibility here to be really quite creative."*

TWO EXPERIMENTS, deliberately separated:

  A. SALIENCE — which palettes break the feed. This is MEASURABLE, not a matter of taste.
     The LinkedIn feed ground is #F4F2EE (light) / #1B1F23 (dark). A slide pops by being a
     feature singleton against that ground (doctrine §2d). So we compute, per palette:
       * ΔE2000 from the feed ground   — perceptual colour distance, the pop
       * WCAG contrast vs feed ground   — luminance separation
       * WCAG contrast of ink on ground — legibility, which no amount of pop may sacrifice
     A palette that pops but cannot be read is a failure. Both numbers must clear.

  B. WORD-REACTIVE BACKGROUNDS — the background derived FROM the words, not decorating them.
     This does not breach the coherence principle: that rule says a background either MEANS
     something or recedes. A ground shaped by the text means something.

Usage, from the labs folder:
    python3 colour_measure.py          (on Windows: python colour_measure.py)
    renders, measures, builds the sheet and opens it
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
W, H = 1080, 1350

# The feed a slide has to survive. LinkedIn light mode is the common case.
FEED_LIGHT = "#F4F2EE"
FEED_DARK = "#1B1F23"


# ---------------------------------------------------------------------------
# Colour maths. ΔE2000 is the perceptual distance that predicts "pop".
# ---------------------------------------------------------------------------
def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(h):
    r, g, b = (_lin(x) for x in hex_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _xyz(h):
    r, g, b = (_lin(x) for x in hex_rgb(h))
    return (r * .4124 + g * .3576 + b * .1805,
            r * .2126 + g * .7152 + b * .0722,
            r * .0193 + g * .1192 + b * .9505)


def _lab(h):
    x, y, z = _xyz(h)
    x, y, z = x / .95047, y / 1.0, z / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a, b):
    """CIE76 — close enough to rank pop, and honest about being an approximation of ΔE2000."""
    la, aa, ba = _lab(a)
    lb, ab, bb = _lab(b)
    return math.dist((la, aa, ba), (lb, ab, bb))




def _mix(hexc, k, toward):
    """Blend a colour toward black (toward=0) or white (toward=255)."""
    r, g, b = hex_rgb(hexc)
    f = lambda c: int(round(c + (toward - c) * k))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))


def accent_for(surface, accent, floor=4.5):
    """An accent tuned for a dark ground is INVISIBLE on a light one.

    Measured: acid lime (#CCFF00) is 16.8:1 on near-black and 1.0:1 on the light half of an
    `invert` treatment. Ten of twelve palettes failed the same way. A palette is therefore not
    (ground, ink, accent) — it needs an accent PER SURFACE.

    Push the accent AWAY from the surface it must sit on (darken it on a light surface, lighten
    it on a dark one) until it clears the WCAG floor. Direction matters: an earlier version only
    darkened, so it failed on light palettes whose inverted half is dark.
    """
    if contrast(accent, surface) >= floor:
        return accent
    toward = 0 if luminance(surface) > 0.18 else 255   # move away from the surface
    best = accent
    for i in range(1, 21):
        cand = _mix(accent, i * 0.05, toward)
        if contrast(cand, surface) >= floor:
            return cand
        best = cand
    return best


# ---------------------------------------------------------------------------
# A. PALETTES. Brand-free, per Ashley. Two controls included so the test can fail honestly.
# ---------------------------------------------------------------------------
# Revised 2026-07-10 after Ashley: "I don't like orange for the green one."
#   * `safety` (safety orange) CUT — he does not want it.
#   * `chartreuse` had a RED accent at 2.9:1 on its own ground. That was never a taste problem:
#     it was unreadable. Swapped to a deep-violet accent (12.1:1). The dislike was correct and
#     the measurement explains why.
#   * Added the non-orange grounds that survive BOTH feed modes and carry legible ink:
#     electric indigo, royal violet, spring green, crimson, plum.
#   * `gold` added as a GROUND (gold field, black ink). It survives both feeds where the same
#     gold as an accent on a dark ground does not. The brand colour is not the problem; using
#     it dark is.
PALETTES = {
    "hallmark":   dict(bg="#151515", ink="#F3EEE3", acc="#C9A25B", note="CONTROL — the current brand; vanishes in dark mode"),
    "linkedin":   dict(bg="#0A66C2", ink="#FFFFFF", acc="#7CF5D5", note="CONTROL — platform's own chrome"),
    "indigo":     dict(bg="#3A2BD9", ink="#FFFFFF", acc="#CCFF00", note="acid lime on electric indigo — top pop"),
    "violet":     dict(bg="#4B27C9", ink="#FFFFFF", acc="#FFE45C", note="gold on royal violet"),
    "cobalt":     dict(bg="#0B2FCB", ink="#FFFFFF", acc="#FFE45C", note="gold on cobalt"),
    "chartreuse": dict(bg="#D6F700", ink="#0A0A0A", acc="#2A1B5E", note="LIGHT — deep violet on chartreuse (was unreadable red)"),
    "spring":     dict(bg="#1FD65F", ink="#0A0A0A", acc="#12124A", note="LIGHT — navy on spring green"),
    "crimson":    dict(bg="#B0122F", ink="#FFFFFF", acc="#FFD166", note="warm gold on crimson"),
    "plum":       dict(bg="#5B1D5B", ink="#FFF3FF", acc="#7CF5D5", note="mint on plum"),
    "oxblood":    dict(bg="#4A0E1E", ink="#FFF3E8", acc="#FFC94A", note="cream + gold on oxblood"),
    "gold":       dict(bg="#C9A25B", ink="#0A0A0A", acc="#12124A", note="LIGHT — the brand gold as GROUND, not accent"),
    "paper":      dict(bg="#F5F1E8", ink="#141414", acc="#1F5AE0", note="CONTROL — near-white; blends with the light feed"),
}


def score(p):
    """A palette must POP and be READABLE. Neither buys the other."""
    pop_light = delta_e(p["bg"], FEED_LIGHT)
    pop_dark = delta_e(p["bg"], FEED_DARK)
    con_feed = contrast(p["bg"], FEED_LIGHT)
    legible = contrast(p["ink"], p["bg"])
    acc_legible = contrast(p["acc"], p["bg"])
    # the binding constraint is the WORSE of the two feed modes
    pop = min(pop_light, pop_dark)
    return dict(pop_light=pop_light, pop_dark=pop_dark, pop=pop,
                con_feed=con_feed, legible=legible, acc_legible=acc_legible,
                verdict=("FAIL: unreadable" if legible < 4.5 else
                         "FAIL: accent unreadable" if acc_legible < 3.0 else
                         "weak pop" if pop < 25 else
                         "strong"))


# ---------------------------------------------------------------------------
# B. WORD-REACTIVE TREATMENTS. The ground derived from the text.
# ---------------------------------------------------------------------------
COPY = dict(
    idx="Build 1",
    title="A client database that fills itself",
    does="Every call and message logs itself as it happens, so I type nothing up.",
    got_plain="It surfaced a renewal I had let slip, and I reached the client in time.",
    got_bold="I own it outright.",
    key="itself",          # the word the ground reacts to
)

TREATMENTS = {
    "knockout": dict(
        note="the words are CUT OUT of the colour field; type is the ground showing through",
        body=lambda p: f'''
  <div class="ko-field"></div>
  <div class="inner">
    <div class="idx">{COPY["idx"]}</div>
    <div class="title ko">{COPY["title"]}</div>
    <div class="does">{COPY["does"]}</div>
    <div class="got"><b>{COPY["got_bold"]}</b> {COPY["got_plain"]}</div>
  </div>'''),

    "highlighter": dict(
        note="the result phrase gets a swiped accent block behind it, like a marker pen",
        body=lambda p: f'''
  <div class="inner">
    <div class="idx">{COPY["idx"]}</div>
    <div class="title">{COPY["title"]}</div>
    <div class="does">{COPY["does"]}</div>
    <div class="got"><span class="hl"><b>{COPY["got_bold"]}</b></span> {COPY["got_plain"]}</div>
  </div>'''),

    "ghost": dict(
        note="the key word set enormous and faint behind everything; the ground IS the word",
        body=lambda p: f'''
  <div class="ghost">{COPY["key"]}</div>
  <div class="inner">
    <div class="idx">{COPY["idx"]}</div>
    <div class="title">{COPY["title"]}</div>
    <div class="does">{COPY["does"]}</div>
    <div class="got"><b>{COPY["got_bold"]}</b> {COPY["got_plain"]}</div>
  </div>'''),

    "swell": dict(
        note="a thick accent rule swells beneath the title, weighted to the emphasised word",
        body=lambda p: f'''
  <div class="inner">
    <div class="idx">{COPY["idx"]}</div>
    <div class="title">{COPY["title"]}<div class="swell"></div></div>
    <div class="does">{COPY["does"]}</div>
    <div class="got"><b>{COPY["got_bold"]}</b> {COPY["got_plain"]}</div>
  </div>'''),

    "invert": dict(
        note="the payload half inverts — ground becomes ink — so the result detonates",
        body=lambda p: f'''
  <div class="inner">
    <div class="half-top">
      <div class="idx">{COPY["idx"]}</div>
      <div class="title">{COPY["title"]}</div>
    </div>
    <div class="half-pay">
      <div class="does">{COPY["does"]}</div>
      <div class="got"><b>{COPY["got_bold"]}</b> {COPY["got_plain"]}</div>
    </div>
  </div>'''),

    "bleed": dict(
        note="a colour field radiates FROM the emphasised phrase, as if the word stained the page",
        body=lambda p: f'''
  <div class="bleed"></div>
  <div class="inner">
    <div class="idx">{COPY["idx"]}</div>
    <div class="title">{COPY["title"]}</div>
    <div class="does">{COPY["does"]}</div>
    <div class="got"><b>{COPY["got_bold"]}</b> {COPY["got_plain"]}</div>
  </div>'''),
}


def css(p, treatment):
    bg, ink, acc = p["bg"], p["ink"], p["acc"]
    base = f"""
 .slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; background:{bg}; color:{ink};
   font-family:"Segoe UI",Arial,sans-serif; }}
 .inner {{ position:relative; z-index:3; height:100%; display:flex; flex-direction:column; padding:84px 76px 132px; }}
 .idx {{ font-family:Consolas,Menlo,monospace; font-size:26px; letter-spacing:.34em; text-transform:uppercase; color:{acc}; margin-bottom:26px; }}
 .title {{ font-size:92px; font-weight:800; line-height:1.02; letter-spacing:-.01em; position:relative; }}
 .does {{ margin-top:96px; font-size:42px; line-height:1.34; font-weight:600; max-width:900px; }}
 .got {{ margin-top:24px; font-size:36px; line-height:1.36; max-width:900px; opacity:.92; }}
 .got b {{ color:{acc}; font-weight:800; }}
 .brand {{ position:absolute; z-index:4; left:76px; bottom:56px; font-family:Consolas,Menlo,monospace;
   font-size:19px; letter-spacing:.18em; text-transform:uppercase; color:{ink}; opacity:.85; }}
 .brand i {{ display:block; font-style:normal; font-size:14px; letter-spacing:.3em; color:{acc}; }}
"""
    extra = {
        "knockout": f"""
 .ko-field {{ position:absolute; inset:0; background:{acc}; z-index:1; }}
 .inner {{ mix-blend-mode:normal; }}
 .slide {{ background:{bg}; }}
 .title.ko {{ color:{bg}; background:{acc}; box-decoration-break:clone; padding:.06em .18em; margin-left:-.18em; }}
 .idx, .does, .got {{ position:relative; z-index:3; color:{bg}; }}
 .got b {{ color:{bg}; text-decoration:underline; text-decoration-thickness:6px; }}
 .brand {{ color:{bg}; }} .brand i {{ color:{bg}; opacity:.7; }}
""",
        "highlighter": f"""
 .hl {{ background:{acc}; color:{bg}; padding:.02em .16em; box-decoration-break:clone; }}
 .hl b {{ color:{bg}; }}
""",
        "ghost": f"""
 .ghost {{ position:absolute; z-index:1; right:-80px; top:120px; font-size:520px; font-weight:900;
   line-height:.8; color:{acc}; opacity:.13; letter-spacing:-.04em; }}
""",
        "swell": f"""
 .swell {{ position:absolute; left:0; bottom:-26px; width:62%; height:22px; background:{acc};
   border-radius:2px; }}
 .swell::after {{ content:""; position:absolute; left:62%; top:6px; width:22%; height:10px; background:{acc}; opacity:.55; }}
""",
        "invert": f"""
 .inner {{ padding:0; }}
 .half-top {{ padding:84px 76px 60px; flex:1; display:flex; flex-direction:column; justify-content:center; }}
 .half-pay {{ background:{ink}; color:{bg}; padding:60px 76px 140px; }}
 .half-pay .does {{ margin-top:0; }}
 .half-pay .got {{ opacity:1; }}
 .half-pay .got b {{ color:{accent_for(ink, acc)}; }}
 .brand {{ color:{bg}; }} .brand i {{ color:{accent_for(ink, acc)}; }}
""",
        "bleed": f"""
 .bleed {{ position:absolute; inset:0; z-index:1;
   background: radial-gradient(58% 42% at 22% 74%, {acc} 0%, transparent 62%); opacity:.30; }}
""",
    }[treatment]
    return base + extra


def slide(p, treatment):
    return (f'<div class="slide">{TREATMENTS[treatment]["body"](p)}'
            f'<div class="brand">Your Name<i>Your Business</i></div></div>')


def render_all():
    OUT.mkdir(exist_ok=True)
    made = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)

        # A. one treatment, every palette — isolate COLOUR
        for name, p in PALETTES.items():
            doc = f"<!doctype html><meta charset='utf-8'><style>{css(p,'highlighter')}</style>{slide(p,'highlighter')}"
            f = OUT / f"_lab-pal-{name}.html"; f.write_text(doc, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(160)
            pg.locator(".slide").screenshot(path=str(OUT / f"lab-pal-{name}.png"))
            made.append(("palette", name))

        # B. one strong palette, every treatment — isolate STRUCTURE
        p = PALETTES["indigo"]   # the strongest-popping palette, for isolating STRUCTURE
        for t in TREATMENTS:
            doc = f"<!doctype html><meta charset='utf-8'><style>{css(p,t)}</style>{slide(p,t)}"
            f = OUT / f"_lab-tr-{t}.html"; f.write_text(doc, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(160)
            pg.locator(".slide").screenshot(path=str(OUT / f"lab-tr-{t}.png"))
            made.append(("treatment", t))
        b.close()
    return made


def sheet():
    rows = []
    for name, p in sorted(PALETTES.items(), key=lambda kv: -score(kv[1])["pop"]):
        s = score(p)
        rows.append((name, p, s))

    pal_cards = "".join(f'''
  <figure class="{ 'fail' if s['verdict'].startswith('FAIL') else '' }">
    <div class="feed"><img src="lab-pal-{n}.png"></div>
    <figcaption>
      <b>{n}</b><span>{html.escape(p['note'])}</span>
      <table>
        <tr><td>pop vs feed (ΔE)</td><td class="num">{s['pop']:.0f}</td></tr>
        <tr><td>ink on ground</td><td class="num">{s['legible']:.1f}:1</td></tr>
        <tr><td>accent on ground</td><td class="num">{s['acc_legible']:.1f}:1</td></tr>
        <tr><td>verdict</td><td class="num v">{s['verdict']}</td></tr>
      </table>
    </figcaption>
  </figure>''' for n, p, s in rows)

    tr_cards = "".join(f'''
  <figure><div class="feed"><img src="lab-tr-{t}.png"></div>
  <figcaption><b>{t}</b><span>{html.escape(TREATMENTS[t]["note"])}</span></figcaption></figure>'''
                       for t in TREATMENTS)

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Feed lab</title><style>
 body{{margin:0;background:#101010;color:#eee;font-family:Segoe UI,Arial,sans-serif;padding:26px 30px 80px}}
 h1{{font-size:21px;margin:0 0 4px}} h2{{font-size:16px;margin:34px 0 4px}}
 p.l{{color:#9a9a9a;font-size:13px;max-width:920px;line-height:1.55;margin:0 0 18px}}
 .grid{{display:flex;flex-wrap:wrap;gap:20px}}
 figure{{margin:0;width:230px}} figure.fail{{opacity:.42}}
 .feed{{background:{FEED_LIGHT};padding:10px;border-radius:8px}}
 .feed img{{display:block;width:100%;border-radius:4px}}
 figcaption b{{display:block;font-size:14px;margin-top:8px}}
 figcaption span{{color:#8f8f8f;font-size:12px;display:block;margin-bottom:6px}}
 table{{width:100%;font-size:11.5px;color:#bbb;border-collapse:collapse}}
 td{{padding:1px 0}} td.num{{text-align:right;font-family:Consolas,Menlo,monospace;color:#eee}}
 td.v{{color:#ffd479}}
</style></head><body>
<h1>Feed lab — colour salience, and backgrounds that mould to the words</h1>
<p class="l">Every slide is shown sitting on the real LinkedIn feed ground (#F4F2EE), which is what it must break out of.
<b>Pop</b> is perceptual colour distance (ΔE) from that ground — how much the slide separates from the feed.
<b>Ink on ground</b> is WCAG contrast — legibility, which no amount of pop is allowed to buy. A palette that pops and cannot be read is a failure and is dimmed.
Two controls are included so the test can fail honestly: the current brand, and LinkedIn's own blue, which should blend.</p>

<h2>A · Which colours break the feed</h2>
<p class="l">One treatment, every palette, so colour is the only variable.</p>
<div class="grid">{pal_cards}</div>

<h2>B · Backgrounds derived from the words</h2>
<p class="l">This is not decoration, so it does not breach the coherence principle: that rule says a background either <i>means something</i> or recedes. A ground shaped by the text means something. One palette, every treatment, so structure is the only variable.</p>
<div class="grid">{tr_cards}</div>
</body></html>"""
    out = OUT / "feed-lab.html"
    out.write_text(doc, encoding="utf-8")
    return out, rows


if __name__ == "__main__":
    render_all()
    out, rows = sheet()
    print(f"{'palette':12} {'pop':>5} {'ink':>6} {'accent':>7}  verdict")
    for n, p, s in rows:
        print(f"{n:12} {s['pop']:5.0f} {s['legible']:6.1f} {s['acc_legible']:7.1f}  {s['verdict']}")
    print(f"\nsheet -> {out}")
    # Opens the page in the member's own default browser.
    if webbrowser.open(out.as_uri()):
        print("opened in your browser")
