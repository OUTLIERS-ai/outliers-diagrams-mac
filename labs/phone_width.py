"""How clean should the background be? Four levels, same slide, judged at phone size.

Ashley, 2026-07-10: *"I think the cleaner the background the better."*
This is the coherence principle (Carousel-Craft-Doctrine-V3 §2c) taken to its conclusion:
decoration lowers comprehension on instructional material. The question is only how far to go.

    flat      — nothing. Ground colour, type, brand. Zero texture.
    edge      — texture confined to the margins; the type sits on clean ground.
    whisper   — the current abstract field, dropped to a murmur (opacity .18)
    texture   — what b01 ships today (opacity .9 under a light scrim)

Renders one item slide at each level, shrinks each to 380px (the size it is actually read),
and builds a side-by-side sheet. No image generation, no cost, instant.
"""
from __future__ import annotations

import html
import importlib.util
import json
import sys
import webbrowser
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
# The example slides that travel with this file, so it runs the moment it is cloned.
SPEC = HERE / "example-slides.json"
OUT = HERE / "_gallery"
W, H = 1080, 1350

# ten_design_systems.py was called themes.py until it was renamed for readability.
spec_mod = importlib.util.spec_from_file_location(
    "ten_design_systems", HERE / "ten_design_systems.py")
themes = importlib.util.module_from_spec(spec_mod)
sys.modules["ten_design_systems"] = themes
spec_mod.loader.exec_module(themes)

PALETTE = {"accent": "#C9A25B", "accent2": "#B08A3E", "bg": "#151515", "ink": "#F3EEE3"}

LEVELS = {
    "flat":    dict(opacity=0.0,  mask=None,   note="nothing at all. type on ground."),
    "edge":    dict(opacity=0.55, mask="edge", note="texture at the margins only; type on clean ground"),
    "whisper": dict(opacity=0.18, mask=None,   note="the field, dropped to a murmur"),
    "texture": dict(opacity=0.90, mask=None,   note="what b01 ships today"),
}

SEAL = ('<svg width="46" height="46" viewBox="0 0 190 190">'
        '<circle cx="95" cy="95" r="88" stroke="#F3EEE3" stroke-width="7" fill="none"/>'
        '<circle cx="95" cy="95" r="46" stroke="#F3EEE3" stroke-width="22" fill="none"/>'
        '<circle cx="158" cy="31" r="13" fill="#C9A25B"/></svg>')


def bg_svg(level: str) -> str:
    cfg = LEVELS[level]
    if cfg["opacity"] == 0:
        return ""
    inner = themes.bg_nodes(PALETTE, seed=17)
    mask = ""
    if cfg["mask"] == "edge":
        # keep texture only near the edges: a soft black hole over the middle
        mask = ('<defs><radialGradient id="hole"><stop offset="0" stop-color="#000" stop-opacity="1"/>'
                '<stop offset=".62" stop-color="#000" stop-opacity="1"/>'
                '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
                f'<rect width="{W}" height="{H}" fill="url(#hole)"/>')
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
            f'style="position:absolute;inset:0;width:100%;height:100%;opacity:{cfg["opacity"]}">'
            f'{inner}{mask}</svg>')


def slide(level: str, s: dict) -> str:
    return f'''<div class="slide">{bg_svg(level)}
  <div class="inner">
    <div class="idx">{html.escape(s["idx"])}</div>
    <div class="title">{html.escape(s["title"])}</div>
    <div class="does">{html.escape(s["does"])}</div>
    <div class="got">{s["got"]}</div>
  </div>
  <div class="brand">{SEAL}<div class="bn">Your Name<small>Your Business</small></div></div>
  <div class="count">3 / 10</div>
</div>'''


CSS = f"""
 body {{ margin:0; background:#111; }}
 .slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; background:#151515;
   color:#F3EEE3; font-family:Constantia,Georgia,serif; display:flex; flex-direction:column; }}
 .inner {{ position:relative; z-index:2; flex:1; display:flex; flex-direction:column; padding:84px 76px 132px; }}
 .idx {{ font-family:Consolas,Menlo,monospace; font-size:26px; letter-spacing:.34em; text-transform:uppercase;
   color:#C9A25B; margin-bottom:26px; }}
 .title {{ font-size:88px; font-weight:700; line-height:1.05; }}
 .does {{ margin-top:auto; padding-top:38px; font-size:42px; line-height:1.34; font-weight:600; max-width:900px; }}
 .got {{ margin-top:24px; font-style:italic; color:#B9B2A4; font-size:36px; line-height:1.34; max-width:900px; }}
 .got b {{ color:#C9A25B; font-style:normal; font-weight:700; }}
 .brand {{ position:absolute; z-index:3; left:76px; bottom:56px; display:flex; align-items:center; gap:16px; }}
 .bn {{ font-family:Consolas,Menlo,monospace; font-size:20px; letter-spacing:.2em; text-transform:uppercase; line-height:1.2; }}
 .bn small {{ display:block; font-size:15px; letter-spacing:.3em; color:#C9A25B; }}
 .count {{ position:absolute; z-index:3; right:76px; bottom:60px; font-family:Consolas,Menlo,monospace;
   font-size:22px; letter-spacing:.22em; color:#B9B2A4; opacity:.8; }}
"""


def main():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    item = next(s for s in spec["slides"] if s.get("role") == "item")
    OUT.mkdir(exist_ok=True)

    shots = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for lvl in LEVELS:
            doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{slide(lvl, item)}</body></html>"
            p = OUT / f"_clean-{lvl}.html"
            p.write_text(doc, encoding="utf-8")
            pg.goto(p.as_uri()); pg.wait_for_timeout(250)
            png = OUT / f"clean-{lvl}.png"
            pg.locator(".slide").screenshot(path=str(png))
            # the acceptance test: the size it is actually read
            im = Image.open(png)
            im.resize((380, int(380 * im.height / im.width)), Image.LANCZOS).save(OUT / f"clean-{lvl}-phone.png")
            shots.append(lvl)
            print(f"  {lvl:8} rendered")
        b.close()

    cards = "".join(
        f'<figure><img src="clean-{l}-phone.png"><figcaption><b>{l}</b><span>{html.escape(LEVELS[l]["note"])}</span></figcaption></figure>'
        for l in shots)
    sheet = f"""<!doctype html><html><head><meta charset="utf-8"><title>How clean?</title><style>
 body{{margin:0;background:#1a1a1a;color:#eee;font-family:Segoe UI,Arial,sans-serif;padding:26px 30px}}
 h1{{font-size:20px;margin:0 0 4px}} p.l{{color:#9a9a9a;font-size:13px;margin:0 0 22px;max-width:840px;line-height:1.5}}
 .row{{display:flex;gap:22px}} figure{{margin:0}} img{{display:block;border:1px solid #333;border-radius:6px}}
 figcaption{{padding-top:8px;display:flex;flex-direction:column}} figcaption b{{font-size:14px}}
 figcaption span{{color:#8f8f8f;font-size:12px}}
</style></head><body>
<h1>How clean should the background be?</h1>
<p class="l">Same slide, four levels, each shown at 380px — the size a slide is actually read on a phone in the feed. The coherence principle says decoration lowers comprehension on teaching material while raising how much people like it. So the question is not whether to recede, but how far.</p>
<div class="row">{cards}</div>
</body></html>"""
    out = OUT / "how-clean.html"
    out.write_text(sheet, encoding="utf-8")
    print(f"sheet -> {out}")

    # Opens the page in the member's own default browser.
    if webbrowser.open(out.as_uri()):
        print("opened in your browser")


if __name__ == "__main__":
    main()
