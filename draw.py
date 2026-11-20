#!/usr/bin/env python3
"""One-page picture of Friday 20 November 2026: four stories, three continents.

Drawn fresh with Pillow. No clock, no random numbers, so running it twice
writes the same file both times. Title: 20 November 2026, 4 Stories,
3 Continents, One Page, Hormuz Edition.
"""
from PIL import Image as Canvas
from PIL import ImageDraw as Pen
from PIL import ImageFont as Type

PAGE = 1024

PAINT = {
    "navy": (27, 42, 74),
    "cream": (247, 243, 234),
    "ink": (30, 30, 34),
    "grey": (70, 70, 76),
    "gold": (201, 162, 39),
    "sea": (226, 236, 242),
    "sea_edge": (200, 210, 218),
    "orange": (232, 122, 54),
    "blue": (64, 120, 200),
    "green": (46, 160, 120),
    "flat": (196, 198, 192),
    "white": (255, 255, 255),
    "card_edge": (214, 210, 200),
    "soft": (214, 222, 235),
}


def typeface(bold, px):
    stem = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return Type.truetype("/usr/share/fonts/truetype/dejavu/" + stem, px)


BIG = typeface(True, 62)
SUB = typeface(True, 30)
EDITION = typeface(True, 24)
PLACE = typeface(True, 22)
PIN = typeface(True, 20)
HEAD = typeface(True, 27)
BODY = typeface(False, 21)
TAG = typeface(True, 18)

# One tuple per story: number, headline, one-line summary, continent, colour.
NEWS = [
    (1, "Ukraine hits Crimea bridge again",
     "Putin abandons the sea and energy ceasefire.",
     "EUROPE", (64, 120, 200)),
    (2, "UN court rules Myanmar genocide",
     "Judges rule the state committed genocide against the Rohingya.",
     "ASIA", (232, 122, 54)),
    (3, "Tankers burn in Hormuz",
     "Three oil tankers hit mines and catch fire; Iran escalates attacks.",
     "ASIA", (232, 122, 54)),
    (4, "Anthropic's $2tn IPO",
     "Record debut on Nasdaq, the largest ever.",
     "NORTH AMERICA", (46, 160, 120)),
]

# Schematic land shapes: outline, fill, label position (or None), label text.
LAND = {
    "North America": (
        [(88, 240), (150, 200), (240, 192), (320, 214), (350, 250),
         (330, 290), (300, 330), (260, 336), (220, 306), (160, 296),
         (110, 272)],
        (46, 160, 120), (104, 198), "NORTH AMERICA"),
    "South America": (
        [(340, 372), (392, 358), (420, 388), (404, 444), (372, 494),
         (344, 462), (328, 412)],
        (196, 198, 192), None, None),
    "Europe": (
        [(474, 228), (516, 202), (556, 208), (572, 236), (560, 266),
         (522, 278), (490, 264), (468, 246)],
        (64, 120, 200), (456, 184), "EUROPE"),
    "Africa": (
        [(488, 302), (548, 292), (596, 308), (606, 352), (586, 416),
         (546, 446), (508, 422), (482, 366), (478, 326)],
        (196, 198, 192), None, None),
    "Asia": (
        [(606, 212), (696, 182), (796, 178), (886, 198), (946, 232),
         (952, 288), (902, 332), (842, 356), (758, 362), (688, 338),
         (628, 302), (598, 258)],
        (232, 122, 54), (740, 236), "ASIA"),
    "Oceania": (
        [(828, 426), (882, 416), (916, 436), (902, 466), (852, 466),
         (824, 448)],
        (196, 198, 192), None, None),
}

# Where each story happened: (x, y, story number).
PINS = ((544, 248, 1), (836, 318, 2), (680, 296, 3), (300, 266, 4))


def fit(d, s, f, width):
    """Break a string into lines no wider than width pixels."""
    out, line = [], ""
    for word in s.split():
        test = (line + " " + word).strip()
        if d.textlength(test, font=f) <= width:
            line = test
        elif line:
            out.append(line)
            line = word
        else:
            line = word
    if line:
        out.append(line)
    return out


def centre(d, s, f, y, fill):
    w = d.textlength(s, font=f)
    d.text(((PAGE - w) / 2, y), s, font=f, fill=fill)


def header(d):
    d.rectangle((0, 0, PAGE, 168), fill=PAINT["navy"])
    d.rectangle((0, 168, PAGE, 174), fill=PAINT["gold"])
    centre(d, "20 NOVEMBER 2026", BIG, 14, PAINT["white"])
    centre(d, "4 Stories \u00b7 3 Continents \u00b7 One Page", SUB, 84,
           PAINT["soft"])
    label = "HORMUZ EDITION"
    lw = d.textlength(label, font=EDITION) + 36
    x0 = (PAGE - lw) / 2
    d.rounded_rectangle((x0, 124, x0 + lw, 156), radius=15,
                        fill=PAINT["gold"], outline=PAINT["navy"], width=2)
    d.text((x0 + 18, 128), label, font=EDITION, fill=PAINT["navy"])


def world(d):
    d.rounded_rectangle((28, 186, 996, 566), radius=18, fill=PAINT["sea"],
                        outline=PAINT["sea_edge"], width=2)
    for shape, fill, _pos, _tag in LAND.values():
        d.polygon(shape, fill=fill, outline=PAINT["white"], width=2)
    for _shape, _fill, pos, tag in LAND.values():
        if pos is None:
            continue
        d.text((pos[0] + 1, pos[1] + 1), tag, font=PLACE,
               fill=PAINT["white"])
        d.text(pos, tag, font=PLACE, fill=PAINT["navy"])
    for x, y, n in PINS:
        d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=PAINT["navy"],
                  outline=PAINT["white"], width=3)
        s = str(n)
        sw = d.textlength(s, font=PIN)
        d.text((x - sw / 2, y - 11), s, font=PIN, fill=PAINT["white"])


def card(d, story, x, y, w, h):
    n, head, body, tag, colour = story
    d.rounded_rectangle((x, y, x + w, y + h), radius=14,
                        fill=PAINT["white"], outline=PAINT["card_edge"],
                        width=2)
    d.rectangle((x, y, x + 10, y + h), fill=colour)
    cx, cy = x + 44, y + 40
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=colour)
    s = str(n)
    sw = d.textlength(s, font=PIN)
    d.text((cx - sw / 2, cy - 12), s, font=PIN, fill=PAINT["white"])
    tx = x + 78
    hy = y + 18
    for line in fit(d, head, HEAD, w - 100):
        d.text((tx, hy), line, font=HEAD, fill=PAINT["ink"])
        hy += 32
    sy = hy + 6
    for line in fit(d, body, BODY, w - 100):
        d.text((tx, sy), line, font=BODY, fill=PAINT["grey"])
        sy += 27
    tw = d.textlength(tag, font=TAG) + 26
    ty = y + h - 40
    d.rounded_rectangle((tx, ty, tx + tw, ty + 28), radius=14, fill=colour)
    d.text((tx + 13, ty + 4), tag, font=TAG, fill=PAINT["white"])


def build():
    canvas = Canvas.new("RGB", (PAGE, PAGE), PAINT["cream"])
    d = Pen.Draw(canvas)
    header(d)
    world(d)
    spots = ((28, 582), (530, 582), (28, 792), (530, 792))
    for story, (x, y) in zip(NEWS, spots):
        card(d, story, x, y, 466, 196)
    canvas.save("entry.png", "PNG")


build()
