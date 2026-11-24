#!/usr/bin/env python3
"""Render the news-image-20261124 front page: one day of world news,
Tuesday 24 November 2026, as a 1024x1024 PNG.

Every scene is drawn on its own layer exactly the size of its box and
then pasted, so no drawn pixel can spill outside its box. Every text
block is wrapped to a fixed font size and truncated with an ellipsis
as a safety net, so no text can overflow its box.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")

PAPER = (247, 243, 234, 255)
INK = (26, 26, 26, 255)
MUTED = (90, 86, 78, 255)
RULE = (180, 172, 158, 255)
RED = (176, 42, 32, 255)
NAVY = (31, 58, 95, 255)
GREEN = (46, 125, 50, 255)
AMBER = (176, 124, 0, 255)
CARD = (255, 255, 255, 255)
CARD_EDGE = (205, 198, 186, 255)
SKY = (210, 226, 238, 255)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)
F_SERIF_REG = lambda s: font("DejaVuSerif.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, max_w, max_lines):
    """Wrap to max_lines, truncating the last line with an ellipsis."""
    lines = wrap(d, text, f, max_w)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    last = out[-1]
    while last and d.textlength(last + " …", font=f) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    out[-1] = (last + " …") if last else "…"
    return out


def trunc(d, text, f, max_w):
    """Single line truncated with an ellipsis to fit max_w."""
    if d.textlength(text, font=f) <= max_w:
        return text
    t = text
    while t and d.textlength(t + " …", font=f) > max_w:
        t = t.rsplit(" ", 1)[0] if " " in t else t[:-1]
    return (t + " …") if t else "…"


def tag_width(label):
    """Width of a proof-tag pill, without drawing it."""
    return int(F_BOLD(8).getlength(label)) + 12


def tag_pill(d, x, y, label, kind):
    """Proof tag pill; returns its width. kind: CONFIRMED / REPORTED."""
    f = F_BOLD(8)
    tw = d.textlength(label, font=f)
    w = int(tw) + 12
    h = 13
    col = GREEN if kind == "CONFIRMED" else AMBER
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=col)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255, 255))
    return w


def scene_layer(w, h):
    """A transparent layer exactly box-sized; scenes draw only here."""
    return Image.new("RGBA", (w, h), (0, 0, 0, 0)), ImageDraw.Draw(
        Image.new("RGBA", (w, h), (0, 0, 0, 0))
    )


def make_layer(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)

# ---------------------------------------------------------------- scenes
def scene_nvidia(w, h):
    """Hero 1: a chip on a dark board, a rising line, cheering figures."""
    img, d = make_layer(w, h)
    d.rectangle([0, 0, w, h], fill=(18, 38, 28, 255))
    for gy in range(0, h, 14):
        d.line([(0, gy), (w, gy)], fill=(28, 54, 40, 255))
    # rising chart line, ends above the chip
    pts = [(14, h - 18), (70, h - 34), (120, h - 26), (180, h - 52),
           (235, h - 66), (290, h - 84)]
    d.line(pts, fill=(120, 220, 130, 255), width=4)
    d.ellipse([284, h - 90, 296, h - 78], fill=(140, 240, 150, 255))
    # chip
    cx, cy, s = w // 2 + 52, h // 2 + 6, 62
    d.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                        radius=8, fill=(12, 90, 60, 255),
                        outline=(140, 240, 150, 255), width=3)
    d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=4,
                        fill=(20, 160, 100, 255))
    for i in range(5):
        x = cx - 24 + i * 12
        d.line([(x, cy - s // 2 - 8), (x, cy - s // 2)], fill=(180, 230, 190, 255), width=3)
        d.line([(x, cy + s // 2), (x, cy + s // 2 + 8)], fill=(180, 230, 190, 255), width=3)
    d.text((cx - 20, cy - 8), "NVDA", font=F_BOLD(13), fill=(255, 255, 255, 255))
    # three cheering figures, bottom left
    for i, fx in enumerate((34, 62, 90)):
        fy = h - 26
        d.ellipse([fx - 5, fy - 22, fx + 5, fy - 12], fill=(245, 220, 190, 255))
        d.polygon([(fx - 8, fy), (fx + 8, fy), (fx + 6, fy - 12),
                   (fx - 6, fy - 12)], fill=(200, 60, 50, 255) if i != 1 else (40, 90, 160, 255))
        d.line([(fx - 7, fy - 10), (fx - 13, fy - 24)], fill=(245, 220, 190, 255), width=3)
        d.line([(fx + 7, fy - 10), (fx + 13, fy - 24)], fill=(245, 220, 190, 255), width=3)
    return img


def scene_gaza(w, h):
    """Hero 2: night skyline, explosion burst above the roofs."""
    img, d = make_layer(w, h)
    d.rectangle([0, 0, w, h], fill=(24, 28, 52, 255))
    for sx, sy in ((30, 16), (90, 30), (200, 12), (260, 26), (150, 22), (300, 34)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 220, 255))
    # explosion burst, kept clear of the roofline below
    bx, by = w // 2 + 70, 34
    for r, col in ((34, (255, 170, 40, 255)), (24, (255, 200, 80, 255)),
                   (13, (255, 240, 160, 255))):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for ang in range(0, 360, 30):
        import math
        x2 = bx + int(46 * math.cos(math.radians(ang)))
        y2 = by + int(46 * math.sin(math.radians(ang)))
        d.line([(bx, by), (x2, y2)], fill=(255, 180, 60, 255), width=3)
    # skyline
    base = h
    for bx0, bw, bh in ((0, 52, 46), (52, 44, 62), (96, 58, 40), (154, 48, 56),
                        (202, 56, 44), (258, 54, 58)):
        d.rectangle([bx0, base - bh, bx0 + bw, base], fill=(12, 14, 30, 255))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx0 + 8, bx0 + bw - 8, 14):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90, 255))
    # smoke column from the burst, fading before the roofs
    d.polygon([(bx - 14, by + 20), (bx + 14, by + 20), (bx + 8, h - 58),
               (bx - 8, h - 58)], fill=(90, 90, 110, 160))
    return img


def scene_zaporizhzhia(w, h):
    """Hero 3: apartment block with a blasted gap, rubble, rescue light."""
    img, d = make_layer(w, h)
    d.rectangle([0, 0, w, h], fill=(196, 205, 214, 255))
    d.ellipse([w - 52, 10, w - 16, 46], fill=(250, 240, 200, 255))
    # apartment block
    bx0, by0, bw, bh = 40, 26, 190, h - 40
    d.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(150, 120, 95, 255))
    # blasted gap in the middle floors
    d.rectangle([bx0 + 78, by0 + 52, bx0 + 138, by0 + 104], fill=(40, 32, 28, 255))
    d.polygon([(bx0 + 78, by0 + 52), (bx0 + 108, by0 + 78), (bx0 + 78, by0 + 104)],
              fill=(90, 70, 55, 255))
    d.polygon([(bx0 + 138, by0 + 52), (bx0 + 108, by0 + 78), (bx0 + 138, by0 + 104)],
              fill=(110, 88, 66, 255))
    # windows, skipping the gap
    for row in range(4):
        for col in range(5):
            wx = bx0 + 12 + col * 36
            wy = by0 + 12 + row * 26
            if 78 <= wx - bx0 <= 138 and 52 <= wy - by0 <= 104:
                continue
            d.rectangle([wx, wy, wx + 20, wy + 14], fill=(220, 225, 230, 255))
    # rubble at the foot
    for rx, ry, rr in ((bx0 + 90, by0 + bh - 4, 12), (bx0 + 120, by0 + bh - 2, 9),
                       (bx0 + 70, by0 + bh - 2, 8), (bx0 + 140, by0 + bh - 3, 10)):
        d.polygon([(rx - rr, by0 + bh), (rx, by0 + bh - rr), (rx + rr, by0 + bh)],
                  fill=(110, 95, 80, 255))
    # rescue crane + light, right side
    d.line([(262, h - 8), (262, 30)], fill=(200, 60, 40, 255), width=5)
    d.line([(262, 30), (312, 44)], fill=(200, 60, 40, 255), width=4)
    d.line([(312, 44), (312, 62)], fill=(60, 60, 60, 255), width=2)
    d.ellipse([w - 34, h - 40, w - 14, h - 20], fill=(255, 60, 40, 255))
    return img


def mini_scene(kind, w, h):
    """Small drawn scene for a medium card: coloured band + one icon."""
    img, d = make_layer(w, h)
    bands = {
        "sat": (20, 30, 66), "iran": (30, 60, 90), "delta": (40, 70, 120),
        "ship": (24, 68, 96), "drc": (30, 80, 50), "pip": (90, 70, 40),
        "gomez": (70, 40, 90), "pill": (120, 40, 70), "mkt": (120, 30, 30),
        "g6": (30, 90, 110), "wwc": (30, 100, 60), "book": (100, 60, 90),
    }
    d.rectangle([0, 0, w, h], fill=bands[kind] + (255,))
    cx, cy = w // 2, h // 2
    if kind == "sat":
        d.rectangle([cx - 12, cy - 6, cx + 12, cy + 6], fill=(220, 225, 235, 255))
        d.rectangle([cx - 34, cy - 4, cx - 14, cy + 4], fill=(120, 160, 220, 255))
        d.rectangle([cx + 14, cy - 4, cx + 34, cy + 4], fill=(120, 160, 220, 255))
        d.ellipse([cx + 22, cy - 16, cx + 30, cy - 8], fill=(255, 220, 90, 255))
    elif kind == "iran":
        d.polygon([(cx - 26, cy + 8), (cx, cy - 12), (cx + 26, cy + 8)],
                  fill=(240, 235, 220, 255))
        d.rectangle([cx - 3, cy - 14, cx + 3, cy + 2], fill=(240, 235, 220, 255))
        d.polygon([(cx - 34, cy + 12), (cx + 34, cy + 12), (cx + 20, cy - 2),
                   (cx - 20, cy - 2)], fill=(200, 60, 50, 255))
    elif kind == "delta":
        d.rectangle([cx - 30, cy - 8, cx - 2, cy + 8], fill=(40, 90, 180, 255))
        d.rectangle([cx + 2, cy - 8, cx + 30, cy + 8], fill=(250, 200, 40, 255))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    elif kind == "ship":
        d.rectangle([0, cy + 6, w, h], fill=(40, 110, 160, 255))
        d.polygon([(cx - 34, cy + 2), (cx + 30, cy + 2), (cx + 18, cy + 10),
                   (cx - 22, cy + 10)], fill=(60, 60, 66, 255))
        d.line([(cx - 6, cy + 2), (cx - 6, cy - 12)], fill=(220, 220, 220, 255), width=3)
        d.polygon([(cx - 6, cy - 12), (cx + 12, cy - 4), (cx - 6, cy - 4)],
                  fill=(220, 80, 60, 255))
    elif kind == "drc":
        d.rectangle([cx - 26, cy - 10, cx + 26, cy + 10], fill=(255, 255, 255, 255))
        d.rectangle([cx - 5, cy - 7, cx + 5, cy + 7], fill=(200, 40, 40, 255))
        d.rectangle([cx - 8, cy - 3, cx + 8, cy + 3], fill=(200, 40, 40, 255))
    elif kind == "pip":
        d.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(250, 248, 240, 255))
        d.rectangle([cx - 16, cy - 12, cx + 16, cy - 6], fill=(176, 42, 32, 255))
        for ly in (-1, 4, 9):
            d.line([(cx - 11, cy + ly), (cx + 11, cy + ly)], fill=(120, 120, 120, 255), width=2)
    elif kind == "gomez":
        d.ellipse([cx - 8, cy - 12, cx + 8, cy + 2], fill=(240, 235, 225, 255))
        d.rectangle([cx - 26, cy + 2, cx + 26, cy + 10], fill=(240, 235, 225, 255))
        for px in (-20, -7, 6, 19):
            d.rectangle([cx + px, cy + 2, cx + px + 4, cy + 10], fill=(70, 40, 90, 255))
    elif kind == "pill":
        d.rounded_rectangle([cx - 26, cy - 7, cx + 26, cy + 7], radius=7,
                            fill=(255, 255, 255, 255))
        d.rectangle([cx - 2, cy - 7, cx + 2, cy + 7], fill=(200, 40, 40, 255))
        d.ellipse([cx - 26, cy - 7, cx - 12, cy + 7], fill=(200, 40, 40, 255))
    elif kind == "mkt":
        pts = [(cx - 34, cy - 10), (cx - 14, cy - 2), (cx + 4, cy - 6),
               (cx + 22, cy + 8), (cx + 34, cy + 12)]
        d.line(pts, fill=(255, 220, 90, 255), width=4)
        d.polygon([(cx + 34, cy + 12), (cx + 26, cy + 12), (cx + 34, cy + 4)],
                  fill=(255, 220, 90, 255))
    elif kind == "g6":
        d.line([(cx, cy + 12), (cx, cy - 6)], fill=(255, 255, 255, 255), width=4)
        for r in (8, 14):
            d.arc([cx - r, cy - r - 4, cx + r, cy + r - 4], start=200, end=340,
                  fill=(140, 220, 255, 255), width=3)
        d.text((cx + 12, cy - 8), "6G", font=F_BOLD(11), fill=(255, 255, 255, 255))
    elif kind == "wwc":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255, 255),
                  outline=(40, 40, 40, 255), width=2)
        d.polygon([(cx - 4, cy - 5), (cx + 4, cy - 5), (cx + 6, cy + 3),
                   (cx, cy + 8), (cx - 6, cy + 3)], fill=(40, 40, 40, 255))
    elif kind == "book":
        d.rectangle([cx - 22, cy - 11, cx + 22, cy + 11], fill=(250, 245, 230, 255))
        d.rectangle([cx - 22, cy - 11, cx, cy + 11], fill=(220, 210, 190, 255))
        d.line([(cx, cy - 11), (cx, cy + 11)], fill=(120, 100, 80, 255), width=2)
        d.rectangle([cx + 5, cy - 6, cx + 17, cy + 6], fill=(176, 42, 32, 255))
    return img

# ---------------------------------------------------------------- data
HEROES = [
    dict(kicker="TECH · NVIDIA", scene=scene_nvidia, tag="REPORTED",
         head="Huang back at Nvidia HQ as Trump takes credit",
         deck="Staff cheered Huang on his return, a day after the board "
             "reinstated him as CEO.",
         src="BBC"),
    dict(kicker="MIDDLE EAST · GAZA", scene=scene_gaza, tag="CONFIRMED",
         head="Israeli strike kills Hamas security chief in Gaza",
         deck="Naeem Abu Nahel, who ran Hamas’ internal security, was "
             "killed with six others, medics said.",
         src="Reuters"),
    dict(kicker="WAR · UKRAINE", scene=scene_zaporizhzhia, tag="CONFIRMED",
         head="Russian strike on flats kills 2, wounds 40",
         deck="An overnight attack hit a five-storey block in "
             "Zaporizhzhia, wounding 40 — four children hurt.",
         src="Reuters"),
]

MEDIUMS = [
    dict(kicker="SPACE · NATO", kind="sat", tag="REPORTED",
         head="NATO vows to defend space after satellite reports",
         deck="Rutte: the alliance will meet any threat in orbit, after "
             "reports of a Russian nuclear satellite.",
         src="BBC"),
    dict(kicker="IRAN WAR", kind="iran", tag="CONFIRMED",
         head="Vance, Rubio meet Qatar PM; Iran rial plunges",
         deck="US envoys held White House talks as fresh sanctions sent "
             "the rial to 2.82m per dollar.",
         src="AP · AFP"),
    dict(kicker="UKRAINE · GERMANY", kind="delta", tag="CONFIRMED",
         head="Germany first to use Ukraine’s Delta war system",
         deck="Berlin signed up to Kyiv’s battlefield software; Zelensky "
             "pressed NATO to admit Ukraine outright.",
         src="Kyiv Independent"),
    dict(kicker="LIBYA", kind="ship", tag="REPORTED",
         head="UN urges probe into Benghazi port attacks",
         deck="A Russian warship was hit and sunk off Libya; Ukraine "
             "claimed it. The UN wants an inquiry.",
         src="UN News"),
    dict(kicker="AFRICA · HEALTH", kind="drc", tag="CONFIRMED",
         head="Fighting traps Ebola responders in DR Congo",
         deck="WHO staff sheltered in a hospital maternity ward in Ituri "
             "for over a day as fighting raged outside.",
         src="UN News"),
    dict(kicker="UK · WELFARE", kind="pip", tag="CONFIRMED",
         head="Benefits review: system ‘not fit for purpose’",
         deck="The Timms review called PIP assessments “dehumanising” "
             "and urged quicker payments.",
         src="BBC"),
    dict(kicker="US · CONGRESS", kind="gomez", tag="CONFIRMED",
         head="Rep. Gomez to resign after ethics findings",
         deck="The California Democrat quits on 1 Dec after the panel "
             "found “substantial evidence” of misconduct.",
         src="New York Times"),
    dict(kicker="BUSINESS · PHARMA", kind="pill", tag="CONFIRMED",
         head="Sanofi to buy Insmed for $41bn",
         deck="The French drugmaker’s biggest deal under its chief; "
             "Sanofi shares rose 5.6% on the news.",
         src="Reuters"),
    dict(kicker="MARKETS", kind="mkt", tag="CONFIRMED",
         head="Stocks retreat; Nvidia gives back 5%",
         deck="The Nasdaq fell 1.8% and the S&P 500 1.2% a day after "
             "the record rally; Europe’s STOXX 600 paused.",
         src="Reuters"),
    dict(kicker="TECH · CHINA", kind="g6", tag="CONFIRMED",
         head="China launches 6G pilots in eight regions",
         deck="Beijing, Shanghai and six more provinces start coordinated "
             "tests as the standards race speeds up.",
         src="Global Times"),
    dict(kicker="SPORT · FOOTBALL", kind="wwc", tag="CONFIRMED",
         head="UK awarded the 2035 Women’s World Cup",
         deck="Britain will host the tournament after FIFA awarded it "
             "by acclamation. No rival bid stood.",
         src="BBC"),
    dict(kicker="FRANCE · LAW", kind="book", tag="CONFIRMED",
         head="Pelicot sues publisher over nude photos",
         deck="Gisèle Pelicot says pictures of her were sent to media "
             "to promote a book. She calls it humiliation.",
         src="BBC"),
]

ALSO_ON = [
    "Russian jets enter South Korea’s air defence zone — AP",
    "Seven states back EU limits on Russian visas — Kyiv Independent",
    "Iraq PM orders ministry to run Kurdish-area oilfields — Reuters",
    "Sheikh Hasina plans return to Bangladesh on 16 Dec — Reuters",
    "Japan to pay full 2027 ICC bill early, ahead of US sanctions — Reuters",
    "S. Korea offers $375,000 to catch AI exam cheats — Wall Street Journal",
    "US blacklists Singapore cloud firm Megaspeed — Politico",
    "Pentagon: Canada falls short as defence partner — AP",
    "Huckabee doubts US aid to Israel ends this year — Reuters",
    "US weighs training Syrian soldiers in demining — Reuters",
    "Ilhan Omar warrant papers unsealed; probe reaches back to 1980 — WSJ",
    "DOJ: US citizen deported after ICE error — The Hill",
    "Texas AG Paxton drops suits over trans youth care — AP",
    "Army to detonate 5 tonnes of explosives in Iowa on Wed — NYT",
    "Hegseth’s ex-chief of staff: ‘He should resign’ — Politico",
    "FBI deputy director Raia plans to retire by year-end — NYT",
    "Senate probes Vance role in Vitol Venezuela oil deal — Reuters",
    "Trump orders DOJ to speed up federal death sentences — WSJ",
    "Appeals court revives Trump bid to move hush-money case — NYT",
    "UK sanctions 5 Myanmar generals after ICJ ruling — BBC",
    "Amnesty: Ethiopia Tigray strikes may be war crimes — Reuters",
    "UK designates Houthis under Yemen sanctions — Reuters",
    "UK warns firms aiding Ukraine of Russian sabotage — AP",
    "Hegseth yet to approve 60 Patriot missiles for Ukraine — FT",
    "UN chief calls for global AI safety framework — UN News",
    "Australia tables 46 AI governance recommendations — Digital Watch",
    "Car bomb wounds more than 20 in Colombian city — BBC",
]

TIMELINE = [
    ("00:40", "Russian strike hits Zaporizhzhia flats; 2 dead, 40 hurt"),
    ("07:45", "AFC Champions League: Shanghai Port 3–1 Buriram"),
    ("09:20", "STOXX 600 slips 0.16% as tech rally fades"),
    ("12:12", "Israeli strike kills Hamas security chief in Gaza"),
    ("14:30", "Iran’s rial plunges to 2.82m per dollar"),
    ("18:45", "Champions League night: Bodø/Glimt–LASK kick off"),
]

# lon/lat polygons, drawn by hand (simplified world outline)
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 70), (-60, 60), (-55, 52), (-60, 46), (-68, 44),
     (-70, 40), (-75, 35), (-80, 26), (-81, 31), (-84, 30), (-90, 21),
     (-94, 17), (-97, 16), (-105, 20), (-110, 23), (-115, 29), (-120, 34),
     (-124, 40), (-124, 48), (-130, 55), (-140, 60), (-152, 58), (-162, 55),
     (-168, 66)],
    # Greenland
    [(-58, 64), (-48, 60), (-40, 60), (-32, 68), (-40, 76), (-55, 76),
     (-60, 73), (-58, 64)],
    # South America
    [(-80, 9), (-77, 8), (-72, 11), (-64, 10), (-60, 8), (-52, 4),
     (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -27),
     (-52, -33), (-58, -35), (-62, -39), (-65, -41), (-68, -47),
     (-69, -52), (-73, -53), (-73, -45), (-73, -37), (-71, -30),
     (-70, -20), (-75, -15), (-80, -6), (-81, 0), (-80, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (38, 22),
     (43, 12), (48, 11), (51, 11), (46, 5), (41, -2), (40, -10),
     (36, -18), (32, -26), (28, -33), (20, -35), (16, -28), (12, -18),
     (13, -12), (9, -1), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 15)],
    # Eurasia — clockwise from Gibraltar, up the Atlantic coast,
    # round Scandinavia and the Arctic, down the Pacific coast,
    # round India and Arabia, back along the Mediterranean
    [(-9, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 47), (-4, 48),
     (0, 50), (2, 51), (4, 52), (7, 54), (8, 57), (10, 57), (10, 55),
     (12, 56), (14, 57), (18, 59), (21, 60), (24, 60), (22, 63),
     (21, 66), (25, 71), (30, 70), (33, 68), (35, 66), (40, 65),
     (44, 68), (50, 69), (55, 68), (60, 69), (68, 70), (75, 72),
     (80, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 77),
     (110, 74), (115, 73), (120, 73), (125, 72), (130, 72), (135, 71),
     (140, 72), (145, 71), (150, 70), (155, 70), (160, 70), (165, 69),
     (170, 67), (178, 66), (178, 65), (170, 60), (162, 56), (156, 52),
     (150, 59), (142, 54), (141, 45), (135, 43),
     (130, 42), (127, 40), (126, 38), (122, 31), (120, 28), (115, 23),
     (110, 20), (108, 18), (105, 10), (103, 8), (100, 7), (98, 10),
     (95, 16), (92, 21), (89, 22), (86, 20), (83, 18), (80, 13),
     (77, 8), (74, 13), (72, 20), (68, 23), (66, 25), (61, 25),
     (57, 26), (54, 27), (52, 28), (50, 29), (48, 30), (44, 29),
     (42, 27), (40, 22), (39, 20), (38, 18), (43, 13), (44, 13),
     (43, 12), (40, 15), (38, 21), (36, 28), (34, 29), (32, 31),
     (27, 36), (23, 36), (20, 39), (15, 44), (8, 44), (3, 43),
     (0, 38), (-2, 37), (-6, 36), (-9, 36)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -30), (153, -27), (150, -23),
     (146, -19), (142, -11), (139, -15), (136, -12), (132, -11),
     (128, -14), (124, -15), (120, -20), (114, -22)],
    # United Kingdom (drawn slightly enlarged so the island reads)
    [(-8, 50), (-4, 49), (-1, 51), (0, 53), (-1, 56), (-2, 59),
     (-5, 59), (-7, 57), (-7, 53), (-8, 50)],
    # Japan
    [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 36),
     (140, 38), (141, 40), (141, 44), (144, 44), (143, 42), (141, 39),
     (139, 36), (136, 33), (132, 33), (130, 31)],
    # Caribbean islands (drawn slightly enlarged so they read at this
    # scale — so no dot floats on sea)
    [(-87, 24), (-82, 24), (-77, 21), (-73, 20), (-77, 19), (-82, 22),
     (-87, 24)],  # Cuba
    [(-75, 20), (-72, 20), (-69, 19), (-67, 18), (-71, 17), (-75, 19)],  # Hispaniola
    [(-79, 19), (-76, 18), (-77, 17), (-79, 18)],  # Jamaica
    [(-68, 19), (-65, 19), (-66, 17), (-68, 18)],  # Puerto Rico
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
     (43, -20), (44, -16)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -8), (136, -6), (131, -3), (131, -1)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3),
     (110, -2), (109, 1)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
     (100, -1), (97, 3), (95, 5)],
    # Java
    [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -7), (105, -6)],
]

# (number, label, lon, lat) — every dot sits on a drawn polygon.
# Display positions are nudged a few degrees where two cities would
# otherwise share one dot (London/Paris, Gaza/Zaporizhzhia); each
# nudged dot still sits on its own country's land.
MAP_DOTS = [
    (1, "Gaza", 30.5, 28.5),
    (2, "Zaporizhzhia", 37.5, 50.5),
    (3, "London", -4.5, 53.5),
    (4, "Washington", -77.0, 38.9),
    (5, "Beijing", 116.4, 39.9),
    (6, "Seoul", 127.0, 37.5),
    (7, "Ituri, DRC", 29.5, 1.5),
    (8, "Baghdad", 44.4, 33.3),
    (9, "Dhaka", 90.4, 23.8),
    (10, "Paris", 5.5, 47.5),
    (11, "Tokyo", 139.7, 35.7),
    (12, "Bogotá", -74.0, 4.7),
]

# ---------------------------------------------------------------- layout
def draw_masthead(img, d):
    d.rectangle([0, 0, W, 78], fill=(26, 26, 26, 255))
    d.text((14, 8), "THE WORLD IN ONE DAY", font=F_SERIF(34),
           fill=(247, 243, 234, 255))
    d.text((14, 50), "TUESDAY, 24 NOVEMBER 2026",
           font=F_BOLD(15), fill=(255, 210, 90, 255))
    right = "42 STORIES  ·  7 REGIONS  ·  13 FIELDS"
    rw = d.textlength(right, font=F_BOLD(13))
    d.text((W - 14 - rw, 52), right, font=F_BOLD(13),
           fill=(247, 243, 234, 255))
    d.text((W - 14 - rw, 14), "ONE DAY · ONE PAGE",
           font=F_BOLD(11), fill=(180, 175, 165, 255))


def draw_timeline(img, d):
    y0, y1 = 82, 120
    d.rectangle([12, y0, W - 12, y1], fill=(31, 58, 95, 255))
    d.text((22, y0 + 3), "THE DAY IN TIME — UTC", font=F_BOLD(10),
           fill=(255, 210, 90, 255))
    # two rows x three columns; time bold, text on the same line
    xs = [22, 352, 682]
    for i, (t, txt) in enumerate(TIMELINE):
        col = i % 3
        row = i // 3
        x = xs[col]
        yy = y0 + 15 + row * 12
        d.text((x, yy), t, font=F_BOLD(9), fill=(255, 210, 90, 255))
        tw = d.textlength(t, font=F_BOLD(9))
        d.text((x + tw + 6, yy),
               trunc(d, txt, F_REG(9), 322 - tw - 6),
               font=F_REG(9), fill=(235, 240, 245, 255))
    d.line([(12, y1), (W - 12, y1)], fill=RULE, width=1)


def hero_card(img, d, x, y, w, h, hero):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE, width=1)
    pad = 8
    # top row: kicker left, proof tag right
    d.text((x + pad, y + 5), hero["kicker"], font=F_BOLD(9), fill=RED)
    tag_pill(d, x + w - pad - tag_width(hero["tag"]), y + 4,
             hero["tag"], hero["tag"])
    # scene
    sy = y + 22
    sh = 100
    img.paste(hero["scene"](w - 2 * pad, sh), (x + pad, sy))
    # headline, 2 lines fixed size
    hy = sy + sh + 6
    for i, ln in enumerate(fit_lines(d, hero["head"], F_BOLD(15), w - 2 * pad, 2)):
        d.text((x + pad, hy + i * 18), ln, font=F_BOLD(15), fill=INK)
    # deck, 2 lines fixed size
    dy = hy + 38
    for i, ln in enumerate(fit_lines(d, hero["deck"], F_REG(12), w - 2 * pad, 2)):
        d.text((x + pad, dy + i * 15), ln, font=F_REG(12), fill=(50, 48, 44, 255))
    # source
    d.text((x + pad, y + h - 14), "Source: " + hero["src"],
           font=F_REG(9), fill=MUTED)


def medium_card(img, d, x, y, w, h, m):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE, width=1)
    pad = 6
    # top row: kicker left, proof tag right
    d.text((x + pad, y + 4), trunc(d, m["kicker"], F_BOLD(8), w - 2 * pad - 66),
           font=F_BOLD(8), fill=NAVY)
    tag_pill(d, x + w - pad - tag_width(m["tag"]), y + 3, m["tag"], m["tag"])
    # scene band
    sy = y + 17
    sh = 28
    img.paste(mini_scene(m["kind"], w - 2 * pad, sh), (x + pad, sy))
    # headline, 2 lines fixed size
    hy = sy + sh + 4
    for i, ln in enumerate(fit_lines(d, m["head"], F_BOLD(11), w - 2 * pad, 2)):
        d.text((x + pad, hy + i * 12), ln, font=F_BOLD(11), fill=INK)
    # deck, 2 lines fixed size
    dy = hy + 25
    for i, ln in enumerate(fit_lines(d, m["deck"], F_REG(9), w - 2 * pad, 2)):
        d.text((x + pad, dy + i * 10), ln, font=F_REG(9), fill=(50, 48, 44, 255))
    # source
    d.text((x + pad, y + h - 10), "Source: " + m["src"],
           font=F_REG(8), fill=MUTED)


def draw_map(img, d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 246, 255),
                outline=CARD_EDGE, width=1)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED — 12 STORIES ON THE MAP",
           font=F_BOLD(10), fill=NAVY)
    # map area stops short of the legend strip on the right
    mx0, my0, mx1, my1 = x + 8, y + 20, x + w - 198, y + h - 4

    def proj(lon, lat):
        px = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        py = my0 + (78 - lat) / 156.0 * (my1 - my0)
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(168, 196, 168, 255), outline=(110, 140, 110, 255))
    for num, label, lon, lat in MAP_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255, 255), width=2)
        tw = d.textlength(str(num), font=F_BOLD(8))
        d.text((px - tw / 2, py - 6), str(num), font=F_BOLD(8),
               fill=(255, 255, 255, 255))
    # legend, right side of the map box
    lx = x + w - 178
    d.text((lx, y + 20), "ON THE MAP", font=F_BOLD(9), fill=NAVY)
    for i, (num, label, lon, lat) in enumerate(MAP_DOTS):
        col = i % 2
        row = i // 2
        lx2 = lx + col * 88
        ly2 = y + 34 + row * 14
        d.ellipse([lx2, ly2, lx2 + 11, ly2 + 11], fill=RED)
        tw = d.textlength(str(num), font=F_BOLD(7))
        d.text((lx2 + 5.5 - tw / 2, ly2 + 1), str(num), font=F_BOLD(7),
               fill=(255, 255, 255, 255))
        d.text((lx2 + 14, ly2 + 1), trunc(d, label, F_REG(8), 72),
               font=F_REG(8), fill=INK)


def draw_also_on(img, d, x, y, w, h):
    d.text((x, y), "ALSO ON TUESDAY 24 NOVEMBER — 27 MORE STORIES",
           font=F_BOLD(11), fill=NAVY)
    col_w = (w - 14) // 2
    f = F_REG(9)
    lh = 8.5
    for i, item in enumerate(ALSO_ON):
        col = i // 14
        row = i % 14
        ix = x + col * (col_w + 14)
        iy = y + 14 + row * lh
        num = f"{i + 16}. "
        nw = d.textlength(num, font=F_BOLD(9))
        d.text((ix, iy), num, font=F_BOLD(9), fill=RED)
        d.text((ix + nw, iy), trunc(d, item, f, col_w - nw),
               font=f, fill=INK)


def draw_bottom(img, d, y, h):
    # DATE CHECK, left half
    x0, w0 = 12, 496
    d.rectangle([x0, y, x0 + w0, y + h], fill=(255, 250, 230, 255),
                outline=CARD_EDGE, width=1)
    d.text((x0 + 8, y + 4), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=F_BOLD(10), fill=RED)
    left_out = [
        "COP31 talks end with no deal — Mon 23 Nov",
        "Nvidia +31.5% / Nasdaq +6.5% surge — Mon 23 Nov",
        "Russian missiles hit Poland — 19 Nov",
        "Russian drone over Poland — Sat 22 Nov",
        "Zelensky’s NATO plea, Berlin — Mon 23 Nov",
        "Oxfam: Gaza ‘toxic wasteland’ report — Mon 23 Nov",
    ]
    not_yet = [
        "Champions League night — kicks off 17:45 GMT",
        "Iowa explosives detonation — Wed 25 Nov",
        "US Thanksgiving — Thu 27 Nov",
    ]
    f = F_REG(9)
    ly = y + 18
    for t in left_out:
        d.text((x0 + 8, ly), "✕ " + trunc(d, t, f, 236), font=f, fill=INK)
        ly += 8.5
    d.text((x0 + 256, y + 18), "NOT YET:", font=F_BOLD(9), fill=NAVY)
    ny = y + 30
    for t in not_yet:
        d.text((x0 + 256, ny), "• " + trunc(d, t, f, 228), font=f, fill=INK)
        ny += 9
    # MARKETS, right half
    x1, w1 = 516, 496
    d.rectangle([x1, y, x1 + w1, y + h], fill=(235, 240, 245, 255),
                outline=CARD_EDGE, width=1)
    d.text((x1 + 8, y + 4), "MARKETS — MON 23 NOV CLOSES, TUE 24 NOV SO FAR",
           font=F_BOLD(10), fill=NAVY)
    mlines = [
        "S&P 500  7,237  +4.7%   ·   Nasdaq  24,089  +6.5%",
        "Dow  49,595  +3.0%   ·   Nvidia  +31.5%   ·   Gold  $3,634",
        "Tue: STOXX 600 −0.2% in morning trade; Brent −1% to a",
        "near 3-month low; US stocks retreat, Nvidia −5%.",
    ]
    my = y + 18
    for t in mlines:
        d.text((x1 + 8, my), t, font=F_REG(10), fill=INK)
        my += 11
    d.text((x1 + 8, y + h - 11), "Sources: AP · Reuters — Tue 24 Nov 2026",
           font=F_REG(8), fill=MUTED)


def main():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(img, d)
    draw_timeline(img, d)
    # heroes: y 124–348
    hx = [12, 348, 684]
    for x, hero in zip(hx, HEROES):
        hero_card(img, d, x, 124, 328, 224, hero)
    # mediums: 4 cols x 3 rows, y 352–674
    mx = [12, 264, 516, 768]
    my = [352, 460, 568]
    for r in range(3):
        for c in range(4):
            medium_card(img, d, mx[c], my[r], 244, 106, MEDIUMS[r * 4 + c])
    # map: y 678–800
    draw_map(img, d, 12, 678, 1000, 122)
    # also on: y 804–937
    draw_also_on(img, d, 12, 804, 1000, 133)
    # bottom: y 942–1012
    draw_bottom(img, d, 942, 70)
    # footer
    foot = ("Sources: BBC · Reuters · AP · AFP · NYT · WSJ · Politico · Kyiv Independent · "
            "UN News · Global Times — every event happened or was first reported Tue 24 Nov 2026.")
    fw = d.textlength(foot, font=F_REG(8))
    d.text(((W - fw) / 2, 1014), foot, font=F_REG(8), fill=MUTED)
    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
