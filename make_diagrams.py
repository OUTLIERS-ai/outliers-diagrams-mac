# -*- coding: utf-8 -*-
"""Diagrams for "Making Your Own Collateral".

Same palette, same drawing conventions and the same standing rule as the week one, week
two and session three sets: no label may overlap a line or another label, so every label
extent is placed against the geometry rather than eyeballed.

Six, and each one replaces prose rather than decorating it:

  s5-two-jobs    sameness and variety are opposite jobs, so they take opposite makers
  s5-thrash      why reacting to new versions cannot converge, and what does
  s5-sizes       the same mark at the three sizes it is actually judged at
  s5-mark        the mark written as measurements, which is why it can be rebuilt
  s5-colour      standing out and being readable are two numbers, and both must clear
  s5-four-ways   the four ways a decision sticks, and where each one fails

Rendered through the browser rather than a converter so the typeface matches the
documents and the decks.

    python3 make_diagrams.py          (on Windows: python make_diagrams.py)

Run it from the folder this file is in.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
# Beside this file, not above it. The original lived in a vault folder where the
# pictures belonged one level up; here that would write outside the folder the reader
# cloned, and they would find nothing.
PNG = HERE / "png"
PNG.mkdir(parents=True, exist_ok=True)

PAPER, INK, OX, BRASS, MUT, LINE = "#F3EEE3", "#14110C", "#6E1A18", "#B08A3E", "#5A5145", "#B3A78E"
VELLUM = "#E7DEC9"
SERIF = "Constantia,Georgia,serif"
# Menlo, the Mac's own, comes after Consolas, so drawings made where Consolas exists do not change.
MONO = "Consolas,Menlo,monospace"


# A drawing 1240 wide is printed 166mm wide, so a 17px label lands near 6pt against 10.2pt
# body text. That is below the legibility floor this document argues for, so every label is
# scaled once here rather than in forty separate calls.
TYPE = 1.34


def txt(x, y, s, size=17, fill=INK, anchor="middle", weight="400", font=SERIF, italic=False):
    size = round(size * TYPE, 1)
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}"{st}>{s}</text>')


def box(x, y, w, h, stroke=INK, sw=2.6, fill="none"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, colour=LINE, sw=2.0, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{colour}" '
            f'stroke-width="{sw}"{d}/>')


def arrow(x1, y1, x2, y2, colour=INK, sw=2.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    head = (f'<path d="M {x2} {y2} L {x2-13} {y2-6} L {x2-13} {y2+6} Z" fill="{colour}"/>'
            if y1 == y2 else
            f'<path d="M {x2} {y2} L {x2-6} {y2-13} L {x2+6} {y2-13} Z" fill="{colour}"/>')
    return (f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{colour}" '
            f'stroke-width="{sw}"{d}/>' + head)


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{PAPER}"/>'
            + "".join(body) + "</svg>")


def mark(cx, cy, r, ring=True):
    """The mark itself, drawn from the same measurements the real one uses."""
    import math
    o = []
    if ring:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" '
                 f'stroke-width="{r*0.035:.2f}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.56:.2f}" fill="none" stroke="{INK}" '
             f'stroke-width="{r*0.56*0.20:.2f}"/>')
    a = math.radians(46)
    px, py = cx + r * math.cos(a), cy + r * math.sin(a)
    o.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r*0.115:.2f}" fill="{OX}"/>')
    return o


# ------------------------------------------------------------------ 1. two jobs
def d_two_jobs():
    W, H = 1240, 430
    o = []
    o.append(box(60, 70, 520, 300, INK, 3.0))
    o.append(box(660, 70, 520, 300, OX, 3.0))
    o.append(txt(320, 48, "COLLATERAL", 20, INK, "middle", "600", MONO))
    o.append(txt(920, 48, "CONTENT", 20, OX, "middle", "600", MONO))

    o.append(txt(320, 128, "The material itself", 21, INK))
    o.append(txt(320, 166, "mark, colours, typefaces,", 17, MUT))
    o.append(txt(320, 196, "documents, decks, site", 17, MUT))
    o.append(txt(920, 128, "What you publish", 21, OX))
    o.append(txt(920, 166, "posts, replies, articles,", 17, MUT))
    o.append(txt(920, 196, "videos", 17, MUT))

    o.append(line(90, 218, 550, 218, LINE, 1.6))
    o.append(line(690, 218, 1150, 218, LINE, 1.6))

    o.append(txt(320, 252, "Must come out", 17, MUT))
    o.append(txt(320, 298, "IDENTICAL", 32, INK, "middle", "600", MONO))
    o.append(txt(320, 336, "every single time", 17, MUT))
    o.append(txt(920, 252, "Must come out", 17, MUT))
    o.append(txt(920, 298, "DIFFERENT", 32, OX, "middle", "600", MONO))
    o.append(txt(920, 336, "every single time", 17, MUT))

    o.append(arrow(320, 384, 320, 412, INK, 2.6))
    o.append(arrow(920, 384, 920, 412, OX, 2.6))
    return svg(W, H + 60, o + [
        txt(320, 462, "So a PROGRAM makes it", 21, INK, "middle", "600"),
        txt(920, 462, "So a MODEL makes it", 21, OX, "middle", "600"),
    ])


# ------------------------------------------------------------------ 2. the thrash
def d_thrash():
    W, H = 1240, 480
    o = []
    # top band: the oscillation
    o.append(txt(60, 44, "Reacting to a new version each time", 20, OX, "start", "600"))
    o.append(line(60, 150, 1180, 150, LINE, 1.4, "5 5"))
    o.append(txt(60, 82, "too rigid", 16, MUT, "start"))
    o.append(txt(60, 228, "too loose", 16, MUT, "start"))
    pts = [(200, 95), (300, 210), (400, 92), (500, 215), (600, 90), (700, 218),
           (800, 94), (900, 212), (1000, 96), (1100, 208)]
    d = "M 160 150 " + " ".join("L %d %d" % p for p in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{OX}" stroke-width="2.6"/>')
    for x, y in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{OX}"/>')
    o.append(txt(620, 268, "twenty three versions, ten hours, none usable", 17, MUT, "middle",
                 "400", SERIF, True))

    # bottom band: settle then step
    o.append(txt(60, 340, "Settling the direction first, then small steps", 20, INK, "start", "600"))
    o.append(box(160, 366, 210, 74, INK, 3.0, VELLUM))
    o.append(txt(265, 400, "Direction", 19, INK, "middle", "600"))
    o.append(txt(265, 424, "settled and kept", 14, MUT))
    step = [(470, 425), (600, 412), (730, 400), (860, 392), (990, 388)]
    o.append(arrow(380, 403, 452, 403, INK, 2.2))
    prev = (470, 425)
    for x, y in step:
        o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}"/>')
        if (x, y) != prev:
            o.append(line(prev[0], prev[1], x, y, INK, 2.4))
        prev = (x, y)
    o.append(f'<circle cx="1090" cy="386" r="11" fill="none" stroke="{OX}" stroke-width="3"/>')
    o.append(line(996, 388, 1079, 386, INK, 2.4))
    o.append(txt(1090, 358, "chosen", 16, OX, "middle", "600"))
    return svg(W, H, o)


# ------------------------------------------------------------------ 3. the three sizes
def d_sizes():
    W, H = 1240, 360
    o = []
    o.append(txt(620, 46, "Judged where it actually lives, not where it is shown to you",
                 21, INK, "middle", "600"))
    specs = [(300, 112, "112 px", "a post"), (640, 56, "56 px", "a comment"),
             (940, 32, "32 px", "a browser tab")]
    for cx, px, lbl, where in specs:
        o += mark(cx, 190, px / 2)
        o.append(txt(cx, 300, lbl, 19, INK, "middle", "600", MONO))
        o.append(txt(cx, 326, where, 16, MUT))
    o.append(line(1060, 120, 1060, 260, LINE, 1.4, "5 5"))
    o.append(txt(1105, 172, "If it dies here,", 18, OX, "start", "600"))
    o.append(txt(1105, 206, "it is not a logo", 18, OX, "start", "600"))
    return svg(W + 120, H, o)


# ------------------------------------------------------------------ 4. the mark as measurements
def d_mark():
    import math
    W, H = 1240, 560
    cx, cy, r = 430, 285, 200
    o = []
    o.append(txt(60, 48, "Written as measurements, so it is identical at any size for ever",
                 21, INK, "start", "600"))
    o += mark(cx, cy, r)
    # radius line
    o.append(line(cx, cy, cx, cy - r, BRASS, 2.0, "6 5"))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{BRASS}"/>')
    # angle to the point
    a = math.radians(46)
    px, py = cx + r * math.cos(a), cy + r * math.sin(a)
    o.append(line(cx, cy, px, py, BRASS, 2.0, "6 5"))
    o.append(line(cx, cy, cx + r + 40, cy, LINE, 1.6, "4 4"))

    # the four measurements, right hand column, no line crosses them
    rows = [
        ("Outer ring", "at the full radius, drawn 3.5% thick"),
        ("Letter O", "at 56% of the radius, drawn 20% thick"),
        ("The point", "46 degrees below centre, 11.5% of the radius"),
        ("Small version", "drops the outer ring, keeps the O and the point"),
    ]
    y = 150
    for k, v in rows:
        o.append(txt(760, y, k, 19, INK, "start", "600"))
        o.append(txt(760, y + 26, v, 16, MUT, "start"))
        y += 82
    o.append(line(742, 128, 742, 452, LINE, 1.6))
    o.append(txt(760, y + 6, "Anybody can rebuild it exactly.", 17, OX, "start", "600"))
    return svg(W, H, o)


# ------------------------------------------------------------------ 5. the colour test
def d_colour():
    W, H = 1240, 520
    x0, y0, w, h = 300, 90, 620, 360
    o = []
    o.append(box(x0, y0, w, h, LINE, 1.8))
    o.append(line(x0 + w / 2, y0, x0 + w / 2, y0 + h, LINE, 1.6))
    o.append(line(x0, y0 + h / 2, x0 + w, y0 + h / 2, LINE, 1.6))
    # axis labels, placed outside the box so nothing overlaps a line
    o.append(txt(x0 + w / 2, y0 + h + 46, "STANDS OUT FROM THE FEED", 17, INK, "middle",
                 "600", MONO))
    o.append(txt(x0 - 28, y0 + h / 2, "READABLE", 17, INK, "end", "600", MONO))
    o.append(txt(x0 - 28, y0 + h / 2 + 24, "on its own ground", 14, MUT, "end"))
    o.append(txt(x0 - 12, y0 + 16, "yes", 15, MUT, "end"))
    o.append(txt(x0 - 12, y0 + h - 6, "no", 15, MUT, "end"))
    o.append(txt(x0 + 10, y0 + h + 22, "no", 15, MUT, "start"))
    o.append(txt(x0 + w - 10, y0 + h + 22, "yes", 15, MUT, "end"))
    # quadrants
    o.append(txt(x0 + w * 0.25, y0 + h * 0.26, "Readable", 18, MUT))
    o.append(txt(x0 + w * 0.25, y0 + h * 0.26 + 34, "and ignored", 18, MUT))
    o.append(f'<rect x="{x0+w/2+2}" y="{y0+2}" width="{w/2-4}" height="{h/2-4}" '
             f'fill="{VELLUM}"/>')
    o.append(txt(x0 + w * 0.75, y0 + h * 0.26, "THE ONLY", 20, OX, "middle", "600", MONO))
    o.append(txt(x0 + w * 0.75, y0 + h * 0.26 + 38, "ONE THAT PASSES", 20, OX, "middle",
                 "600", MONO))
    o.append(txt(x0 + w * 0.25, y0 + h * 0.76, "Invisible", 18, MUT))
    o.append(txt(x0 + w * 0.75, y0 + h * 0.76, "Loud", 18, OX))
    o.append(txt(x0 + w * 0.75, y0 + h * 0.76 + 34, "and unreadable", 18, OX))
    o.append(txt(620, 52, "Two numbers, and both have to clear", 21, INK, "middle", "600"))
    o.append(txt(1000, y0 + h * 0.30, "A colour that stands out", 17, MUT, "start"))
    o.append(txt(1000, y0 + h * 0.30 + 34, "but cannot be read", 17, MUT, "start"))
    o.append(txt(1000, y0 + h * 0.30 + 68, "is a failure.", 17, MUT, "start"))
    return svg(W, H, o)


# ------------------------------------------------------------------ 6. four ways
def d_four_ways():
    W, H = 1240, 500
    o = []
    o.append(txt(60, 46, "Four ways to keep a decision, weakest first", 21, INK, "start", "600"))
    rows = [
        ("A note to yourself", "You intend to follow it", "Fails silently", MUT),
        ("A written standard", "Read before the work starts", "Fails silently", MUT),
        ("Values inside the renderer", "The colours are in the program that draws",
         "Cannot drift", INK),
        ("A refusal inside the builder", "It will not build at all", "Cannot be ignored", OX),
    ]
    y = 92
    for i, (k, v, note, colour) in enumerate(rows):
        strong = 2.0 + i * 0.9
        o.append(box(60, y, 660, 78, colour, strong, VELLUM if i >= 2 else "none"))
        o.append(txt(84, y + 34, k, 20, colour, "start", "600"))
        o.append(txt(84, y + 60, v, 16, MUT, "start"))
        o.append(txt(756, y + 46, note, 18, colour, "start", "600" if i >= 2 else "400"))
        y += 98
    o.append(line(736, 92, 736, 466, LINE, 1.6))
    o.append(arrow(40, 96, 40, 456, BRASS, 2.4))
    o.append(f'<text transform="rotate(-90 26 279)" x="26" y="279" text-anchor="middle" '
             f'font-family="{SERIF}" font-size="15" fill="{BRASS}" font-style="italic">'
             f'stronger</text>')
    return svg(W, H, o)



# ------------------------------------------------------------------ 7. render, not source
def d_render_not_source():
    W, H = 1240, 430
    o = []
    o.append(txt(620, 46, "Where a check looks decides what it can possibly find", 21, INK,
                 "middle", "600"))
    o.append(box(80, 100, 460, 240, LINE, 2.2))
    o.append(txt(310, 132, "READS THE FILE", 18, MUT, "middle", "600", MONO))
    o.append(line(110, 152, 510, 152, LINE, 1.4))
    for i, t in enumerate(["Spelling", "Forbidden words", "Broken markup"]):
        o.append(txt(310, 192 + i * 34, t, 17, MUT))
    o.append(txt(310, 312, "Cannot see the page", 17, OX, "middle", "600"))

    o.append(box(700, 100, 460, 240, OX, 3.0, VELLUM))
    o.append(txt(930, 132, "READS THE FINISHED PAGE", 18, OX, "middle", "600", MONO))
    o.append(line(730, 152, 1130, 152, BRASS, 1.4))
    for i, t in enumerate(["All of the above", "Text fallen off the bottom",
                           "A line that wrapped"]):
        o.append(txt(930, 192 + i * 34, t, 17, INK))
    o.append(txt(930, 312, "Sees what the reader sees", 17, OX, "middle", "600"))
    o.append(txt(620, 392, "A check that reports faults nobody can see is ignored within a week",
                 17, MUT, "middle", "400", SERIF, True))
    return svg(W, H, o)


# ------------------------------------------------------------------ 8. the safe area
def d_safe_area():
    W, H = 1240, 490
    bx, by, bw, bh = 180, 90, 880, 220
    o = []
    o.append(txt(620, 48, "A constraint said out loud, and the same constraint measured",
                 21, INK, "middle", "600"))
    # the banner
    o.append(box(bx, by, bw, bh, INK, 2.6, VELLUM))
    # profile picture position, bottom left
    o.append(f'<circle cx="{bx+110}" cy="{by+bh-10}" r="66" fill="{PAPER}" stroke="{OX}" '
             f'stroke-width="3"/>')
    o.append(txt(bx + 110, by + bh + 96, "profile picture", 15, OX, "middle", "600"))
    # the forbidden zone
    o.append(f'<rect x="{bx+2}" y="{by+bh-96}" width="212" height="94" fill="{OX}" '
             f'fill-opacity="0.10" stroke="{OX}" stroke-width="1.8" stroke-dasharray="6 5"/>')
    o.append(txt(bx + 330, by + 70, "No wording may be placed here", 18, OX, "start", "600"))
    o.append(txt(bx + 330, by + 100, "It is covered on every screen", 16, MUT, "start"))
    o.append(txt(bx + 330, by + 150, "Said in words: ignored the next morning", 16, MUT, "start"))
    o.append(txt(bx + 330, by + 178, "Measured in the drawing code: never again", 16, INK,
                 "start", "600"))
    o.append(txt(620, 450, "An instruction asks. A measurement decides.", 19, OX, "middle", "600"))
    return svg(W, H, o)


# ------------------------------------------------------------------ 9. the fixed page
def d_fixed_page():
    W, H = 1240, 470
    o = []
    o.append(txt(620, 46, "Why a page of fixed height loses work without telling you",
                 21, INK, "middle", "600"))
    for i, (x, title, colour) in enumerate([(200, "A page that flows", INK),
                                            (720, "A page of fixed height", OX)]):
        o.append(txt(x + 160, 92, title, 19, colour, "middle", "600"))
        o.append(box(x, 110, 320, 250, colour, 2.6))
        for j in range(6):
            o.append(line(x + 24, 142 + j * 30, x + 296, 142 + j * 30, LINE, 5.0))
    # flowing: continues onto a second page
    o.append(box(200, 372, 320, 60, INK, 2.6))
    o.append(line(224, 400, 496, 400, LINE, 5.0))
    o.append(txt(360, 452, "the rest moves down", 16, MUT))
    # fixed: cut
    o.append(f'<rect x="722" y="332" width="316" height="26" fill="{OX}" fill-opacity="0.14"/>')
    # the seventh line: written, inside the page, and about to be lost
    o.append(line(744, 346, 1016, 346, LINE, 5.0))
    # and the eighth, which never appears at all
    o.append(f'<path d="M 744 384 L 1016 384" stroke="{LINE}" stroke-width="5" '
             f'stroke-opacity="0.30"/>')
    o.append(line(720, 360, 1040, 360, OX, 3.0))
    o.append(txt(880, 400, "everything past this line", 16, OX, "middle", "600"))
    o.append(txt(880, 424, "is deleted, and nothing says so", 16, OX, "middle", "600"))
    return svg(W, H, o)


# ------------------------------------------------------------------ 10. what is which
def d_which_maker():
    W, H = 1240, 470
    o = []
    o.append(txt(620, 46, "Everything that makes the material, and what makes each one",
                 21, INK, "middle", "600"))
    o.append(box(70, 86, 540, 340, INK, 3.0))
    o.append(txt(340, 120, "PROGRAMS", 19, INK, "middle", "600", MONO))
    o.append(line(100, 138, 580, 138, LINE, 1.4))
    progs = ["Build every direction so they compare", "Render ten design systems side by side",
             "Reduce a page to phone width", "Measure colour and readability",
             "Draw the mark from measurements", "Render the documents and the decks",
             "The six checks"]
    for i, t in enumerate(progs):
        o.append(txt(100, 172 + i * 34, t, 16, MUT, "start"))
    o.append(txt(340, 408, "because sameness is the point", 16, INK, "middle", "600"))

    o.append(box(660, 86, 510, 340, OX, 3.0, VELLUM))
    o.append(txt(915, 120, "AGENTS", 19, OX, "middle", "600", MONO))
    o.append(line(690, 138, 1140, 138, BRASS, 1.4))
    o.append(txt(690, 178, "The judge", 18, OX, "start", "600"))
    o.append(txt(690, 204, "five independent passes over finished work", 15, MUT, "start"))
    o.append(txt(690, 254, "The site builder", 18, OX, "start", "600"))
    o.append(txt(690, 280, "works to a standard already set", 15, MUT, "start"))
    o.append(txt(690, 330, "And one that was refused", 18, MUT, "start", "600"))
    o.append(txt(690, 356, "taste cannot be automated", 15, MUT, "start"))
    o.append(txt(915, 408, "because judgement is not repetition", 16, OX, "middle", "600"))
    return svg(W, H, o)



# ------------------------------------------------------------------ 11. the nine steps
def d_nine_steps():
    """The whole process on one page, with both loops marked.

    Two rows rather than one line: nine boxes across a printed page would put every label
    below the legibility floor this document argues for elsewhere. The rework path runs in
    its own lane so it crosses no box, and every caption is short enough to sit inside the
    rectangle it belongs to.
    """
    W, H = 1240, 610
    o = []
    o.append(txt(620, 42, "The whole process, and the two places it loops",
                 21, INK, "middle", "600"))

    steps = [
        (1, "Second brain", "the foundation"),
        (2, "Research", "in one order"),
        (3, "Fan out", "not one at a time"),
        (4, "Design", "what good means"),
        (5, "The critic", "ways that disagree"),
        (6, "Visualisation", "draw, never generate"),
        (7, "Assembly", "words plus pictures"),
        (8, "Other formats", "deck, mark, banner"),
        (9, "Publish", ""),
    ]

    bw, bh, gap = 214, 104, 20
    row1_y, row2_y = 168, 392
    lane_rework = row1_y + bh + 26
    lane_down = row1_y + bh + 62
    pos = {}
    for i, (n, title, sub) in enumerate(steps):
        x = 60 + (i if i < 5 else i - 5) * (bw + gap)
        y = row1_y if i < 5 else row2_y
        pos[n] = (x, y)
        strong = n in (4, 5, 7)
        o.append(box(x, y, bw, bh, OX if strong else INK, 3.0 if strong else 2.2,
                     VELLUM if strong else "none"))
        o.append(txt(x + 15, y + 24, str(n), 16, BRASS, "start", "600", MONO))
        o.append(txt(x + bw / 2, y + 60, title, 18, OX if strong else INK, "middle", "600"))
        if sub:
            o.append(txt(x + bw / 2, y + 86, sub, 12, MUT))

    for a in (1, 2, 3, 4):
        xa = pos[a][0] + bw
        o.append(arrow(xa + 2, row1_y + bh / 2, xa + gap - 2, row1_y + bh / 2, LINE, 2.0))
    for a in (6, 7, 8):
        xa = pos[a][0] + bw
        o.append(arrow(xa + 2, row2_y + bh / 2, xa + gap - 2, row2_y + bh / 2, LINE, 2.0))

    x5c = pos[5][0] + bw / 2
    x6c = pos[6][0] + bw / 2
    o.append(line(x5c, row1_y + bh, x5c, lane_down, LINE, 2.0))
    o.append(line(x5c, lane_down, x6c, lane_down, LINE, 2.0))
    o.append(arrow(x6c, lane_down, x6c, row2_y - 2, LINE, 2.0))

    x4c = pos[4][0] + bw / 2
    o.append(f'<path d="M {x5c} {row1_y - 8} C {x5c} {row1_y - 66}, '
             f'{x4c} {row1_y - 66}, {x4c} {row1_y - 8}" fill="none" '
             f'stroke="{OX}" stroke-width="2.6"/>')
    o.append(f'<path d="M {x4c} {row1_y - 8} L {x4c - 6} {row1_y - 21} '
             f'L {x4c + 6} {row1_y - 21} Z" fill="{OX}"/>')
    o.append(txt((x4c + x5c) / 2, row1_y - 100, "YOU ARE THE GATE", 15, OX, "middle",
                 "600", MONO))
    o.append(txt((x4c + x5c) / 2, row1_y - 76, "it ends when you say so", 14, MUT))

    x7c = pos[7][0] + bw / 2
    y7b = row2_y + bh
    o.append(line(x7c, y7b + 4, x7c, y7b + 38, OX, 2.6, "7 5"))
    o.append(line(x7c, y7b + 38, 34, y7b + 38, OX, 2.6, "7 5"))
    o.append(line(34, y7b + 38, 34, lane_rework, OX, 2.6, "7 5"))
    o.append(line(34, lane_rework, x4c, lane_rework, OX, 2.6, "7 5"))
    o.append(arrow(x4c, lane_rework, x4c, row1_y + bh + 4, OX, 2.6))
    o.append(txt(x7c + 24, y7b + 66, "not good enough: back to rework", 16, OX, "start",
                 "600"))
    return svg(W, H, o)


DIAGRAMS = {
    "s5-two-jobs": d_two_jobs(),
    "s5-thrash": d_thrash(),
    "s5-sizes": d_sizes(),
    "s5-mark": d_mark(),
    "s5-colour": d_colour(),
    "s5-four-ways": d_four_ways(),
    "s5-render-not-source": d_render_not_source(),
    "s5-safe-area": d_safe_area(),
    "s5-fixed-page": d_fixed_page(),
    "s5-which-maker": d_which_maker(),
    "s5-nine-steps": d_nine_steps(),
}


def audit(pg, name, w, h):
    """Measure every label. Two rules, both mechanical rather than eyeballed:
    no label may run off the canvas, and no label may overlap another label."""
    boxes = pg.evaluate("""() => [...document.querySelectorAll('text')]
        .filter(t => !t.getAttribute('transform'))
        .map(t => {
        const b = t.getBBox();
        return {s: t.textContent.slice(0, 34), x: b.x, y: b.y, w: b.width, h: b.height};
    })""")
    bad = []
    for b in boxes:
        if b["x"] < -1 or b["y"] < -1 or b["x"] + b["w"] > w + 1 or b["y"] + b["h"] > h + 1:
            bad.append("OFF CANVAS  %-34s x=%d..%d y=%d..%d" %
                       (b["s"], b["x"], b["x"] + b["w"], b["y"], b["y"] + b["h"]))
    for i, a_ in enumerate(boxes):
        for b_ in boxes[i + 1:]:
            if (a_["x"] < b_["x"] + b_["w"] - 2 and b_["x"] < a_["x"] + a_["w"] - 2
                    and a_["y"] < b_["y"] + b_["h"] - 2 and b_["y"] < a_["y"] + a_["h"] - 2):
                bad.append("OVERLAP     %-34s <> %s" % (a_["s"], b_["s"]))
    for line in bad:
        print("    %s  %s" % (name, line))
    return len(bad)


def main():
    from playwright.sync_api import sync_playwright
    total = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for name, s in DIAGRAMS.items():
            f = PNG / ("_%s.svg.html" % name)
            f.write_text("<!doctype html><meta charset='utf-8'>"
                         "<style>*{margin:0;padding:0}body{background:%s}</style>%s"
                         % (PAPER, s), encoding="utf-8")
            m = re.search(r'width="(\d+)" height="(\d+)"', s)
            w, h = int(m.group(1)), int(m.group(2))
            pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            pg.goto(f.as_uri())
            pg.wait_for_timeout(350)
            out = PNG / (name + ".png")
            pg.screenshot(path=str(out))
            faults = audit(pg, name, w, h)
            pg.close()
            total += faults
            print("drew %-14s %4dx%-4d  %d KB%s"
                  % (name, w, h, out.stat().st_size / 1024,
                     "" if not faults else "   %d FAULTS" % faults))
        br.close()
    print("label audit: %d faults" % total)
    return total


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
