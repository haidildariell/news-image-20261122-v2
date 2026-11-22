#!/usr/bin/env python3
"""Render entry.png (1024x1024) for make.fun news-image-20261122, v2.

One page that sums up Sunday 22 November 2026 in world news.
Design rule for this rebuild: legibility first. 35 stories, large type,
airy spacing, nothing clipped. All layout code written for this edition.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (247, 242, 231)
NAVY = (22, 40, 63)
INK = (22, 24, 29)
RED = (176, 42, 33)
GOLD = (201, 162, 39)
FAINT = (110, 104, 92)
CARD = (252, 249, 242)
LINEC = (214, 205, 186)
MAPDOT = (168, 178, 196)

FD = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FD + "LiberationSerif-Bold.ttf"
SERIF_I = FD + "LiberationSerif-Italic.ttf"
SANS_B = FD + "LiberationSans-Bold.ttf"
SANS_R = FD + "LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, font):
    return d.textlength(text, font=font)


def tracked(d, xy, text, font, color, track=3):
    """Draw text with manual letter tracking; returns end x."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=color)
        x += tw(d, ch, font) + track
    return x


def tracked_w(d, text, font, track=3):
    return sum(tw(d, ch, font) + track for ch in text) - track


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, path, size, max_w, min_size=10):
    while size > min_size and tw(d, text, font=F(path, size)) > max_w:
        size -= 1
    return F(path, size)


# ---------------------------------------------------------------- data
with open(os.path.join(HERE, "stories_20261122.json")) as fh:
    DATA = json.load(fh)
BY_N = {s["n"]: s for s in DATA["stories"]}

DAY = "Sunday"
DATE_LINE = "Sunday 22 November 2026"

# Lead cards: (story n, banner big word, region label, status chip)
LEADS = [
    (11, "400 DRONES", "EUROPE - WAR", "CONFIRMED"),
    (1, "GULF WIDENS", "MIDDLE EAST - WAR", "CONFIRMED"),
    (15, "DEADLOCK", "EUROPE - CLIMATE TALKS", "REPORTED"),
    (12, "PROVOCATION", "EUROPE - NATO BORDER", "REPORTED"),
]

# Mid briefs: original story numbers, shown with bold place lead-ins.
MIDS = [2, 4, 13, 14, 31, 18, 3, 16]

# Also-on one-liners: (story n, compact text without the place lead-in).
# Kept deliberately short - one printed line each is the legibility fix.
ALSO = [
    (7, "fire at power plant kills 4, hurts 35"),
    (8, "UNIFIL hands control to the army"),
    (9, "six wounded in ceasefire breaches"),
    (17, "Zelensky: Putin a 'killer'"),
    (19, "cover for 10,000 forest staff"),
    (20, "Trafalgar Square tree sets off"),
    (21, "Depardieu probed over rape claim"),
    (22, "EU mulls budget cuts, platform tax"),
    (23, "Pentagon curbs Canada socialising"),
    (24, "FBI probes criminal-database hack"),
    (25, "plan to close Rikers Island jail"),
    (26, "airlines warned of al-Qaeda threat"),
    (27, "Gupta gets 19 years in Pannun plot"),
    (29, "Trump threatens AI data-centre ban"),
    (30, "Bolsonaro in ICU, bowel obstruction"),
    (32, "Modi opens Patna-Vaishali bridge"),
    (33, "cyclone cancels 14 flights"),
    (34, "ICMR seals 100 tech transfers"),
    (35, "Nepal PM Shah to meet Modi"),
    (37, "Japan troops to drill in India, a first"),
    (38, "driverless air taxi's first passengers"),
    (41, "England's T20 streak ended"),
    (42, "ANC fights to keep its cities"),
]

# Map pins for the 4 lead + 8 mid stories: display number -> (col, row)
PIN_AT = {
    1: (33, 2),    # Kyiv
    2: (36, 6),    # Kuwait
    3: (32, 6),    # Antalya
    4: (30, 3),    # Poland
    5: (38, 8),    # Bahrain
    6: (40, 5),    # Strait of Hormuz
    7: (28, 0),    # Baltic Sea
    8: (31, 0),    # Tallinn
    9: (7, 8),     # Sinaloa
    10: (34, 4),   # Crimea
    11: (36, 10),  # off Oman
    12: (27, 2),   # Copenhagen
}
PIN_NAMES = ["Kyiv", "Kuwait", "Antalya", "Poland", "Bahrain", "Hormuz",
             "Baltic", "Tallinn", "Sinaloa", "Crimea", "Oman", "Copenhagen"]

# Stylised dot world map, 48 cols x 15 rows ('#' = land dot).
MAP_ROWS = [
    "                                                ",
    "   ######    #####     ##################       ",
    "  ########  #######   #####################     ",
    "  #########  ######    ##########  ########     ",
    "   ########   ####      ########     ###        ",
    "    ######     ##        ######                 ",
    "     ####               #######      ##         ",
    "     ###      ##         #####      ####        ",
    "      ##     ####         ###        ##         ",
    "      #      ######       ##     #              ",
    "              ####       #      ###             ",
    "              ###              ######           ",
    "              ##                ####            ",
    "              #                  ##             ",
    "                                                ",
]

DATE_CHECK = (
    "DATE CHECK - Every story on this page happened, or was first reported, "
    "on Sunday 22 November 2026. Discarded as off-day: the Peru 6.9 quake "
    "(Friday 20 Nov local, reported 21 Nov - it led the 21 Nov edition), "
    "the APEC Shenzhen summit and the Anthropic IPO (both 18-20 Nov)."
)


# ---------------------------------------------------------------- draw
def draw_masthead(d):
    d.rectangle([0, 0, W, 148], fill=NAVY)
    t = "THE DAY IN WORLD NEWS"
    f = F(SANS_B, 20)
    x = (W - tracked_w(d, t, f, 6)) / 2
    tracked(d, (x, 15), t, f, GOLD, 6)
    d.line([30, 48, 994, 48], fill=GOLD, width=2)
    t2 = DATE_LINE
    f2 = fit(d, t2, SERIF_B, 58, 940)
    d.text(((W - tw(d, t2, f2)) / 2, 58), t2, font=f2, fill=(255, 255, 255))
    t3 = "Thirty-five stories - seven regions - one page"
    f3 = F(SERIF_I, 19)
    d.text(((W - tw(d, t3, f3)) / 2, 121), t3, font=f3, fill=(233, 224, 199))


def draw_numbers(d):
    y0, y1 = 162, 230
    d.line([30, y0, 994, y0], fill=LINEC, width=2)
    d.line([30, y1, 994, y1], fill=LINEC, width=2)
    cell = 964 / 6
    for i, item in enumerate(DATA["numbers_strip"]):
        cx = 30 + cell * i + cell / 2
        f = F(SANS_B, 36)
        v = item["value"]
        d.text((cx - tw(d, v, f) / 2, 168), v, font=f, fill=NAVY)
        fc = F(SANS_R, 12)
        lines = wrap(d, item["caption"], fc, cell - 14)
        for j, ln in enumerate(lines[:2]):
            d.text((cx - tw(d, ln, fc) / 2, 207 + j * 14), ln, font=fc, fill=INK)


def draw_leads(d):
    cw, chh, gx, gy, y0 = 474, 140, 16, 12, 244
    for idx, (n, banner, cat, status) in enumerate(LEADS):
        s = BY_N[n]
        x = 30 + (idx % 2) * (cw + gx)
        y = y0 + (idx // 2) * (chh + gy)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=LINEC, width=1)
        d.ellipse([x + 14, y + 12, x + 46, y + 44], fill=RED)
        fn = F(SANS_B, 17)
        num = str(idx + 1)
        d.text((x + 30 - tw(d, num, fn) / 2, y + 19), num, font=fn,
               fill=(255, 255, 255))
        fb = fit(d, banner, SANS_B, 28, cw - 70)
        d.text((x + 58, y + 12), banner, font=fb, fill=RED)
        fc = F(SANS_B, 11)
        tracked(d, (x + 58, y + 48), cat, fc, NAVY, 2)
        fh = F(SERIF_B, 19)
        lines = wrap(d, s["headline"], fh, cw - 32)
        if len(lines) > 2:
            fh = F(SERIF_B, 17)
            lines = wrap(d, s["headline"], fh, cw - 32)
        for j, ln in enumerate(lines[:2]):
            d.text((x + 16, y + 68 + j * 23), ln, font=fh, fill=INK)
        fchip = F(SANS_B, 11)
        src = s["source"].upper()
        d.rectangle([x + 16, y + chh - 26, x + 28 + tw(d, src, fchip),
                     y + chh - 8], outline=NAVY, width=1)
        d.text((x + 22, y + chh - 23), src, font=fchip, fill=NAVY)
        d.text((x + cw - 16 - tw(d, status, fchip), y + chh - 23), status,
               font=fchip, fill=RED)


def draw_mids(d):
    y = 552
    fh = F(SANS_B, 13)
    tracked(d, (30, y), "MORE OF THE DAY", fh, NAVY, 3)
    d.line([240, y + 8, 994, y + 8], fill=LINEC, width=2)
    cw, chh, gx, gy, y0 = 235, 62, 8, 8, 576
    for i, n in enumerate(MIDS):
        s = BY_N[n]
        x = 30 + (i % 4) * (cw + gx)
        yy = y0 + (i // 4) * (chh + gy)
        fp = F(SANS_B, 13)
        d.text((x, yy), s["place"], font=fp, fill=RED)
        fs = F(SANS_R, 10)
        d.text((x + tw(d, s["place"], fp) + 6, yy + 2), "- " + s["source"],
               font=fs, fill=FAINT)
        ft = F(SANS_R, 13)
        lines = wrap(d, s["headline"], ft, cw - 4)
        for j, ln in enumerate(lines[:3]):
            d.text((x, yy + 19 + j * 15), ln, font=ft, fill=INK)


def draw_bottom(d):
    y = 716
    fh = F(SANS_B, 13)
    tracked(d, (30, y), "WHERE IT HAPPENED", fh, NAVY, 3)
    tracked(d, (470, y), "ALSO ON SUNDAY", fh, RED, 3)
    d.line([30, y + 22, 994, y + 22], fill=LINEC, width=2)
    # --- dot map
    ox, oy, cell = 30, 750, 8.8
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx, cy = ox + c * cell + 4.4, oy + r * cell + 4.4
                d.ellipse([cx - 2.4, cy - 2.4, cx + 2.4, cy + 2.4], fill=MAPDOT)
    fp = F(SANS_B, 10)
    for num, (c, r) in PIN_AT.items():
        cx, cy = ox + c * cell + 4.4, oy + r * cell + 4.4
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)
        t = str(num)
        d.text((cx - tw(d, t, fp) / 2, cy - 6), t, font=fp, fill=(255, 255, 255))
    legend = " - ".join(f"{i + 1} {nm}" for i, nm in enumerate(PIN_NAMES))
    fl = F(SANS_R, 12)
    for j, ln in enumerate(wrap(d, legend, fl, 424)):
        d.text((30, 892 + j * 16), ln, font=fl, fill=INK)
    # --- also-on digest, two columns, one line per story
    colw, gx, y0, pitch = 254, 16, 750, 15.5
    for i, (n, text) in enumerate(ALSO):
        s = BY_N[n]
        col, row = divmod(i, 12)
        x = 470 + col * (colw + gx)
        yy = y0 + row * pitch
        num = str(13 + i)
        place = s["place"].title() if s["place"].isupper() else s["place"]
        rest = " - " + text
        size = 11
        while size > 8:
            fp2, ft = F(SANS_B, size), F(SANS_R, size)
            if 20 + tw(d, place, fp2) + tw(d, rest, ft) <= colw:
                break
            size -= 1
        fn = F(SANS_B, size)
        d.text((x, yy), num, font=fn, fill=RED)
        d.text((x + 20, yy), place, font=fp2, fill=INK)
        d.text((x + 20 + tw(d, place, fp2), yy), rest, font=ft, fill=INK)


def draw_footer(d):
    d.rectangle([30, 948, 994, 988], outline=RED, width=2)
    f = F(SANS_R, 12)
    lines = wrap(d, DATE_CHECK, f, 936)
    for j, ln in enumerate(lines[:2]):
        d.text((44, 956 + j * 15), ln, font=f, fill=INK)
    src = ("Sources: Reuters - BBC - Times of India - The Daily Jagran - "
           "PW Live - wire reports")
    fs = F(SANS_R, 11)
    d.text(((W - tw(d, src, fs)) / 2, 996), src, font=fs, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_leads(d)
    draw_mids(d)
    draw_bottom(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
