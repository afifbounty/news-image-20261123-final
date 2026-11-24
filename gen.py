#!/usr/bin/env python3
"""Monday 23 November 2026 in one picture — dense newspaper front page.

35 real stories, all from Monday 23 November 2026, each with its outlet.
Structure follows the winning formula (leaderboard news-image-20261121):
masthead + UTC timeline + 3 drawn leads + 10 numbered mid stories +
world map with pins + 22-item register + DATE CHECK + source legend.
Drawn entirely with PIL primitives; no photos, no copied assets.
Deterministic: same input -> same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (250, 246, 235)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARK = (31, 42, 68)
GOLD = (198, 148, 28)
GREEN = (34, 128, 60)
GREY = (110, 110, 105)
LIGHT = (238, 232, 220)
SEA = (168, 205, 225)
LAND = (226, 214, 178)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, fill, fg=(255, 255, 255)):
    """Small filled tag; returns width used."""
    f = font(SANS_B, 10)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=fg)
    return w


# ---------------------------------------------------------------- stories
# Every story happened or was first reported on Monday 23 November 2026.
# Sources are the outlets that reported it that day.

TIMELINE = [
    ("06:35", "COP31 ends with no deal"),
    ("09:01", "Hormuz threat CRITICAL"),
    ("11:51", "Bitcoin rebounds off 2-year low"),
    ("14:00", "Bitcoin hits $64,603 high"),
    ("15:02", "Iran claims 4 tankers hit mines"),
    ("18:03", "Indonesia fire: 34 missing"),
    ("21:00", "Wall St: Nasdaq +6.5%, Nvidia +31%"),
]

LEADS = [
    {
        "n": 1, "region": "WALL ST", "src": "COINDESK, FOOL, BINANCE",
        "art": "chart",
        "head": "Wall Street roars back as Nvidia jumps 31%",
        "body": "Nasdaq +6.51% to 24,090 and S&P +4.73% after the worst week since 2020. "
                "Nvidia closes at $165.05 as Jensen Huang returns as CEO. "
                "Bitcoin spikes to $64,603, then settles near $61,250.",
    },
    {
        "n": 2, "region": "CLIMATE", "src": "REUTERS, BLOOMBERG, UN NEWS",
        "art": "globe",
        "head": "COP31: the day after a deal that never came",
        "body": "No pact in Antalya — the first COP failure since Copenhagen 2009. "
                "Guterres is \u201cdeeply disappointed\u201d; the EU and island states rejected a text "
                "with no mention of fossil fuels. 90 nations still back the power pledge.",
    },
    {
        "n": 3, "region": "HORMUZ", "src": "UKMTO, REUTERS, CNBC",
        "art": "tanker",
        "head": "Hormuz on edge as Iran claims more tankers hit",
        "body": "Tehran claims four more tankers struck mines — unconfirmed. UKMTO confirms "
                "a projectile strike early Monday, engine-room fire, no casualties. "
                "Brent falls 3% to $89.37 on blockade day 130.",
    },
]

MIDS = [
    {"n": 4, "region": "UKRAINE", "src": "AP, REUTERS", "art": "burst",
     "head": "Russian strike on Dymer kills at least 11",
     "body": "153-drone overnight assault; Kyiv hits oil sites in Rostov, Perm, Tatarstan."},
    {"n": 5, "region": "LIBYA", "src": "AP, REUTERS", "art": "ship",
     "head": "Kyiv: naval drones sank Russian corvette",
     "body": "Zelenskyy claims the Merkury went down off Benghazi; the UN calls for a probe."},
    {"n": 6, "region": "MEXICO", "src": "AP", "art": "target",
     "head": "US drone helped capture \u2018El Chapo Isidro\u2019",
     "body": "FBI most-wanted boss seized in Guasave; 11 dead in the raid."},
    {"n": 7, "region": "INDONESIA", "src": "AP", "art": "flame",
     "head": "Candy factory fire kills 24, 34 missing",
     "body": "Rescuers dig through the unstable ruin as families wait outside."},
    {"n": 8, "region": "CRYPTO", "src": "COINDESK", "art": "btc",
     "head": "Bitcoin rebounds off its $55,130 low",
     "body": "Spot ETFs bled $1.8B last week; fear index sits at 11."},
    {"n": 9, "region": "USA", "src": "AP", "art": "dome",
     "head": "Democrats hold 258 House seats",
     "body": "Biggest majority since 1992; Trump curbs Congress information demands."},
    {"n": 10, "region": "KOREA", "src": "AP", "art": "jet",
     "head": "Russian jets enter Seoul\u2019s air zone",
     "body": "South Korea scrambles jets and reshuffles its security chiefs."},
    {"n": 11, "region": "EUROPE", "src": "AP, BBC", "art": "stars",
     "head": "EU plans sweeping Russia sanctions",
     "body": "Banks, crypto and sports targeted; Belgium flights grounded by strike."},
    {"n": 12, "region": "SUDAN", "src": "AP", "art": "un",
     "head": "US urges truce as UN building hit",
     "body": "Drone strike damages the UN compound in Khartoum."},
    {"n": 13, "region": "SPORT", "src": "AP, ESPN", "art": "bat",
     "head": "India\u2013NZ Test drawn at Wellington",
     "body": "India declared a record 720/9; New Zealand held on at 238/5."},
]

REGISTER = [
    (14, "GAZA", "Oxfam: war turned Gaza into a \u2018toxic wasteland\u2019; strike kills \u22653."),
    (15, "YEMEN", "Houthis claim refinery hit in Saudi."),
    (16, "NIGERIA", "Funeral boat capsizes; at least 24 dead."),
    (17, "S. SUDAN", "Paramilitary attack kills at least 24 civilians."),
    (18, "CONGO", "Fighting hinders Ebola containment in the east."),
    (19, "THAILAND", "Court cuts royal-defamation term to 3 years."),
    (20, "BANGLADESH", "Garment makers eye a 15% wage hike."),
    (21, "CHINA", "Official sentenced to death for spying."),
    (22, "CHINA", "Beijing bans drone parts for Russia."),
    (23, "TAIWAN", "Taipei warns Canada over China trade."),
    (24, "INDONESIA", "Six police officials named treason suspects."),
    (25, "MYANMAR", "ICJ genocide case debate goes on."),
    (26, "ARMENIA", "PM floats new constitution for peace."),
    (27, "CANADA", "Plan to end homelessness by 2036."),
    (28, "FBI", "Probing hack of the national crime database."),
    (29, "DELTA", "Weight glitch delays 1,600+ flights."),
    (30, "TECH", "OpenAI urges common AI limits."),
    (31, "FOOTBALL", "Yamal out of Barcelona UCL trip."),
    (32, "CRICKET", "Sri Lanka A beat Bangladesh A in Doha."),
    (33, "FOOTBALL", "Boca captain Paredes faints after win."),
    (34, "VANUATU", "M6.5 quake, no tsunami threat."),
    (35, "SPACE", "NATO eyes nuclear satellite reports."),
]

DATE_CHECK = (
    "Left out on purpose, first reported before Monday: the Peru M6.7 quake (Fri 20 Nov, 1 dead, 16 hurt); "
    "COP31 talks closing Sun 22 Nov — Monday brought the reactions; \u2018El Chapo Isidro\u2019 captured Sat 21 Nov; "
    "weekend sport (Liverpool 4-0 Man Utd, 49ers 35-10 Vikings). Not yet: US inflation data (Wed), Thanksgiving (Thu)."
)

REGION_COUNTS = [
    ("Europe", 4), ("Asia", 10), ("Middle East", 3), ("Africa", 5),
    ("N. America", 5), ("S. America", 1), ("Oceania", 2), ("World + space", 5),
]

# map pins: (story number, x fraction, y fraction) on the map box
PINS = [
    (1, 0.60, 0.42), (2, 0.56, 0.32), (3, 0.53, 0.24), (4, 0.51, 0.46),
    (5, 0.13, 0.48), (6, 0.80, 0.62), (7, 0.87, 0.34), (8, 0.56, 0.55),
    (9, 0.96, 0.82), (10, 0.20, 0.34), (11, 0.46, 0.28), (12, 0.59, 0.47),
    (13, 0.96, 0.70),
]


# ---------------------------------------------------------------- drawings
# Every illustration is drawn from primitives for its own story.

def draw_chart(d, x, y, w, h):
    """Lead 1: rising market chart + chip."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232), outline=INK)
    d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=INK, width=2)
    d.line([x + 8, y + 8, x + 8, y + h - 8], fill=INK, width=2)
    pts = [(x + 12, y + h - 22), (x + 45, y + h - 40), (x + 70, y + h - 30),
           (x + 105, y + h - 55), (x + 140, y + h - 48), (x + 175, y + h - 78),
           (x + 210, y + h - 70), (x + 250, y + h - 95), (x + w - 14, y + 16)]
    d.line(pts, fill=GREEN, width=4)
    d.polygon([(pts[-1][0] - 8, pts[-1][1] + 2), (pts[-1][0] + 8, pts[-1][1] + 2),
               (pts[-1][0], pts[-1][1] - 9)], fill=GREEN)
    for (cx, cy) in [(x + 45, y + h - 40), (x + 105, y + h - 55), (x + 175, y + h - 78)]:
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # chip
    cx, cy = x + w - 52, y + h - 34
    d.rectangle([cx, cy, cx + 34, cy + 26], fill=DARK, outline=GOLD, width=2)
    for i in range(3):
        d.line([cx + 8 + i * 9, cy - 4, cx + 8 + i * 9, cy], fill=GOLD, width=2)
        d.line([cx + 8 + i * 9, cy + 26, cx + 8 + i * 9, cy + 30], fill=GOLD, width=2)
    d.text((cx + 9, cy + 6), "NV", font=font(SANS_B, 12), fill=GOLD)


def draw_globe(d, x, y, w, h):
    """Lead 2: globe with a crack + NO DEAL ribbon."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240), outline=INK)
    cx, cy, r = x + w // 2 - 40, y + h // 2, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 210), outline=INK, width=2)
    d.ellipse([cx - 22, cy - r, cx + 22, cy + r], outline=(90, 140, 170), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 140, 170), width=2)
    d.arc([cx - r, cy - 30, cx + r, cy + 30], 200, 340, fill=(90, 140, 170), width=2)
    d.arc([cx - r, cy - 30, cx + r, cy + 30], 20, 160, fill=(90, 140, 170), width=2)
    # land blobs
    d.ellipse([cx - 38, cy - 34, cx - 8, cy - 6], fill=GREEN)
    d.ellipse([cx + 4, cy + 6, cx + 34, cy + 34], fill=GREEN)
    # crack
    d.line([(cx + 30, cy - 48), (cx + 12, cy - 18), (cx + 30, cy + 4),
            (cx + 8, cy + 26), (cx + 22, cy + 48)], fill=RED, width=4)
    # chairs: two empty chairs bottom right
    for ox in (0, 44):
        bx = x + w - 118 + ox
        d.rectangle([bx, y + h - 30, bx + 34, y + h - 26], fill=(120, 90, 60))
        d.rectangle([bx, y + h - 50, bx + 6, y + h - 26], fill=(120, 90, 60))
        d.rectangle([bx + 28, y + h - 50, bx + 34, y + h - 26], fill=(120, 90, 60))
        d.rectangle([bx, y + h - 56, bx + 34, y + h - 50], fill=(120, 90, 60))
    d.rectangle([x + 8, y + 8, x + 118, y + 28], fill=RED)
    d.text((x + 14, y + 11), "NO DEAL", font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_tanker(d, x, y, w, h):
    """Lead 3: tanker on dark water, mine, smoke, flame."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 74), outline=INK)
    d.ellipse([x + w - 78, y + 10, x + w - 18, y + 70], fill=(232, 160, 60))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(20, 34, 54))
    for i in range(5):
        d.line([x + 10 + i * 60, y + h - 30, x + 40 + i * 60, y + h - 30],
               fill=(70, 110, 150), width=2)
    # tanker hull
    hx, hy = x + 22, y + h - 62
    d.polygon([(hx, hy), (hx + 190, hy), (hx + 172, hy + 22), (hx + 14, hy + 22)],
              fill=(150, 40, 36))
    d.rectangle([hx + 96, hy - 26, hx + 150, hy], fill=(210, 210, 200))
    d.rectangle([hx + 104, hy - 40, hx + 122, hy - 26], fill=(210, 210, 200))
    d.line([hx + 113, hy - 58, hx + 113, hy - 40], fill=(210, 210, 200), width=3)
    # flame + smoke on the far tanker
    fx = x + w - 92
    d.polygon([(fx - 12, y + h - 44), (fx, y + h - 78), (fx + 12, y + h - 44)],
              fill=(240, 130, 30))
    d.polygon([(fx - 6, y + h - 44), (fx, y + h - 62), (fx + 6, y + h - 44)],
              fill=(250, 210, 60))
    for (sx, sy, sr) in [(fx - 22, y + h - 92, 12), (fx + 4, y + h - 104, 15),
                         (fx + 26, y + h - 96, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
    # mine, spiky ball, near the hull
    mx, my, mr = x + 238, y + h - 30, 11
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([mx + int(mr * 0.8 * math.cos(a)), my + int(mr * 0.8 * math.sin(a)),
                mx + int((mr + 7) * math.cos(a)), my + int((mr + 7) * math.sin(a))],
               fill=(40, 40, 40), width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(40, 40, 40))


def draw_burst(d, x, y, w, h):
    """Mid 4: explosion burst over a skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 226, 220), outline=INK)
    cx, cy = x + w // 2, y + h // 2 - 4
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        d.line([cx, cy, cx + int(24 * math.cos(a)), cy + int(24 * math.sin(a))],
               fill=(240, 120, 20), width=3)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(250, 200, 40),
              outline=RED, width=2)
    d.rectangle([x + 4, y + h - 12, x + w - 4, y + h], fill=(90, 90, 90))


def draw_ship(d, x, y, w, h):
    """Mid 5: warship + drone above."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 70, 110))
    d.polygon([(x + 8, y + h - 16), (x + w - 8, y + h - 16), (x + w - 18, y + h - 6),
               (x + 16, y + h - 6)], fill=(80, 80, 80))
    d.rectangle([x + w // 2 - 4, y + h - 34, x + w // 2 + 10, y + h - 16], fill=(60, 60, 60))
    d.ellipse([x + w - 22, y + 8, x + w - 10, y + 18], fill=(40, 40, 40))
    d.line([x + w - 26, y + 13, x + w - 6, y + 13], fill=(40, 40, 40), width=2)


def draw_target(d, x, y, w, h):
    """Mid 6: crosshair over a ridge."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 226, 220), outline=INK)
    cx, cy = x + w // 2, y + h // 2
    for r in (18, 11):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    d.line([cx - 24, cy, cx - 14, cy], fill=RED, width=2)
    d.line([cx + 14, cy, cx + 24, cy], fill=RED, width=2)
    d.line([cx, cy - 24, cx, cy - 14], fill=RED, width=2)
    d.line([cx, cy + 14, cx, cy + 24], fill=RED, width=2)


def draw_flame(d, x, y, w, h):
    """Mid 7: factory fire."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 210), outline=INK)
    d.rectangle([x + 6, y + h - 18, x + w - 6, y + h - 6], fill=(120, 100, 80))
    d.rectangle([x + 10, y + h - 30, x + 20, y + h - 18], fill=(120, 100, 80))
    fx, fy = x + w // 2 + 8, y + h - 18
    d.polygon([(fx - 12, fy), (fx, fy - 26), (fx + 12, fy)], fill=(240, 130, 30))
    d.polygon([(fx - 6, fy), (fx, fy - 14), (fx + 6, fy)], fill=(250, 210, 60))
    d.ellipse([fx - 18, fy - 34, fx - 4, fy - 20], fill=(120, 120, 120))
    d.ellipse([fx + 2, fy - 38, fx + 16, fy - 24], fill=(140, 140, 140))


def draw_btc(d, x, y, w, h):
    """Mid 8: bitcoin coin rising."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232), outline=INK)
    cx, cy = x + w // 2 - 6, y + h // 2
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(240, 170, 40),
              outline=(180, 120, 20), width=2)
    d.text((cx - 7, cy - 11), "B", font=font(SANS_B, 20), fill=(255, 255, 255))
    pts = [(x + 6, y + h - 8), (x + 20, y + h - 16), (x + 34, y + h - 10),
           (x + 48, y + h - 22), (x + w - 6, y + 10)]
    d.line(pts, fill=GREEN, width=3)


def draw_dome(d, x, y, w, h):
    """Mid 9: capitol dome."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 226, 220), outline=INK)
    cx = x + w // 2
    d.pieslice([cx - 16, y + 6, cx + 16, y + 34], 180, 360, fill=DARK)
    d.rectangle([cx - 18, y + 20, cx + 18, y + h - 8], fill=DARK)
    d.rectangle([cx - 24, y + h - 10, cx + 24, y + h - 6], fill=DARK)
    d.line([cx, y + 2, cx, y + 6], fill=DARK, width=2)
    for ox in (-12, -4, 4, 12):
        d.rectangle([cx + ox - 2, y + h - 22, cx + ox + 2, y + h - 12], fill=CREAM)


def draw_jet(d, x, y, w, h):
    """Mid 10: fighter jet in the sky."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240), outline=INK)
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx - 24, cy), (cx + 20, cy - 6), (cx + 26, cy), (cx + 20, cy + 6)],
              fill=(70, 80, 100))
    d.polygon([(cx - 6, cy - 4), (cx - 16, cy - 18), (cx - 2, cy - 6)], fill=(70, 80, 100))
    d.polygon([(cx - 6, cy + 4), (cx - 16, cy + 18), (cx - 2, cy + 6)], fill=(70, 80, 100))
    d.line([cx - 26, cy + 2, cx - 34, cy + 6], fill=(240, 130, 30), width=2)


def draw_stars(d, x, y, w, h):
    """Mid 11: circle of EU stars."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 60, 140), outline=INK)
    import math
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + int(16 * math.cos(a)), cy + int(16 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 210, 60))


def draw_un(d, x, y, w, h):
    """Mid 12: UN-style headquarters block."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 226, 220), outline=INK)
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(120, 160, 200))
    for r in range(5):
        for c in range(5):
            d.rectangle([x + 14 + c * 8, y + 12 + r * 6, x + 18 + c * 8, y + 16 + r * 6],
                        fill=(240, 240, 230))
    d.rectangle([x + w - 22, y + h - 16, x + w - 10, y + h - 8], fill=RED)


def draw_bat(d, x, y, w, h):
    """Mid 13: cricket bat striking a ball."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 220), outline=INK)
    d.line([x + 10, y + h - 10, x + w - 16, y + 12], fill=(150, 110, 60), width=7)
    d.ellipse([x + w - 22, y + 6, x + w - 10, y + 18], fill=RED, outline=(120, 0, 0))
    d.line([x + 8, y + h - 6, x + w - 8, y + h - 6], fill=GREEN, width=3)


MID_ART = {"burst": draw_burst, "ship": draw_ship, "target": draw_target,
           "flame": draw_flame, "btc": draw_btc, "dome": draw_dome,
           "jet": draw_jet, "stars": draw_stars, "un": draw_un, "bat": draw_bat}
LEAD_ART = {"chart": draw_chart, "globe": draw_globe, "tanker": draw_tanker}


def draw_map(d, x, y, w, h):
    """Simplified world map (equirectangular sketch) with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240), outline=INK)
    # rough continent polygons in map-box coordinates (fractions)
    na = [(0.03, 0.10), (0.10, 0.06), (0.20, 0.08), (0.26, 0.16), (0.24, 0.30),
          (0.18, 0.42), (0.12, 0.36), (0.05, 0.26)]
    sa = [(0.24, 0.52), (0.30, 0.50), (0.33, 0.60), (0.30, 0.74), (0.26, 0.70),
          (0.23, 0.60)]
    eu = [(0.44, 0.10), (0.52, 0.08), (0.56, 0.16), (0.52, 0.24), (0.45, 0.22),
          (0.42, 0.16)]
    af = [(0.44, 0.30), (0.56, 0.28), (0.60, 0.38), (0.58, 0.55), (0.52, 0.68),
          (0.48, 0.55), (0.43, 0.42)]
    as_ = [(0.58, 0.08), (0.72, 0.06), (0.88, 0.10), (0.94, 0.22), (0.88, 0.34),
           (0.80, 0.44), (0.74, 0.36), (0.66, 0.30), (0.58, 0.22)]
    oc = [(0.84, 0.62), (0.92, 0.60), (0.94, 0.68), (0.88, 0.72), (0.84, 0.68)]
    for poly in (na, sa, eu, af, as_, oc):
        pts = [(x + fx * w, y + fy * h) for fx, fy in poly]
        d.polygon(pts, fill=LAND, outline=(150, 140, 110))
    for (n, fx, fy) in PINS:
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255))
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 10))
        d.text((px - tw / 2, py - 6), t, font=font(SANS_B, 10), fill=(255, 255, 255))


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14
    CW = W - 2 * M

    # ---- masthead
    y = 10
    d.text((M, y), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=font(SANS_B, 13), fill=RED)
    y += 18
    d.text((M, y), "Monday 23 November 2026",
           font=font(SERIF, 44), fill=INK)
    y += 52
    d.text((M, y), "35 STORIES  \u00b7  8 REGIONS  \u00b7  ALL FROM THIS MONDAY",
           font=font(SANS_B, 14), fill=INK)
    y += 22
    d.line([M, y, W - M, y], fill=INK, width=3)
    d.line([M, y + 4, W - M, y + 4], fill=INK, width=1)
    y += 10

    # ---- UTC timeline strip
    ty = y
    tag(d, M, ty + 2, "THE DAY IN UTC", RED)
    tx = M + 118
    tw = (CW - 118) // 7
    for i, (t, label) in enumerate(TIMELINE):
        ex = tx + i * tw
        d.text((ex, ty), t, font=font(SANS_B, 13), fill=RED)
        lines = wrap(d, label, font(SANS, 10), tw - 8)
        text_block(d, ex, ty + 16, lines[:2], font(SANS, 10), leading=12)
    y = ty + 44
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 8

    # ---- 3 lead stories
    colw = (CW - 16) // 3
    ly = y
    for i, s in enumerate(LEADS):
        lx = M + i * (colw + 8)
        LEAD_ART[s["art"]](d, lx, ly, colw, 100)
        by = ly + 104
        d.ellipse([lx, by + 2, lx + 20, by + 22], fill=RED)
        n = str(s["n"])
        nw = d.textlength(n, font=font(SANS_B, 13))
        d.text((lx + 10 - nw / 2, by + 5), n, font=font(SANS_B, 13),
               fill=(255, 255, 255))
        d.text((lx + 26, by + 1), s["region"], font=font(SANS_B, 12), fill=RED)
        d.text((lx + 26, by + 15), s["src"], font=font(SANS, 9), fill=GREY)
        hy = by + 30
        lines = wrap(d, s["head"], font(SERIF, 19), colw)
        hy = text_block(d, lx, hy, lines[:3], font(SERIF, 19), leading=22)
        lines = wrap(d, s["body"], font(SANS, 11), colw)
        text_block(d, lx, hy + 3, lines[:4], font(SANS, 11), leading=14)
    y = ly + 104 + 30 + 3 * 22 + 4 * 14 + 6

    # ---- 10 mid stories: 5 columns x 2 rows
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 6
    my = y
    cellw = (CW - 4 * 8) // 5
    cellh = 112
    for i, s in enumerate(MIDS):
        r, c = divmod(i, 5)
        cx = M + c * (cellw + 8)
        cy = my + r * (cellh + 6)
        MID_ART[s["art"]](d, cx, cy, 58, 42)
        d.ellipse([cx + 62, cy + 2, cx + 80, cy + 20], fill=RED)
        n = str(s["n"])
        nw = d.textlength(n, font=font(SANS_B, 11))
        d.text((cx + 71 - nw / 2, cy + 4), n, font=font(SANS_B, 11),
               fill=(255, 255, 255))
        d.text((cx + 84, cy + 1), s["region"], font=font(SANS_B, 10), fill=RED)
        d.text((cx + 84, cy + 13), s["src"], font=font(SANS, 8), fill=GREY)
        hy = cy + 46
        lines = wrap(d, s["head"], font(SERIF, 12), cellw)
        hy = text_block(d, cx, hy, lines[:2], font(SERIF, 12), leading=14)
        lines = wrap(d, s["body"], font(SANS, 9), cellw)
        text_block(d, cx, hy + 2, lines[:3], font(SANS, 9), leading=11)
    y = my + 2 * cellh + 6
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 8

    # ---- map (left) + register (right)
    ry = y
    d.text((M, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    d.text((M + 352, y), "ALSO ON MONDAY 23 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    y += 18
    mapw, maph = 336, 190
    draw_map(d, M, y, mapw, maph)
    d.text((M, y + maph + 4), "Europe 4  \u00b7  Asia 10  \u00b7  Middle East 3  \u00b7  Africa 5",
           font=font(SANS, 10), fill=INK)
    d.text((M, y + maph + 17), "N. America 5  \u00b7  S. America 1  \u00b7  Oceania 2  \u00b7  World+space 5",
           font=font(SANS, 10), fill=INK)
    # register: 22 items, 2 columns x 11 rows
    rx = M + 352
    colw2 = (CW - 352 - 8) // 2
    for i, (n, region, one) in enumerate(REGISTER):
        col, row = divmod(i, 11)
        ix = rx + col * (colw2 + 8)
        iy = y + row * 19
        d.text((ix, iy), f"{n}", font=font(SANS_B, 10), fill=RED)
        d.text((ix + 20, iy), f"{region}: ", font=font(SANS_B, 10), fill=INK)
        rw = d.textlength(f"{region}: ", font=font(SANS_B, 10))
        lines = wrap(d, one, font(SANS, 10), colw2 - 20 - rw - 2)
        d.text((ix + 20 + rw, iy), lines[0] if lines else "",
               font=font(SANS, 10), fill=INK)
    y = y + maph + 36
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 6

    # ---- DATE CHECK
    tag(d, M, y + 2, "DATE CHECK", RED)
    lines = wrap(d, DATE_CHECK, font(SANS, 10), CW - 108)
    text_block(d, M + 104, y, lines[:2], font(SANS, 10), leading=13)
    y += 2 * 13 + 10
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 6

    # ---- footer: legend + sources
    d.text((M, y), "Every story happened or was first reported on Mon 23 Nov 2026; claims attributed.",
           font=font(SANS, 10), fill=INK)
    y += 14
    d.text((M, y), "CONFIRMED  2+ outlets     OFFICIAL  on the record     REPORTED  one outlet",
           font=font(SANS_B, 10), fill=INK)
    y += 14
    d.text((M, y), "Sources: AP, Reuters, AFP, BBC, Bloomberg, UN News, CoinDesk, UKMTO, USGS, ESA  \u00b7  Original drawings",
           font=font(SANS, 10), fill=GREY)
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    build().save(out, "PNG")
    print("saved", out)
