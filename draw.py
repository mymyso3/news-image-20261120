#!/usr/bin/env python3
"""Draw entry.png: one-page summary of 20 November 2026 world news.

Deterministic: no clock, no randomness. Same script -> same bytes.
4 stories, 3 continents (Asia x2, Europe x1, North America x1).
Title: 20 November 2026 - 4 Stories, 3 Continents, One Page - Hormuz Edition.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUT_PATH = "entry.png"
FONTS = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONTS + name, size)


TITLE_F = load("DejaVuSans-Bold.ttf", 62)
SUB_F = load("DejaVuSans-Bold.ttf", 30)
BADGE_F = load("DejaVuSans-Bold.ttf", 24)
CONT_F = load("DejaVuSans-Bold.ttf", 22)
NUM_F = load("DejaVuSans-Bold.ttf", 20)
HEAD_F = load("DejaVuSans-Bold.ttf", 27)
BODY_F = load("DejaVuSans.ttf", 21)
TAG_F = load("DejaVuSans-Bold.ttf", 18)

NAVY = (27, 42, 74)
CREAM = (247, 243, 234)
INK = (30, 30, 34)
BODY_GREY = (70, 70, 76)
GOLD = (201, 162, 39)
SEA = (226, 236, 242)
SEA_LINE = (200, 210, 218)
ORANGE = (232, 122, 54)
BLUE = (64, 120, 200)
GREEN = (46, 160, 120)
GREY_LAND = (196, 198, 192)
WHITE = (255, 255, 255)
CARD_LINE = (214, 210, 200)

STORIES = [
    {
        "n": 1,
        "head": "Ukraine hits Crimea bridge again",
        "body": "Putin drops the sea and energy ceasefire.",
        "tag": "EUROPE",
        "colour": BLUE,
    },
    {
        "n": 2,
        "head": "UN court: Myanmar genocide",
        "body": "Judges rule the state committed genocide against the Rohingya.",
        "tag": "ASIA",
        "colour": ORANGE,
    },
    {
        "n": 3,
        "head": "Tankers burn in Hormuz",
        "body": "Three oil tankers hit mines and catch fire; Iran escalates attacks.",
        "tag": "ASIA",
        "colour": ORANGE,
    },
    {
        "n": 4,
        "head": "Anthropic's $2tn IPO",
        "body": "Record debut on Nasdaq, the largest ever.",
        "tag": "NORTH AMERICA",
        "colour": GREEN,
    },
]

# Schematic flat shapes for the world map, in canvas coordinates.
# Only the three continents with stories are coloured; the rest are grey.
LAND = [
    ("North America",
     [(92, 238), (168, 196), (262, 194), (328, 222), (344, 262),
      (306, 298), (298, 334), (256, 330), (214, 304), (148, 294),
      (104, 268)],
     GREEN, (112, 206), "NORTH AMERICA"),
    ("South America",
     [(336, 368), (386, 354), (414, 384), (400, 438), (370, 488),
      (346, 458), (330, 408)],
     GREY_LAND, None, None),
    ("Europe",
     [(478, 226), (524, 200), (564, 210), (574, 240), (554, 270),
      (514, 276), (486, 260), (470, 244)],
     BLUE, (466, 190), "EUROPE"),
    ("Africa",
     [(486, 300), (546, 290), (594, 306), (604, 350), (584, 414),
      (544, 444), (506, 420), (480, 364), (476, 324)],
     GREY_LAND, None, None),
    ("Asia",
     [(608, 210), (698, 180), (798, 176), (888, 196), (948, 230),
      (954, 286), (904, 330), (844, 354), (760, 360), (690, 336),
      (630, 300), (600, 256)],
     ORANGE, (742, 238), "ASIA"),
    ("Oceania",
     [(830, 424), (884, 414), (918, 434), (904, 464), (854, 464),
      (826, 446)],
     GREY_LAND, None, None),
]

# Where each story happened on the map: (x, y, story number).
PINS = [
    (540, 246, 1),   # Crimea bridge, Black Sea, eastern Europe
    (836, 318, 2),   # Myanmar, south-east Asia
    (668, 298, 3),   # Strait of Hormuz, Persian Gulf
    (300, 266, 4),   # New York / Nasdaq, US east coast
]


def wrap_lines(text, font, max_width, draw):
    """Split text into lines that fit max_width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, text, font, y, colour):
    width = draw.textlength(text, font=font)
    draw.text(((CANVAS_W - width) / 2, y), text, font=font, fill=colour)


def draw_header(draw):
    draw.rectangle([0, 0, CANVAS_W, 168], fill=NAVY)
    draw.rectangle([0, 168, CANVAS_W, 174], fill=GOLD)
    centred(draw, "20 NOVEMBER 2026", TITLE_F, 14, WHITE)
    centred(draw, "4 Stories \u00b7 3 Continents \u00b7 One Page",
            SUB_F, 84, (214, 222, 235))
    badge = "HORMUZ EDITION"
    badge_w = draw.textlength(badge, font=BADGE_F) + 36
    bx = (CANVAS_W - badge_w) / 2
    draw.rounded_rectangle([bx, 124, bx + badge_w, 156], radius=15,
                           fill=GOLD, outline=NAVY, width=2)
    draw.text((bx + 18, 128), badge, font=BADGE_F, fill=NAVY)


def draw_map(draw):
    draw.rounded_rectangle([28, 186, 996, 566], radius=18,
                           fill=SEA, outline=SEA_LINE, width=2)
    for _name, shape, fill, _pos, _label in LAND:
        draw.polygon(shape, fill=fill, outline=WHITE, width=2)
    for _name, _shape, _fill, pos, label in LAND:
        if pos is None:
            continue
        x, y = pos
        draw.text((x + 1, y + 1), label, font=CONT_F, fill=WHITE)
        draw.text((x, y), label, font=CONT_F, fill=NAVY)
    for x, y, num in PINS:
        draw.ellipse([x - 15, y - 15, x + 15, y + 15],
                     fill=NAVY, outline=WHITE, width=3)
        label = str(num)
        lw = draw.textlength(label, font=NUM_F)
        draw.text((x - lw / 2, y - 11), label, font=NUM_F, fill=WHITE)


def draw_card(draw, story, x, y, w, h):
    colour = story["colour"]
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14,
                           fill=WHITE, outline=CARD_LINE, width=2)
    draw.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=colour)
    cx, cy = x + 44, y + 40
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=colour)
    num = str(story["n"])
    nw = draw.textlength(num, font=NUM_F)
    draw.text((cx - nw / 2, cy - 12), num, font=NUM_F, fill=WHITE)
    tx = x + 78
    hy = y + 18
    for line in wrap_lines(story["head"], HEAD_F, w - 100, draw):
        draw.text((tx, hy), line, font=HEAD_F, fill=INK)
        hy += 32
    sy = hy + 6
    for line in wrap_lines(story["body"], BODY_F, w - 100, draw):
        draw.text((tx, sy), line, font=BODY_F, fill=BODY_GREY)
        sy += 27
    tag = story["tag"]
    tag_w = draw.textlength(tag, font=TAG_F) + 26
    ty = y + h - 40
    draw.rounded_rectangle([tx, ty, tx + tag_w, ty + 28], radius=14,
                           fill=colour)
    draw.text((tx + 13, ty + 4), tag, font=TAG_F, fill=WHITE)


def main():
    image = Image.new("RGB", (CANVAS_W, CANVAS_H), CREAM)
    draw = ImageDraw.Draw(image)
    draw_header(draw)
    draw_map(draw)
    card_w, card_h = 466, 196
    spots = [(28, 582), (530, 582), (28, 792), (530, 792)]
    for story, (x, y) in zip(STORIES, spots):
        draw_card(draw, story, x, y, card_w, card_h)
    image.save(OUT_PATH, format="PNG")


if __name__ == "__main__":
    main()
