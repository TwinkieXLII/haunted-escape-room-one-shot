"""Build the Station 5 (Collapsing Armory) print-and-play kit.

Text-heavy pieces (rack tags, ceiling word cards, tracker, plaque, blueprint,
corridor mat, card frames) are drawn here as SVG/HTML so the lettering is exact.
Illustrated pieces (penalty art, pups token, crest) are image slots that fill in
once the PNGs named in Art_Generation_Prompts.md exist in this folder.

Run:  python3 build_station5.py
"""
from pathlib import Path
import random

D = Path(__file__).parent

# --- Brand palette (BRANDGUIDE.md section 2) ---------------------------------
VOID, PLUM, STONE = "#0E0B16", "#2C1438", "#2B2D42"
GREEN, CYAN, MAGENTA, AMBER = "#39FF14", "#00F0FF", "#FF007F", "#FF7700"
GOLD, PARCH, INK = "#FFD700", "#E0D7EC", "#1A1A1A"
BRASS = "#C9A13B"

# --- Racks, entrance (1) to door (8). Mirrors the station file Room Setup. ---
RACKS = [
    ("SPEAR", "Dwarvish", "spear", True),
    ("MACE", "Giant", "mace", False),
    ("NET", "Goblin", "net", True),
    ("AXE", "Draconic", "axe", True),
    ("GLAIVE", "Gnomish", "glaive", False),
    ("RAPIER", "Elvish", "rapier", True),
    ("HALBERD", "Sylvan", "halberd", False),
    ("EXECUTIONER'S BLADE", "Infernal", "exec", True),
]
# Scrambled deal order for the five ceiling cards (no relation to rack order).
CEILING_ORDER = ["RAPIER", "AXE", "EXECUTIONER'S BLADE", "SPEAR", "NET"]

PENALTIES = [
    (1, "WALL ARROWS", "+5 to hit, 1d6+2 piercing."),
    (2, "CONSTRICTING VINES", "DC 13 Str save or Restrained. Action + DC 13 Athletics to break free."),
    (3, "HEAT METAL", "Worn or held metal glows hot: drop it or take 1d8 fire."),
    (4, "BLINDING FLASH", "DC 13 Cha save or blinded for 1 round."),
    (5, "FLAME JET", "DC 13 Dex save, 2d6 fire, half on a save."),
    (6, "GREASE SIPHON", "DC 13 Dex save or fall prone."),
    (7, "PENDULUM BLADE", "+5 to hit, 1d8+3 slashing."),
    (8, "CEILING SURGE", "The ceiling drops an extra 2 ft at once!"),
]

# ----------------------------------------------------------------------------
# Procedural fantasy scripts. Each letter gets a fixed glyph per script (seeded),
# so the same word in the same script always renders identically on the rack
# tag and the ceiling card. Elvish loops are CLOSED; Sylvan loops are OPEN.
# ----------------------------------------------------------------------------
W, H = 40, 56


def _glyph(script, ch):
    r = random.Random(f"{script}:{ch}")
    p = []
    if script == "Dwarvish":  # straight runes on a stave
        p.append("M20 6 L20 50")
        for y in r.sample([10, 20, 30, 40], r.randint(1, 3)):
            x = r.choice([6, 34])
            p.append(f"M20 {y} L{x} {y + r.choice([-10, 10])}")
    elif script == "Giant":  # heavy blocks
        segs = ["M6 8 L34 8", "M6 48 L34 48", "M6 8 L6 48", "M34 8 L34 48",
                "M6 28 L34 28", "M20 8 L20 48"]
        p += r.sample(segs, r.randint(2, 3))
    elif script == "Goblin":  # jagged zigzags
        pts = [(r.choice([6, 12]), 6)]
        for i in range(r.randint(3, 5)):
            pts.append((34 if i % 2 == 0 else 6, 14 + i * 9))
        p.append("M" + " L".join(f"{x} {y}" for x, y in pts))
        if r.random() < .5:
            p.append(f"M{r.choice([10, 30])} 52 L{r.choice([14, 26])} 46")
    elif script == "Draconic":  # claw rakes with hooks
        n = r.randint(2, 3)
        for i in range(n):
            x = 8 + i * (24 // max(1, n - 1))
            p.append(f"M{x + 6} 6 L{x - 2} 44 Q{x - 4} 52 {x + 4} 50")
        if r.random() < .5:
            p.append("M4 26 L36 22")
    elif script == "Gnomish":  # cogs, dots and ticks
        cx, cy, rr = r.choice([14, 20, 26]), r.choice([18, 28, 38]), r.choice([6, 8])
        p.append(f"M{cx - rr} {cy} a{rr} {rr} 0 1 0 {2 * rr} 0 a{rr} {rr} 0 1 0 {-2 * rr} 0")
        for _ in range(r.randint(1, 3)):
            a, b = r.choice([(6, 6), (34, 6), (6, 50), (34, 50), (20, 6), (20, 50)])
            p.append(f"M{a} {b} l0.1 0")
        p.append(f"M{cx} {cy - rr} L{cx} {r.choice([4, 52])}")
    elif script in ("Elvish", "Sylvan"):  # flowing curls
        cx, cy, rr = r.choice([16, 20, 24]), r.choice([18, 24, 30]), r.choice([10, 11, 12])
        if script == "Elvish":  # closed loop
            p.append(f"M{cx - rr} {cy} a{rr} {rr} 0 1 0 {2 * rr} 0 a{rr} {rr} 0 1 0 {-2 * rr} 0")
        else:  # open loop: about 3/4 of a circle, gap at the top
            p.append(f"M{cx - rr * .7:.1f} {cy - rr * .7:.1f} a{rr} {rr} 0 1 0 {rr * 1.4:.1f} 0")
        x2 = r.choice([6, 34])
        p.append(f"M{cx} {cy + rr} C{cx} {cy + 20} {x2} {cy + 6} {x2} 50")
        if r.random() < .6:
            p.append(f"M{r.choice([6, 12])} 6 Q20 {r.choice([2, 12])} {r.choice([28, 34])} 6")
    elif script == "Infernal":  # flame hooks and barbs
        parts = ["M12 50 L26 24 L10 18 L22 4", "M28 50 L14 26 L30 18 L18 4",
                 "M6 34 L34 34", "M6 14 L34 22", "M20 4 L20 50", "M8 50 L20 36 L32 50",
                 "M8 8 l8 -4 l2 12", "M24 8 l8 -4 l2 12", "M6 44 Q20 30 34 44"]
        p += r.sample(parts, 3)
    return " ".join(p)


def script_svg(word, script, color, height_in, max_width_in, stroke=4.2):
    """Render a word as glyphs. Only the first word is written in script
    ("EXECUTIONER'S BLADE" -> EXECUTIONER); words over 7 letters wrap in two."""
    w = word.replace("'S", "").replace("'", "").split(" ")[0]
    half = -(-len(w) // 2)
    lines = [w] if len(w) <= 7 else [w[:half], w[half:]]
    gap, adv = 4, W + 6
    widest = max(len(l) for l in lines)
    vw = widest * adv - 6 + 2 * gap
    vh = len(lines) * (H + 10) - 10 + 2 * gap
    out = []
    for li, line in enumerate(lines):
        x0 = gap + (widest - len(line)) * adv / 2
        for i, ch in enumerate(line):
            out.append(f'<g transform="translate({x0 + i * adv:.1f},{gap + li * (H + 10)})">'
                       f'<path d="{_glyph(script, ch)}"/></g>')
    h = min(height_in, max_width_in * vh / vw)
    return (f'<svg viewBox="0 0 {vw:.0f} {vh}" style="height:{h:.2f}in;max-width:{max_width_in}in" '
            f'fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-label="script word">{"".join(out)}</svg>')


# --- Weapon silhouettes (viewBox 0 0 100 100) --------------------------------
OUT = f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"'
WEAPONS = {
    "spear": f'<path d="M18 86 L72 32" stroke="#6b4423" stroke-width="7" stroke-linecap="round"/><path d="M68 36 L88 12 L64 28 Z" fill="{BRASS}" {OUT}/>',
    "mace": f'<path d="M24 88 L58 46" stroke="#6b4423" stroke-width="7" stroke-linecap="round"/><circle cx="64" cy="36" r="15" fill="{BRASS}" {OUT}/>'
            + "".join(f'<path d="M{64 + 15 * c:.0f} {36 + 15 * s:.0f} L{64 + 24 * c:.0f} {36 + 24 * s:.0f}" stroke="{INK}" stroke-width="5"/>'
                      for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, -.7), (.7, -.7), (-.7, .7)]),
    "net": f'<path d="M14 18 Q50 30 86 18 L80 82 Q50 72 20 82 Z" fill="none" stroke="{BRASS}" stroke-width="4"/>'
           + "".join(f'<path d="M{14 + 9 * i} {20 + i} L{20 + 8 * i} {82 - i}" stroke="{BRASS}" stroke-width="2.5"/>' for i in range(1, 8))
           + "".join(f'<path d="M{16 + i} {28 + 10 * i} Q50 {38 + 10 * i} {84 - i} {28 + 10 * i}" fill="none" stroke="{BRASS}" stroke-width="2.5"/>' for i in range(5))
           + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{STONE}" {OUT}/>' for x, y in [(14, 18), (86, 18), (80, 82), (20, 82)]),
    "axe": f'<path d="M30 90 L62 18" stroke="#6b4423" stroke-width="7" stroke-linecap="round"/><path d="M52 30 Q86 22 84 56 Q70 40 46 46 Z" fill="{BRASS}" {OUT}/>',
    "glaive": f'<path d="M20 92 L62 34" stroke="#6b4423" stroke-width="6" stroke-linecap="round"/><path d="M58 40 Q60 10 88 6 Q76 26 66 46 Z" fill="{BRASS}" {OUT}/>',
    "rapier": f'<path d="M26 74 L86 14" stroke="#d9dde6" stroke-width="4" stroke-linecap="round"/><circle cx="30" cy="70" r="11" fill="none" stroke="{BRASS}" stroke-width="4"/><path d="M14 86 L28 72" stroke="#6b4423" stroke-width="8" stroke-linecap="round"/><path d="M20 62 L40 82" stroke="{BRASS}" stroke-width="5" stroke-linecap="round"/>',
    "halberd": f'<path d="M50 96 L50 10" stroke="#6b4423" stroke-width="6" stroke-linecap="round"/><path d="M50 4 L55 18 L45 18 Z" fill="{BRASS}" {OUT}/><path d="M52 22 Q84 24 80 50 Q70 40 52 42 Z" fill="{BRASS}" {OUT}/><path d="M48 26 L30 20 L36 34 L48 34" fill="{BRASS}" {OUT}/>',
    "exec": f'<path d="M50 96 L50 78" stroke="#6b4423" stroke-width="8" stroke-linecap="round"/><path d="M34 78 L66 78" stroke="{BRASS}" stroke-width="7" stroke-linecap="round"/><path d="M38 74 L38 16 Q38 8 50 8 Q62 8 62 16 L62 74 Z" fill="#d9dde6" {OUT}/><circle cx="50" cy="22" r="5" fill="{VOID}" {OUT}/>',
}


def weapon_svg(key, size_in):
    return f'<svg viewBox="0 0 100 100" style="width:{size_in}in;height:{size_in}in">{WEAPONS[key]}</svg>'


# ----------------------------------------------------------------------------
CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Patrick+Hand&family=Montserrat:wght@800;900&family=UnifrakturCook:wght@700&family=EB+Garamond:wght@500;700&display=swap');
@page {{ size: letter; margin: 0.5in; }}
@page land {{ size: letter landscape; margin: 0.5in; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; background: #444; font-family: 'Patrick Hand', sans-serif; color: {INK}; }}
.screen {{ max-width: 7.5in; margin: 16px auto; color: #fff; font: 14px/1.4 Arial, sans-serif; }}
.page {{ width: 7.5in; height: 10in; margin: 20px auto; background: #fff; position: relative; overflow: hidden; break-after: page; }}
.page.land {{ page: land; width: 10in; height: 7.5in; }}
.ptitle {{ font: 22px 'Bangers', sans-serif; letter-spacing: 1px; margin: 0 0 .08in; color: {PLUM}; }}
.note {{ font: 11px/1.35 Arial, sans-serif; color: #444; margin: .04in 0; }}
.dm {{ background: {MAGENTA}; color: #fff; font: 900 11px Montserrat, Arial; padding: 2px 6px; border-radius: 3px; }}
.cut {{ outline: 1pt dashed #999; outline-offset: 0; }}
.grid {{ display: grid; gap: 0.08in; justify-content: center; }}
/* rack tags & ceiling cards */
.tag {{ width: 2.25in; height: 3in; background: linear-gradient(160deg,#3a2a12,#1f1608); border: 3px solid {BRASS};
        border-radius: 8px; box-shadow: inset 0 0 0 3px {INK}, inset 0 0 18px rgba(255,215,0,.25);
        display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: .14in .1in .1in; }}
.tag .rivet {{ position: absolute; }}
.tag .script {{ min-height: .9in; display: flex; align-items: center; }}
.tag .eng {{ font: 800 9px Montserrat, Arial; color: #d8c79a; letter-spacing: 1px; }}
.ceil {{ width: 2.25in; height: 3in; background: radial-gradient(circle at 50% 40%, #241a3a, {VOID} 75%);
         border: 3px solid {CYAN}; border-radius: 8px; box-shadow: inset 0 0 0 3px {INK}, inset 0 0 22px rgba(0,240,255,.35);
         display: flex; align-items: center; justify-content: center; padding: .15in; }}
/* penalty cards */
.pc {{ width: 2.4in; height: 3.36in; background: {PLUM}; border: 3px solid {INK}; border-radius: 10px;
       box-shadow: inset 0 0 0 3px #7a3fa0; padding: .09in; display: flex; flex-direction: column; position: relative; }}
.pc .num {{ position: absolute; top: .05in; left: .05in; width: .42in; height: .42in; border-radius: 50%;
            background: {VOID}; border: 2px solid {GOLD}; color: {GOLD}; font: 26px Bangers; display: flex; align-items: center; justify-content: center; z-index: 2; }}
.pc .art {{ height: 1.95in; border-radius: 6px; overflow: hidden; background: {VOID}; position: relative; border: 2px solid {INK}; }}
.pc .art img, .slot img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1; }}
.pc .art .ph, .slot .ph {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 0; }}
.pc h3 {{ margin: .06in 0 .03in; font: 19px Bangers; color: {GOLD}; text-align: center; letter-spacing: 1px; -webkit-text-stroke: .4px {INK}; }}
.pc p {{ margin: 0; font: 13px/1.15 'Patrick Hand'; color: #fff; text-align: center; }}
.ph {{ color: #8f7fa8; font: 11px Arial; text-align: center; padding: 6px; }}
.slot {{ position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.round {{ border-radius: 50%; background: {VOID}; border: 3px solid {INK}; }}
/* plaque */
.plaque {{ width: 7in; height: 5in; margin: .1in auto 0; background: radial-gradient(circle at 50% 35%, #2a2433, #0b0910 80%);
           border: 4px solid {INK}; border-radius: 14px; box-shadow: inset 0 0 0 6px #3b2f45, inset 0 0 40px rgba(255,0,127,.35);
           color: {PARCH}; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: .3in .55in; text-align: center; position: relative; }}
.plaque .runes {{ position: absolute; left: .18in; right: .18in; font: 15px monospace; color: {MAGENTA}; letter-spacing: 6px; text-shadow: 0 0 6px {MAGENTA}; overflow: hidden; white-space: nowrap; }}
.plaque h2 {{ font: 700 30px 'UnifrakturCook', serif; color: {GOLD}; margin: .05in 0 .1in; text-shadow: 0 0 8px rgba(255,215,0,.5); }}
.plaque .verse {{ font: 500 21px/1.4 'EB Garamond', Georgia, serif; }}
/* tracker */
.tracker {{ width: 1.55in; height: 9.4in; background: linear-gradient({STONE},{VOID}); border: 3px solid {INK}; border-radius: 8px;
            box-shadow: inset 0 0 0 3px #555a78; padding: .12in .08in; display: flex; flex-direction: column; }}
.tracker .lbl {{ font: 18px Bangers; color: {GOLD}; text-align: center; line-height: 1; }}
.notch {{ flex: 1; display: flex; align-items: center; gap: 6px; border-top: 1px solid #6b6f8f; color: #fff; font: 900 15px Montserrat, Arial; padding-left: 4px; }}
.notch:before {{ content: ''; width: .45in; height: 3px; background: {GOLD}; }}
.notch.crouch {{ background: rgba(255,119,0,.3); }} .notch.crouch span:after {{ content: '  CROUCH'; color: {AMBER}; font-size: 10px; }}
.notch.crush {{ background: rgba(255,0,127,.4); }} .notch.crush span:after {{ content: '  CRUSH'; color: {MAGENTA}; font-size: 10px; }}
table {{ border-collapse: collapse; width: 100%; font: 12px/1.3 Arial, sans-serif; }}
th, td {{ border: 1px solid #aaa; padding: 5px 7px; text-align: left; }}
th {{ background: #eee; }}
@media print {{ body {{ background: #fff; }} .screen {{ display: none; }} .page {{ margin: 0; }} }}
"""

PRINT_NOTE = ('<div class="screen"><b>{title}</b><br>Print at 100% on Letter, background graphics ON, '
              'browser headers/footers OFF. Cut on the dashed lines. Cardstock (110 lb) for cards and tokens. '
              'Images marked "art slot" fill in when the PNGs from Art_Generation_Prompts.md are saved in this folder.</div>')


def doc(title, pages):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}</style></head><body>{PRINT_NOTE.format(title=title)}{"".join(pages)}</body></html>')


def page(inner, land=False):
    return f'<section class="page{" land" if land else ""}">{inner}</section>'


def img_slot(fname, label, cls, style):
    return (f'<div class="slot {cls} cut" style="{style}"><img src="{fname}" alt="" '
            f'onerror="this.remove()"><div class="ph">art slot<br>{fname}<br>{label}</div></div>')


# --- Corridor mat (two landscape halves, 10 x 7.5 in each, viewBox 1000 x 750) --
def floor_tiles():
    t = []
    for row, y in enumerate(range(300, 450, 50)):
        off = 0 if row % 2 == 0 else 35
        for x in range(-off, 1000, 70):
            t.append(f'<rect x="{x}" y="{y}" width="68" height="48" rx="4" fill="{STONE}" stroke="{INK}" stroke-width="2"/>')
    return "".join(t)


def wall(y0):
    bricks = []
    for row, y in enumerate(range(y0, y0 + 300, 30)):
        off = 0 if row % 2 == 0 else 40
        for x in range(-off, 1000, 80):
            bricks.append(f'<rect x="{x}" y="{y}" width="78" height="28" fill="{PLUM}" stroke="{VOID}" stroke-width="2"/>')
    return "".join(bricks)


def rack_slot(x, y):
    return (f'<g><rect x="{x}" y="{y}" width="225" height="300" rx="10" fill="{VOID}" fill-opacity=".72" '
            f'stroke="{BRASS}" stroke-width="4" stroke-dasharray="14 8"/>'
            f'<text x="{x + 112}" y="{y + 158}" text-anchor="middle" font-family="Bangers" font-size="30" fill="{BRASS}" '
            f'opacity=".7">RACK</text><text x="{x + 112}" y="{y + 186}" text-anchor="middle" font-family="Arial" '
            f'font-size="13" fill="{BRASS}" opacity=".7">place tag here</text></g>')


def mat_half(which):
    s = [f'<svg viewBox="0 0 1000 750" style="width:10in;height:7.5in;display:block">',
         f'<rect width="1000" height="750" fill="{VOID}"/>', wall(0), wall(450), floor_tiles(),
         f'<rect x="0" y="296" width="1000" height="8" fill="{CYAN}" opacity=".55"/>',
         f'<rect x="0" y="446" width="1000" height="8" fill="{CYAN}" opacity=".55"/>']
    if which == "A":
        s.append(f'<rect x="0" y="250" width="110" height="250" fill="{VOID}" stroke="{GREEN}" stroke-width="5"/>'
                 f'<text x="55" y="385" text-anchor="middle" font-family="Bangers" font-size="26" fill="{GREEN}" '
                 f'transform="rotate(-90 55 375)">ENTRANCE</text>')
        for x, y in [(140, 0), (300, 450), (460, 0), (620, 450)]:
            s.append(rack_slot(x, y))
        s.append(f'<text x="935" y="383" text-anchor="middle" font-family="Bangers" font-size="22" fill="{GOLD}">TO SHEET B ▶</text>')
    else:
        # grate in the corridor
        s.append(f'<rect x="30" y="318" width="110" height="114" rx="6" fill="#111" stroke="{INK}" stroke-width="4"/>'
                 + "".join(f'<rect x="{38 + i * 20}" y="322" width="7" height="106" fill="#6d7186" stroke="{INK}" stroke-width="2"/>' for i in range(5))
                 + f'<text x="85" y="312" text-anchor="middle" font-family="Bangers" font-size="18" fill="{CYAN}">GRATE</text>')
        for x, y in [(160, 0), (320, 450), (480, 0), (640, 450)]:
            s.append(rack_slot(x, y))
        # blast door with mouth and five sockets
        s.append(f'<rect x="880" y="200" width="120" height="350" fill="#3a3d52" stroke="{INK}" stroke-width="6"/>'
                 + "".join(f'<circle cx="940" cy="{232 + i * 24}" r="9" fill="{VOID}" stroke="{CYAN}" stroke-width="3"/>' for i in range(5))
                 + f'<path d="M906 390 Q940 360 974 390 Q940 430 906 390 Z" fill="{VOID}" stroke="{AMBER}" stroke-width="4"/>'
                 + f'<text x="940" y="480" text-anchor="middle" font-family="Bangers" font-size="24" fill="{GOLD}">BLAST</text>'
                 + f'<text x="940" y="506" text-anchor="middle" font-family="Bangers" font-size="24" fill="{GOLD}">DOOR</text>')
        s.append(f'<text x="85" y="490" text-anchor="middle" font-family="Bangers" font-size="20" fill="{GOLD}">◀ FROM SHEET A</text>')
    s.append("</svg>")
    return "".join(s)


# --- Blueprint (handout) ------------------------------------------------------
def blueprint():
    b = "#7fc8ff"
    pipes = [("LEFT", "M375 520 C330 600 200 610 140 700"),
             ("CENTER", "M375 520 L375 760"),
             ("RIGHT", "M375 520 C420 600 550 610 610 700")]
    s = [f'<svg viewBox="0 0 750 900" style="width:7.5in;height:9in;display:block">',
         f'<rect width="750" height="900" fill="#0c2a5c"/>',
         "".join(f'<path d="M{x} 0 V900" stroke="#1d4a8a" stroke-width="1"/>' for x in range(0, 750, 25)),
         "".join(f'<path d="M0 {y} H750" stroke="#1d4a8a" stroke-width="1"/>' for y in range(0, 900, 25)),
         f'<text x="375" y="60" text-anchor="middle" font-family="UnifrakturCook,serif" font-size="34" fill="#fff">Armory Sump — Cross-Section</text>',
         f'<text x="375" y="88" text-anchor="middle" font-family="Patrick Hand" font-size="18" fill="{b}">drawn by the castle masons · not to scale</text>',
         f'<path d="M60 300 H690" stroke="#fff" stroke-width="5"/>',
         f'<text x="70" y="290" font-family="Patrick Hand" font-size="18" fill="#fff">ARMORY FLOOR</text>',
         f'<rect x="300" y="292" width="150" height="16" fill="#0c2a5c"/>']
    for i in range(6):
        s.append(f'<rect x="{302 + i * 28}" y="290" width="6" height="22" fill="#fff"/>')
    s.append(f'<path d="M308 250 V275 M336 250 V275 M308 262 H336" stroke="{GOLD}" stroke-width="3"/>'
             f'<text x="345" y="240" font-family="Montserrat,Arial" font-weight="900" font-size="20" fill="{GOLD}">4-INCH IRON BAR SPACING</text>'
             f'<path d="M300 312 L330 420 H420 L450 312" fill="none" stroke="#fff" stroke-width="4"/>'
             f'<text x="470" y="400" font-family="Patrick Hand" font-size="18" fill="#fff">culvert</text>'
             f'<path d="M330 420 L375 520 L420 420" fill="none" stroke="#fff" stroke-width="4"/>')
    for name, d in pipes:
        s.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="30" stroke-linecap="round" opacity=".9"/>'
                 f'<path d="{d}" fill="none" stroke="#0c2a5c" stroke-width="20" stroke-linecap="round"/>')
    for name, (x, y) in zip(["LEFT", "CENTER", "RIGHT"], [(140, 750), (375, 805), (610, 750)]):
        s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Bangers" font-size="34" fill="{GOLD}">{name}</text>')
    s.append(f'<text x="375" y="870" text-anchor="middle" font-family="Patrick Hand" font-size="18" fill="{b}">'
             f'Bars fused into bedrock. No hand, blade or crowbar fits.</text></svg>')
    return "".join(s)


# --- Pages ---------------------------------------------------------------------
def tag_html(word, script, key):
    return (f'<div class="tag cut">'
            f'{weapon_svg(key, 1.15)}'
            f'<div class="script">{script_svg(word, script, GOLD, 1.0, 1.95)}</div>'
            f'<div class="eng">{word}</div></div>')


def ceil_html(word):
    script = next(s for w, s, _, _ in RACKS if w == word)
    return f'<div class="ceil cut">{script_svg(word, script, CYAN, 1.3, 1.85, stroke=4.6)}</div>'


def penalty_html(n, title, text):
    return (f'<div class="pc cut"><div class="num">{n}</div>'
            f'<div class="art"><img src="penalty_{n}.png" alt="" onerror="this.remove()"><div class="ph">art slot<br>penalty_{n}.png</div></div>'
            f'<h3>{title}</h3><p>{text}</p></div>')


player = [
    page(f'<div class="ptitle">Armory Corridor — Sheet A (entrance half)</div>{mat_half("A")}', land=True),
    page(f'<div class="ptitle">Armory Corridor — Sheet B (door half)</div>{mat_half("B")}', land=True),
    page('<div class="ptitle">Weapon Rack Tags — cut 8</div>'
         '<p class="note">Lay each tag in its RACK slot on the corridor mat, in the order on the DM sheet. No numbers on the tags.</p>'
         '<div class="grid" style="grid-template-columns:repeat(3,2.25in)">'
         + "".join(tag_html(w, s, k) for w, s, k, _ in RACKS) + '</div>'),
    page('<div style="display:flex;gap:.25in">'
         '<div><div class="ptitle" style="font-size:16px">Ceiling Tracker</div><div class="tracker cut">'
         '<div class="lbl">SPIKE TIPS</div>'
         + "".join(f'<div class="notch{" crouch" if n == 5 else ""}{" crush" if n == 0 else ""}"><span>{n} FT</span></div>' for n in range(15, -1, -1))
         + '</div></div>'
         '<div><div class="ptitle">Glowing Ceiling Words — cut 5</div>'
         '<p class="note">Deal face up in any order. Players match the lettering to the rack tags.</p>'
         '<div class="grid" style="grid-template-columns:repeat(2,2.25in)">'
         + "".join(ceil_html(w) for w in CEILING_ORDER)
         + f'<div class="cut" style="width:2.25in;height:3in;display:flex;flex-direction:column;align-items:center;justify-content:center;background:{VOID};border-radius:8px">'
           f'<svg viewBox="0 0 200 60" style="width:2in"><rect x="10" y="30" width="180" height="22" rx="4" fill="{STONE}" stroke="{INK}" stroke-width="3"/>'
         + "".join(f'<path d="M{20 + i * 20} 30 L{30 + i * 20} 6 L{40 + i * 20} 30 Z" fill="#c8ccd8" stroke="{INK}" stroke-width="2"/>' for i in range(8))
         + f'</svg><div class="note" style="color:#fff;text-align:center">Ceiling slider<br>(cut out, clip to the tracker)</div></div>'
         '</div></div></div>'),
    page('<div class="ptitle">The Archway Plaque — hand over at the start</div>'
         '<div class="plaque cut"><div class="runes" style="top:.12in">ᚱ ᛏ ᛉ ᚦ ᛟ ᛞ ᚹ ᛗ ᛚ ᛜ ᛞ ᚠ ᚱ ᛏ ᛉ ᚦ ᛟ ᛞ ᚹ ᛗ ᛚ</div>'
         f'<svg viewBox="0 0 100 100" style="width:.9in;height:.9in"><circle cx="50" cy="50" r="44" fill="none" stroke="{MAGENTA}" stroke-width="7"/>'
         f'<path d="M30 46 Q30 22 50 22 Q70 22 70 46 Q70 58 62 62 L62 72 H38 L38 62 Q30 58 30 46 Z" fill="{PARCH}" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="42" cy="45" r="6" fill="{INK}"/><circle cx="58" cy="45" r="6" fill="{INK}"/>'
         f'<path d="M18 82 L82 18" stroke="{MAGENTA}" stroke-width="8" stroke-linecap="round"/></svg>'
         '<h2>The Armory Geas</h2>'
         '<div class="verse">“Speak not the hunter\'s word (\'T---\') within these walls, lest iron and fire answer your tongue. '
         'Walk in silence, or speak only of hazards, snares, cogs, devices, and mechanisms.”</div>'
         '<div class="runes" style="bottom:.12in">ᛚ ᛗ ᚹ ᛞ ᛟ ᚦ ᛉ ᛏ ᚱ ᚠ ᛞ ᛜ ᛚ ᛗ ᚹ ᛞ ᛟ ᚦ ᛉ ᛏ ᚱ</div></div>'),
    page('<div class="ptitle">Drainage Grate &amp; Sump Blueprint — give when they examine the grate</div>'
         f'<div class="cut" style="width:7.5in;height:9in">{blueprint()}</div>'),
]

dm = [
    page('<div class="ptitle"><span class="dm">DM ONLY</span> Taboo Penalty Cards 1–6</div>'
         '<p class="note">Keep face down. After a slip, roll 1d8 and show only the rolled card.</p>'
         '<div class="grid" style="grid-template-columns:repeat(3,2.4in)">'
         + "".join(penalty_html(*p) for p in PENALTIES[:6]) + '</div>'),
    page('<div class="ptitle"><span class="dm">DM ONLY</span> Penalty Cards 7–8 · Pups Token · Crest #5</div>'
         '<div class="grid" style="grid-template-columns:repeat(3,2.4in);justify-content:start">'
         + "".join(penalty_html(*p) for p in PENALTIES[6:]) + '</div>'
         '<div style="display:flex;gap:.5in;align-items:center;margin-top:.3in">'
         '<div><div class="ptitle" style="font-size:16px">Swarm of Pups — 2 in token</div>'
         + img_slot("pups_token.png", "Swarm of Pups", "round", "width:2in;height:2in") + '</div>'
         '<div><div class="ptitle" style="font-size:16px">Armory Crest #5 — on solve only</div>'
         + img_slot("armory_crest_token.png", "Crest #5", "round", "width:3in;height:3in") + '</div></div>'),
    page('<div class="ptitle"><span class="dm">DM ONLY</span> Rack Placement &amp; Answer Key</div>'
         '<p class="note">Never print this on the back of a player prop. Source of truth: Stations/Station_5_Collapsing_Armory_Corridor_of_the_Taboo_Word.md.</p>'
         '<table><tr><th>Mat position</th><th>Rack tag</th><th>Script</th><th>Lit by a ceiling word?</th></tr>'
         + "".join(f'<tr><td>{pos}</td><td>{w}</td><td>{s}</td><td>{"<b>YES</b>" if lit else "no"}</td></tr>'
                   for pos, (w, s, _, lit) in zip(
                       ["Sheet A, top wall, 1st slot", "Sheet A, bottom wall, 1st slot", "Sheet A, top wall, 2nd slot",
                        "Sheet A, bottom wall, 2nd slot", "Sheet B, top wall, 1st slot", "Sheet B, bottom wall, 1st slot",
                        "Sheet B, top wall, 2nd slot", "Sheet B, bottom wall, 2nd slot"], RACKS))
         + '</table>'
         '<p style="font:15px Arial;margin-top:.2in">Password (first letters of lit weapons, entrance to door): '
         '<b style="font-size:22px">S · N · A · R · E</b></p>'
         '<p class="note">Crest is in the <b>RIGHT</b> pipe. Ceiling: 15 ft, drops 1 ft per real minute; CROUCH at 5 ft, CRUSH at 0 ft. '
         'Each slip: bell, 1d8 card, door locks 1 minute (sand timer).</p>'
         '<p class="note">Decoy: the Sylvan HALBERD tag looks like the Elvish RAPIER card. Elvish loops are closed; Sylvan loops are open.</p>'),
]

(D / "Station_5_Player_Print_Pack.html").write_text(doc("Station 5 — Player Props (Collapsing Armory)", player))
(D / "Station_5_DM_Print_Pack.html").write_text(doc("Station 5 — DM-held Props & Key", dm))
print(f"Player pack: {len(player)} pages. DM pack: {len(dm)} pages.")
