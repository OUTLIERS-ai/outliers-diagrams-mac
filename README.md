**This is the Mac version.** On Windows, use [outliers-diagrams](https://github.com/OUTLIERS-ai/outliers-diagrams).

# Diagrams drawn by a program

One file that draws ten diagrams from measurements, then measures its own labels and
refuses if any of them collide.

It is here because of a failure. Twenty three generated versions of a mark were rejected in
one day, and the finding underneath was that **an AI model cannot draw the same picture
twice and cannot draw crisp lettering.** For a post that is fine. For anything that has to
be identical every time it is fatal.

So: draw it with a program, from numbers.

## What is in the file

Ten drawings, each one replacing a paragraph that was doing the job badly. Under them sit
four ideas worth more than the pictures.

**Measurements, not shapes.** Every drawing is built from numbers set against one figure.
Change that figure and the whole drawing scales exactly, with no redrawing and no drift.

**One set of values at the top.** The colours and the two typefaces are declared once and
used by every drawing. Change a colour in one line and every picture changes with it.

**A type scale, set once, with its reason written beside it.** A drawing 1240 pixels wide
printed 166 millimetres wide puts a 17 pixel label at roughly 6pt against 10.2pt body text,
which is below the size anybody should be asked to read. Every label is scaled through one
constant rather than in forty separate calls.

**A label audit that refuses.** After the drawings render, it measures every label's real
extent and fails on two conditions: a label running off the canvas, and a label overlapping
another label. On its first run it found **fourteen faults that had been looked at and not
seen.**

## The honest limit, and it matters more than the check

The audit compares labels with each other and with the edge of the canvas. **It cannot see
a line drawn through a box**, and it passed a picture that had one. That was found by
looking at the picture.

A check removes the part you can automate. It does not remove looking.

## Also in here: the four programs that decide what a design looks like

`labs/` carries four more programs, each written the day after something went wrong.

- **ten_design_systems.py** renders the same content in ten complete design systems, side by
  side on one sheet, so choosing becomes pointing rather than arguing.
- **colour_measure.py** works out how different a colour looks to a human eye against the
  background it will sit on, and whether the words on it stay readable. Both numbers have to
  clear.
- **phone_width.py** renders the same page four ways and reduces each to 380 pixels wide,
  which is what a phone gives you. Almost every visual mistake is invisible at the size you
  were looking at it.
- **what_a_background_is_for.py** opens by throwing out the previous day's work, and sets one
  standard: a background either means something or it gets out of the way.

`labs/README.md` says what each one is for and the order to use them in.

## Running it

Needs Python, Playwright and a browser Playwright can drive. 1 of the 4 programs in `labs/`
also needs Pillow, which reads and shrinks pictures. On a Mac they go into a private Python
folder, `~/outliers-diagrams-python`, which works whichever Python your Mac uses. The first
line below makes it; each line after it starts by switching into it. From this folder:

```
python3 -m venv ~/outliers-diagrams-python
source ~/outliers-diagrams-python/bin/activate && python -m pip install pillow playwright
source ~/outliers-diagrams-python/bin/activate && python -m playwright install chromium
source ~/outliers-diagrams-python/bin/activate && python make_diagrams.py
```

Pictures are written to `png/`. The audit prints as it goes and the run exits non-zero if
any label fails, so it can sit inside a build that refuses.

## Making it yours

Change `PAPER`, `INK`, `OX`, `BRASS`, `MUT` and `LINE` at the top to your own colours, and
`SERIF` and `MONO` to typefaces that exist on the machines your readers use. A typeface that
is not on the reader's computer is a typeface your document does not have.

Then write your own drawing as a function that returns `svg(width, height, parts)`, and add
it to the `DIAGRAMS` dictionary at the bottom. The helpers for text, boxes, lines and arrows
are at the top of the file and are the whole vocabulary.

The audit runs on whatever you add, without being told about it.

This repo is made automatically from outliers-diagrams@ca1e42e. To report a problem or suggest a change, use that repo, not this one.
