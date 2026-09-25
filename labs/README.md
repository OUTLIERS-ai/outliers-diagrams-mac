# The four programs that decide what a design looks like

Four small programs. Between them they replace the argument you would otherwise have about
colour, size and layout with numbers and pictures you can point at.

They were written in one week, each one the day after something went wrong. What they do is
in the file names. Why they exist is below.

---

## ten_design_systems.py

**Renders the same content in ten complete design systems, then builds one sheet with all
ten side by side.**

You cannot choose well from one option, and you cannot argue usefully about a description.
Ten built versions on one page turns a taste argument into pointing.

Each system carries its own colours, its own type and its own background language. Every
background is drawn by the program from a fixed starting number, so it costs nothing, renders
instantly, and comes out identical every time you run it.

**Change first:** the ten systems near the top. Replace them with the directions you are
actually choosing between.

---

## phone_width.py

**Renders the same page four ways and reduces every one to 380 pixels wide, which is roughly
what a phone gives you.**

Almost every visual mistake we have made was invisible at the size we were looking at it. A
page judged at full size on a monitor is being judged in conditions no reader will ever be
in.

The four versions here vary how much texture sits behind the words: none at all, a little at
the edges, a murmur, and full. That was the argument it was written to settle.

**Change first:** the four variants, to whatever you are actually deciding between.

---

## colour_measure.py

**Works out, for any set of colours, how different they look to a human eye against the
background they will sit on, and whether the words on them stay readable.**

Two numbers per candidate set, and the rule written into the file: **a set of colours that
stands out but cannot be read is a failure. Both numbers have to clear.**

It does not compare the colour values directly, which would mean nothing. It converts each
colour into a scale built to match how eyes actually perceive difference, then measures the
distance on that scale. The arithmetic is in the file, about sixty lines, and it is honest
about its own shortcut in a comment.

**Change first:** the background value at the top, to whatever your work will actually sit
on.

---

## what_a_background_is_for.py

**The one that argues with the person who wrote it.**

It opens by throwing out the previous day's work, and the reason is written in the file: the
colour work was a trap, because it was measurable and therefore it felt like progress.

Then it asks the harder question the measuring could not answer: what is a background
allowed to be? The standard it sets is one line long. **A background either means something
or it gets out of the way.**

It then applies that standard to its author's own work without mercy, labels the field of
joined dots as decoration, and says so in writing so it could be removed honestly rather than
defended.

**Read this one before you run it.** It is the most opinionated file here and the argument in
it is worth more than the output.

---

## Running any of them

First run the lines under "Running it" in the main README, which make the private Python
folder and install what these need. Then, from the main folder:

```
cd labs
source ~/outliers-diagrams-python/bin/activate && python ten_design_systems.py
source ~/outliers-diagrams-python/bin/activate && python colour_measure.py
```

Run the other 2 the same way, with their own file names. Some write pictures beside themselves,
some print numbers. Read the top of each file: every one states what it does and why it was
written in its first twenty lines.

## The order to use them in

1. **ten_design_systems.py** to see the options built rather than described.
2. **colour_measure.py** to clear the floor on the two or three you like.
3. **phone_width.py** to look at the survivors at the size they will really be seen.
4. **what_a_background_is_for.py** to decide whether anything behind the words has earned
   its place.

Then stop measuring. Contrast is a floor to clear, not a score to raise, and the measurable
half of a design decision will absorb a week while the decision that matters goes unmade.
