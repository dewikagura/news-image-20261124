#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Provenance for the make.fun news-image-20261124 entry (v1, early news).
Every headline was verified against live news sources (Reuters, BBC, CNN,
AP, LA Times, The Times, WSJ) on 24 Nov 2026; see README.md for the fact
notes. Run:  python3 tools/draw.py   -> writes entry.png next to main.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (248, 246, 240)     # newsprint off-white
INK = (20, 20, 20)
GRAY = (110, 108, 100)
RULE = (60, 60, 60)

FONT_DIR = "/usr/share/fonts/truetype"
MASTHEAD_FONT = os.path.join(FONT_DIR, "noto", "NotoSerifDisplay-Black.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu", "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")

GREEN = (27, 122, 61)       # CLIMATE
RED = (179, 38, 30)         # CONFLICT
BLUE = (26, 79, 160)        # MARKETS
PURPLE = (106, 63, 181)     # JUSTICE
NAVY = (15, 61, 145)        # POLITICS
ORANGE = (190, 100, 16)     # INCIDENT
DARK = (40, 40, 40)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + tracking
    return total


def draw_tag(draw, x, y, text, color):
    fnt = font(SANS_BOLD, 14)
    pad_x, h = 10, 22
    w = int(fnt.getlength(text)) + 2 * pad_x
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=color)
    draw.text((x + pad_x, y + 4), text, font=fnt, fill=(255, 255, 255))
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    size = 92
    while True:
        mf = font(MASTHEAD_FONT, size)
        if mf.getlength("WORLD NEWS") <= 880 or size <= 60:
            break
        size -= 2
    d.text(((W - mf.getlength("WORLD NEWS")) / 2, 18), "WORLD NEWS",
           font=mf, fill=INK)

    # ---- Date line ------------------------------------------------------
    draw_tracked(d, W / 2, 128, "TUESDAY, 24 NOVEMBER 2026",
                 font(SANS, 21), INK, tracking=7)
    d.line([(M, 162), (W - M, 162)], fill=RULE, width=3)
    d.line([(M, 169), (W - M, 169)], fill=RULE, width=1)

    # ---- Lead story -----------------------------------------------------
    ly = 186
    draw_tag(d, M, ly, "CONFLICT", RED)
    head_f = font(SANS_BOLD, 44)
    lead_head = "RUSSIA WARNS ESTONIA OF 'OPEN WAR'"
    head_lines = wrap(lead_head, head_f, 716)
    assert len(head_lines) <= 2, f"lead headline {len(head_lines)} lines"
    y = ly + 36
    for line in head_lines:
        d.text((M, y), line, font=head_f, fill=INK)
        y += 52
    body_f = font(SANS, 20)
    lead_body = ("Moscow accuses Tallinn of 'hostile actions' after Estonia "
                 "decides to shut its Russia border crossings from Dec 1.")
    body_lines = wrap(lead_body, body_f, 716)
    assert len(body_lines) <= 2, f"lead body {len(body_lines)} lines"
    y += 6
    for line in body_lines:
        d.text((M, y), line, font=body_f, fill=INK)
        y += 26

    # Stat panel (right of lead): verified numbers from the coverage.
    px0, py0, px1, py1 = 788, 186, W - M, 386
    d.rounded_rectangle([px0, py0, px1, py1], radius=8,
                        outline=RED, width=2, fill=(244, 238, 238))
    num_f = font(SANS_BOLD, 56)
    d.text((px0 + 18, py0 + 12), "6", font=num_f, fill=RED)
    small_f = font(SANS, 15)
    for i, line in enumerate(wrap("months: Estonia's border closure lasts",
                                  small_f, px1 - px0 - 36)):
        d.text((px0 + 18, py0 + 80 + i * 19), line, font=small_f, fill=INK)
    d.line([(px0 + 18, py0 + 124), (px1 - 18, py0 + 124)], fill=RED, width=1)
    yr_f = font(SANS_BOLD, 30)
    d.text((px0 + 18, py0 + 134), "Dec 1", font=yr_f, fill=INK)
    d.text((px0 + 18, py0 + 170), "crossings shut",
           font=small_f, fill=INK)

    d.line([(M, 402), (W - M, 402)], fill=RULE, width=1)

    # ---- Story grid: 2 cols x 3 rows ------------------------------------
    blocks = [
        ("MARKETS", BLUE, "Nvidia: Huang is back, shares soar ~30%",
         "Board reinstates the CEO 11 days after he quit; Nvidia adds "
         "~$1 trillion in value in a day."),
        ("INCIDENT", ORANGE, "89 hurt as 'unknown substance' fills arena",
         "12,000 evacuated from Don Toliver's Manchester show; his "
         "London date is postponed."),
        ("CLIMATE", GREEN, "COP31 fallout: first failure since 2009",
         "Blame game after Antalya ends with no deal; disputes move "
         "to COP32 in Ethiopia."),
        ("CONFLICT", RED, "Ukraine's naval war spreads overseas",
         "Corvette Merkury sunk off Libya; a Russian freighter is hit "
         "in the Baltic."),
        ("POLITICS", NAVY, "EU proposes sweeping new Russia sanctions",
         "Banks, crypto and sports events targeted in the next package."),
        ("JUSTICE", PURPLE, "Prince Andrew 'bribe' claim in court",
         "Ex-prince 'took \u00a3750,000 to help a Turkish heiress', the "
         "High Court is told."),
    ]
    col_w = (CW - 24) // 2
    col_x = [M, M + col_w + 24]
    row_y = [418, 564, 710]
    h_f = font(SANS_BOLD, 23)
    s_f = font(SANS, 15)
    for idx, (tag, color, head, summ) in enumerate(blocks):
        x = col_x[idx % 2]
        y = row_y[idx // 2]
        draw_tag(d, x, y, tag, color)
        hl = wrap(head, h_f, col_w)
        assert len(hl) <= 2, f"block {idx} headline {len(hl)} lines: {head}"
        yy = y + 30
        for line in hl:
            d.text((x, yy), line, font=h_f, fill=INK)
            yy += 28
        sl = wrap(summ, s_f, col_w)
        assert len(sl) <= 2, f"block {idx} summary {len(sl)} lines: {summ}"
        yy += 4
        for line in sl:
            d.text((x, yy), line, font=s_f, fill=(50, 50, 50))
            yy += 20

    d.line([(M, 856), (W - M, 856)], fill=RULE, width=1)

    # ---- In brief --------------------------------------------------------
    y = 870
    brief_h = font(SANS_BOLD, 16)
    d.text((M, y), "IN BRIEF", font=brief_h, fill=INK)
    d.line([(M + 92, y + 9), (W - M, y + 9)], fill=RULE, width=1)
    briefs = [
        ("IRAN", "Trump warns Tehran of a 'very traumatic' outcome if no "
         "nuclear deal is struck."),
        ("ARMENIA", "Pashinyan unveils a draft constitution, key to a peace "
         "deal with Azerbaijan."),
        ("SPAIN", "Top court drops all charges against Catalan separatist "
         "leader Puigdemont."),
    ]
    b_f = font(SANS, 16)
    b_bold = font(SANS_BOLD, 16)
    y += 26
    for lead_in, rest in briefs:
        lines = wrap(lead_in + " \u2014 " + rest, b_f, CW)
        assert len(lines) == 1, f"brief wraps to {len(lines)} lines: {lead_in}"
        d.text((M, y), lead_in + " \u2014 ", font=b_bold, fill=INK)
        d.text((M + b_bold.getlength(lead_in + " \u2014 "), y), rest,
               font=b_f, fill=(50, 50, 50))
        y += 24

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS, 12)
    foot = ("Sources: Reuters \u00b7 BBC \u00b7 CNN \u00b7 AP \u00b7 LA Times "
            "\u00b7 The Times \u00b7 WSJ \u2014 Tuesday, 24 November 2026")
    d.text(((W - foot_f.getlength(foot)) / 2, 988), foot,
           font=foot_f, fill=GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       os.pardir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", os.path.abspath(out), img.size,
          os.path.getsize(os.path.abspath(out)), "bytes")


if __name__ == "__main__":
    main()
