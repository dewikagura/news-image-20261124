"""Front-page renderer for the 24 November 2026 world-news image.

Builds a 1024x1024 newspaper front page from drawing primitives with PIL:
a serif masthead, a letter-spaced dateline, a lead story with a red stat
panel, a two-column grid of shorter stories, an IN BRIEF strip and a
sources footer. Everything is drawn from fixed coordinates, so the output
is deterministic: running this script twice yields identical bytes.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 36
COL_GAP = 24

# --- palette (warm newsprint) ---
PAPER = (247, 244, 238)
INK = (18, 18, 18)
GREY = (105, 112, 122)
PANEL_FILL = (252, 250, 246)
RED = (192, 18, 36)
BLUE = (29, 78, 216)
GREEN = (21, 128, 61)
ORANGE = (194, 65, 12)
NAVY = (30, 58, 138)
PURPLE = (126, 34, 206)
WHITE = (255, 255, 255)

FONT_ROOT = "/usr/share/fonts/truetype"
SERIF_BLACK = os.path.join(FONT_ROOT, "noto", "NotoSerif-Black.ttf")
SERIF = os.path.join(FONT_ROOT, "noto", "NotoSerif-Regular.ttf")
SANS = os.path.join(FONT_ROOT, "liberation", "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_ROOT, "liberation", "LiberationSans-Bold.ttf")


def load(path, size):
    """Load a TrueType font at a pixel size."""
    return ImageFont.truetype(path, size)


def text_width(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap_text(draw, s, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = s.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if text_width(draw, trial, fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_tag(draw, x, y, label, fill):
    """Small rounded label with white bold text. Returns (w, h)."""
    fnt = load(SANS_BOLD, 19)
    pad_x = 11
    h = 30
    w = int(text_width(draw, label, fnt)) + 2 * pad_x
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=fill)
    box = draw.textbbox((0, 0), label, font=fnt)
    th = box[3] - box[1]
    draw.text((x + pad_x, y + (h - th) // 2 - box[1]), label, font=fnt, fill=WHITE)
    return w, h


def draw_spaced(draw, cx, y, s, fnt, tracking, fill):
    """Draw a string centred on cx with extra tracking between letters."""
    widths = [text_width(draw, ch, fnt) for ch in s]
    total = sum(widths) + tracking * max(0, len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def draw_rule(draw, x0, x1, y, width=2, fill=None):
    draw.line([(x0, y), (x1, y)], fill=fill or INK, width=width)


def draw_masthead(draw):
    """Masthead, dateline and the double rule. Returns y below the rule."""
    title = "WORLD NEWS"
    title_font = load(SERIF_BLACK, 96)
    tw = text_width(draw, title, title_font)
    draw.text(((PAGE_W - tw) / 2, 26), title, font=title_font, fill=INK)
    date_font = load(SERIF, 25)
    draw_spaced(draw, PAGE_W / 2, 138, "TUESDAY, 24 NOVEMBER 2026",
                date_font, tracking=6, fill=INK)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, 172, width=3)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, 179, width=1)
    return 179


def draw_stat_panel(draw, x0, y0, x1, y1):
    """Red-bordered panel: big '6', caption, divider, 'Dec 1', caption."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                           outline=RED, width=2, fill=PANEL_FILL)
    pad = 16
    inner_w = (x1 - x0) - 2 * pad
    x = x0 + pad
    y = y0 + 8
    big = load(SERIF_BLACK, 56)
    draw.text((x, y), "6", font=big, fill=RED)
    y += 64
    small = load(SANS, 19)
    for line in wrap_text(draw, "months: Estonia's border closure lasts",
                          small, inner_w):
        draw.text((x, y), line, font=small, fill=INK)
        y += 21
    y += 6
    draw_rule(draw, x, x1 - pad, y, width=1, fill=RED)
    y += 12
    date_fnt = load(SANS_BOLD, 34)
    draw.text((x, y), "Dec 1", font=date_fnt, fill=INK)
    y += 42
    draw.text((x, y), "crossings shut", font=small, fill=INK)
    return y


def draw_lead(draw, y):
    """Lead story: tag, headline, deck, plus the stat panel on the right.
    Returns the y just below the section."""
    top = y
    x0 = MARGIN
    x1 = PAGE_W - MARGIN
    panel_w = 200
    text_max = (x1 - panel_w - COL_GAP) - x0
    draw_tag(draw, x0, y, "CONFLICT", RED)
    y += 38
    head_fnt = load(SANS_BOLD, 50)
    for line in wrap_text(draw, "RUSSIA WARNS ESTONIA OF 'OPEN WAR'",
                          head_fnt, text_max):
        draw.text((x0, y), line, font=head_fnt, fill=INK)
        y += 57
    y += 6
    deck_fnt = load(SANS, 23)
    deck = ("Moscow accuses Tallinn of 'hostile actions' after Estonia "
            "decides to shut its Russia border crossings from Dec 1.")
    for line in wrap_text(draw, deck, deck_fnt, text_max):
        draw.text((x0, y), line, font=deck_fnt, fill=INK)
        y += 29
    bottom = y
    draw_stat_panel(draw, x1 - panel_w, top, x1, bottom)
    return bottom

def draw_story(draw, x, y, w, tag, color, headline, deck):
    """One grid story: tag, bold headline, regular deck. Returns bottom y."""
    draw_tag(draw, x, y, tag, color)
    y += 33
    head_fnt = load(SANS_BOLD, 27)
    for line in wrap_text(draw, headline, head_fnt, w):
        draw.text((x, y), line, font=head_fnt, fill=INK)
        y += 30
    y += 3
    deck_fnt = load(SANS, 17)
    for line in wrap_text(draw, deck, deck_fnt, w):
        draw.text((x, y), line, font=deck_fnt, fill=INK)
        y += 20
    return y


def draw_grid(draw, y):
    """Two-column grid of six stories. Returns y below the grid."""
    x0 = MARGIN
    x1 = PAGE_W - MARGIN
    col_w = (x1 - x0 - COL_GAP) // 2
    left_x = x0
    right_x = x0 + col_w + COL_GAP
    stories_left = [
        ("MARKETS", BLUE,
         "Nvidia: Huang is back, shares soar ~30%",
         "Board reinstates the CEO 11 days after he quit; Nvidia adds "
         "~$1 trillion in value in a day."),
        ("CLIMATE", GREEN,
         "COP31 fallout: first failure since 2009",
         "Blame game after Antalya ends with no deal; disputes move "
         "to COP32 in Ethiopia."),
        ("POLITICS", NAVY,
         "EU proposes sweeping new Russia sanctions",
         "Banks, crypto and sports events targeted in the next package."),
    ]
    stories_right = [
        ("INCIDENT", ORANGE,
         "89 hurt as 'unknown substance' fills arena",
         "12,000 evacuated from Don Toliver's Manchester show; his "
         "London date is postponed."),
        ("CONFLICT", RED,
         "Ukraine's naval war spreads overseas",
         "Corvette Merkury sunk off Libya; a Russian freighter is hit "
         "in the Baltic."),
        ("JUSTICE", PURPLE,
         "Prince Andrew 'bribe' claim in court",
         "Ex-prince 'took \u00a3750,000 to help a Turkish heiress', the "
         "High Court is told."),
    ]
    ly = y
    ry = y
    for story in stories_left:
        ly = draw_story(draw, left_x, ly, col_w, *story)
        ly += 8
    for story in stories_right:
        ry = draw_story(draw, right_x, ry, col_w, *story)
        ry += 8
    return max(ly, ry) - 10


def draw_briefs(draw, y):
    """IN BRIEF strip and the sources footer. Returns y below the footer."""
    x0 = MARGIN
    x1 = PAGE_W - MARGIN
    label = "IN BRIEF"
    lab_fnt = load(SANS_BOLD, 21)
    lw = text_width(draw, label, lab_fnt)
    draw.text((x0, y), label, font=lab_fnt, fill=INK)
    draw_rule(draw, x0 + lw + 12, x1, y + 11, width=1)
    y += 28
    body_fnt = load(SANS, 19)
    bold_fnt = load(SANS_BOLD, 19)
    briefs = [
        ("IRAN", "Trump warns Tehran of a 'very traumatic' outcome if no "
         "nuclear deal is struck."),
        ("ARMENIA", "Pashinyan unveils a draft constitution, key to a "
         "peace deal with Azerbaijan."),
        ("SPAIN", "Top court drops all charges against Catalan separatist "
         "leader Puigdemont."),
    ]
    for country, text in briefs:
        head = country + " \u2014 "
        hw = text_width(draw, head, bold_fnt)
        draw.text((x0, y), head, font=bold_fnt, fill=INK)
        first_w = (x1 - x0) - hw
        lines = wrap_text(draw, text, body_fnt, first_w)
        draw.text((x0 + hw, y), lines[0], font=body_fnt, fill=INK)
        y += 20
        for extra in lines[1:]:
            draw.text((x0, y), extra, font=body_fnt, fill=INK)
            y += 20
        y += 1
    y += 8
    foot_fnt = load(SANS, 16)
    foot = ("Sources: Reuters \u00b7 BBC \u00b7 CNN \u00b7 AP \u00b7 LA Times \u00b7 "
            "The Times \u00b7 WSJ \u2014 Tuesday, 24 November 2026")
    fw = text_width(draw, foot, foot_fnt)
    draw.text(((PAGE_W - fw) / 2, y), foot, font=foot_fnt, fill=GREY)
    return y + 22


def build_page(out_path):
    """Assemble the whole front page and save it as a PNG."""
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y += 8
    y = draw_lead(draw, y)
    y += 8
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, y, width=1)
    y += 10
    y = draw_grid(draw, y)
    y += 10
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, y, width=1)
    y += 8
    draw_briefs(draw, y)
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "entry.png")
    build_page(target)
    print("wrote", target)
