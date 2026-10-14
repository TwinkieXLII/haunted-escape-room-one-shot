"""Draw Station 5 illustrated art as SVG in the brand palette, then render PNGs
with headless Chrome. Outputs the filenames the print packs expect:
penalty_1..8.png, pups_token.png, armory_crest_token.png.

Run:  python3 draw_station5_art.py
"""
from pathlib import Path
import math
import subprocess

D = Path(__file__).parent
SRC = D / "svg_src"
SRC.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

VOID, PLUM, STONE = "#0E0B16", "#2C1438", "#2B2D42"
GREEN, CYAN, MAGENTA, AMBER = "#39FF14", "#00F0FF", "#FF007F", "#FF7700"
GOLD, PARCH, INK = "#FFD700", "#E0D7EC", "#1A1A1A"
O = f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'

DEFS = f"""<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="22"/></filter>
<radialGradient id="vig" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/>
<stop offset="100%" stop-color="#000" stop-opacity=".75"/></radialGradient>
<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fb"/><stop offset=".45" stop-color="#a9b0c4"/><stop offset="1" stop-color="#5d6378"/></linearGradient>
<linearGradient id="silver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e4d8"/><stop offset=".5" stop-color="#b9b2a2"/><stop offset="1" stop-color="#7d7668"/></linearGradient>
<linearGradient id="fire" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{MAGENTA}"/><stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a4a22"/><stop offset="1" stop-color="#4a2a12"/></linearGradient>
</defs>"""


def bricks(w, h, color=PLUM, mortar=VOID, bw=120, bh=56):
    out = [f'<rect width="{w}" height="{h}" fill="{mortar}"/>']
    for r, y in enumerate(range(0, h, bh)):
        off = 0 if r % 2 == 0 else bw // 2
        for x in range(-off, w, bw):
            shade = ["#2C1438", "#33183f", "#261131"][(x // bw + r) % 3] if color == PLUM else color
            out.append(f'<rect x="{x + 3}" y="{y + 3}" width="{bw - 6}" height="{bh - 6}" rx="5" fill="{shade}" '
                       f'stroke="#140a1c" stroke-width="3"/>'
                       f'<path d="M{x + 10} {y + 10} h{bw - 30}" stroke="#ffffff" stroke-opacity=".06" stroke-width="4"/>')
    return "".join(out)


def floor(w, y0, h):
    out = [f'<rect x="0" y="{y0}" width="{w}" height="{h}" fill="#1b1c2b"/>']
    for r, y in enumerate(range(y0, y0 + h, 70)):
        off = 0 if r % 2 == 0 else 80
        for x in range(-off, w, 160):
            out.append(f'<rect x="{x + 4}" y="{y + 4}" width="152" height="62" rx="6" fill="{STONE}" stroke="{INK}" stroke-width="4"/>')
    return "".join(out)


def card(body, w=1200, h=1050):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}'
            f'{body}<rect width="{w}" height="{h}" fill="url(#vig)"/></svg>')


# ---- Penalty art ----------------------------------------------------------------
def arrows():
    b = [bricks(1200, 1050)]
    for y in (240, 470, 700):  # wall ports on the left
        b.append(f'<rect x="40" y="{y - 40}" width="90" height="80" rx="10" fill="{VOID}" {O}/>'
                 f'<rect x="58" y="{y - 22}" width="54" height="44" rx="6" fill="{MAGENTA}" filter="url(#glow)" opacity=".8"/>')
    for y, x, ang in [(230, 520, -4), (470, 760, 2), (700, 430, -2), (360, 980, 5), (600, 1060, -6)]:
        b.append(f'<g transform="translate({x} {y}) rotate({ang})">'
                 f'<path d="M-330 0 H-40" stroke="#ffffff" stroke-opacity=".35" stroke-width="18" stroke-dasharray="40 26"/>'
                 f'<rect x="-210" y="-9" width="230" height="18" rx="8" fill="url(#wood)" {O}/>'
                 f'<path d="M20 -26 L84 0 L20 26 Z" fill="url(#steel)" {O}/>'
                 f'<path d="M-210 -9 L-250 -36 L-176 -9 Z M-210 9 L-250 36 L-176 9 Z" fill="{MAGENTA}" {O}/></g>')
    b.append(f'<path d="M1120 120 l18 -60 M1150 150 l44 -44 M1170 200 l60 -10" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>')
    return card("".join(b))


def vines():
    b = [bricks(1200, 760), floor(1200, 760, 290)]
    for x0, s in [(260, 1), (600, -1), (930, 1)]:
        d = f"M{x0} 1050 C{x0 + 140 * s} 860 {x0 - 160 * s} 640 {x0 + 60 * s} 420 S{x0 + 220 * s} 160 {x0 + 40 * s} 90"
        b.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round"/>'
                 f'<path d="{d}" fill="none" stroke="#5f6b7d" stroke-width="44" stroke-linecap="round"/>'
                 f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="8" stroke-dasharray="6 60" filter="url(#glow)"/>')
        for t in range(5):
            y = 940 - t * 190
            x = x0 + (60 if t % 2 else -60) * s
            b.append(f'<path d="M{x} {y} l{-50 * s} -30 l20 46 Z" fill="#9aa4b6" {O}/>'
                     f'<path d="M{x + 30 * s} {y - 40} l{70 * s} -10 l-46 40 Z" fill="#9aa4b6" {O}/>')
    b.append(f'<path d="M30 980 Q600 900 1170 980" stroke="{GREEN}" stroke-width="10" fill="none" filter="url(#glow)" opacity=".7"/>')
    return card("".join(b))


def heat_metal():
    b = [bricks(1200, 1050)]
    b.append(f'<circle cx="600" cy="540" r="330" fill="{AMBER}" opacity=".35" filter="url(#soft)"/>')
    # gauntlet
    b.append(f'<g filter="url(#glow)"><path d="M420 900 L440 640 Q450 560 520 560 L700 560 Q770 560 780 640 L800 900 Z" fill="url(#fire)" {O}/>'
             + "".join(f'<rect x="{470 + i * 70}" y="330" width="58" height="250" rx="28" fill="url(#fire)" {O}/>' for i in range(4))
             + f'<path d="M780 660 Q900 600 900 500 Q900 450 860 460 Q830 560 760 600 Z" fill="url(#fire)" {O}/>'
             + "".join(f'<path d="M{450 + i * 60} 760 h40" stroke="{MAGENTA}" stroke-width="10"/>' for i in range(6))
             + '</g>')
    for x, y in [(380, 300), (840, 280), (330, 640), (900, 700), (620, 230), (760, 950), (450, 980)]:
        b.append(f'<path d="M{x} {y} l12 -34 l12 34 l34 12 l-34 12 l-12 34 l-12 -34 l-34 -12 Z" fill="{GOLD}" filter="url(#glow)"/>')
    b.append(f'<path d="M520 300 q20 -60 0 -110 M640 290 q24 -70 0 -130 M760 300 q20 -60 0 -110" stroke="#fff" '
             f'stroke-opacity=".5" stroke-width="12" fill="none" stroke-linecap="round"/>')
    return card("".join(b))


def blinding():
    b = [bricks(1200, 1050)]
    rays = "".join(f'<path d="M600 520 L{600 + 900 * math.cos(math.radians(a)):.0f} {520 + 900 * math.sin(math.radians(a)):.0f} '
                   f'L{600 + 900 * math.cos(math.radians(a + 7)):.0f} {520 + 900 * math.sin(math.radians(a + 7)):.0f} Z" fill="#fff" opacity=".55"/>'
                   for a in range(0, 360, 18))
    b.append(rays)
    b.append(f'<circle cx="600" cy="520" r="230" fill="#fff" filter="url(#soft)"/>'
             f'<circle cx="600" cy="520" r="150" fill="#fff" filter="url(#glow)"/>'
             f'<path d="M600 300 L650 470 L820 520 L650 570 L600 740 L550 570 L380 520 L550 470 Z" fill="#fffbe6" {O}/>')
    for x, y, r in [(250, 220, 40), (960, 240, 34), (230, 860, 30), (980, 840, 44)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{CYAN}" stroke-width="10" filter="url(#glow)"/>')
    return card("".join(b))


def flame_jet():
    b = [bricks(1200, 1050)]
    for y in (260, 640):
        b.append(f'<rect x="20" y="{y - 70}" width="120" height="140" rx="14" fill="{STONE}" {O}/>'
                 f'<circle cx="80" cy="{y}" r="40" fill="{VOID}" {O}/>'
                 f'<path d="M110 {y} C350 {y - 170} 640 {y - 120} 1180 {y - 40} C900 {y + 20} 980 {y + 60} 1180 {y + 110} '
                 f'C700 {y + 150} 420 {y + 150} 110 {y} Z" fill="url(#fire)" filter="url(#glow)" {O}/>'
                 f'<path d="M150 {y} C380 {y - 70} 620 {y - 40} 980 {y} C640 {y + 50} 400 {y + 60} 150 {y} Z" fill="{GOLD}" opacity=".9"/>')
    for x, y in [(400, 470), (700, 450), (950, 900), (520, 860)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{AMBER}" filter="url(#glow)"/>')
    return card("".join(b))


def grease():
    b = [bricks(1200, 560), floor(1200, 560, 490)]
    b.append(f'<path d="M560 0 V170" stroke="{INK}" stroke-width="40"/><path d="M500 150 h120 v60 h-120 Z" fill="{STONE}" {O}/>'
             f'<path d="M560 210 C560 380 520 470 470 600" stroke="#141018" stroke-width="70" fill="none" stroke-linecap="round"/>'
             f'<path d="M180 820 C120 700 360 640 520 690 C640 610 980 640 1040 760 C1120 900 820 990 600 950 C380 1010 220 940 180 820 Z" '
             f'fill="#141018" {O}/>'
             f'<path d="M300 780 Q420 720 560 760 M700 720 Q860 700 940 780" stroke="{CYAN}" stroke-width="12" fill="none" '
             f'stroke-linecap="round" filter="url(#glow)" opacity=".8"/>'
             f'<path d="M640 760 q120 -40 230 30" stroke="{MAGENTA}" stroke-width="9" fill="none" stroke-linecap="round" filter="url(#glow)"/>')
    # skid marks and a flung boot
    b.append(f'<path d="M150 980 q200 -60 380 -40 M160 1020 q220 -60 400 -40" stroke="#fff" stroke-opacity=".5" stroke-width="10" fill="none"/>'
             f'<g transform="translate(880 330) rotate(-25)"><path d="M0 0 h90 v120 h80 q30 0 30 40 v30 h-200 Z" fill="#4a2f1b" {O}/></g>'
             f'<path d="M820 300 l-40 -40 M860 260 l-10 -60 M920 270 l30 -50" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>')
    return card("".join(b))


def pendulum():
    b = [bricks(1200, 1050)]
    b.append(f'<path d="M150 820 A520 520 0 0 0 1050 820" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="30" stroke-dasharray="20 30"/>'
             f'<circle cx="600" cy="60" r="44" fill="{STONE}" {O}/>'
             f'<g transform="rotate(-28 600 60)"><path d="M590 60 V720 h20 V60 Z" fill="#6b6f84" {O}/>'
             f'<path d="M330 700 Q600 960 870 700 Q600 820 330 700 Z" fill="url(#steel)" {O}/>'
             f'<path d="M380 720 Q600 880 820 720" stroke="{CYAN}" stroke-width="10" fill="none" filter="url(#glow)"/></g>')
    for i, (x, y) in enumerate([(820, 840), (900, 760), (960, 660)]):
        b.append(f'<path d="M{x} {y} l60 -20" stroke="#fff" stroke-opacity="{.6 - i * .15}" stroke-width="14" stroke-linecap="round"/>')
    return card("".join(b))


def ceiling_surge():
    b = [bricks(1200, 1050)]
    b.append(f'<rect x="0" y="0" width="1200" height="430" fill="{STONE}" {O}/>'
             + "".join(f'<rect x="{x}" y="20" width="110" height="60" fill="#3a3d55" stroke="{INK}" stroke-width="4"/>' for x in range(20, 1200, 130)))
    for x in range(30, 1200, 95):
        b.append(f'<path d="M{x} 430 L{x + 40} 640 L{x + 80} 430 Z" fill="url(#steel)" {O}/>')
    b.append(f'<path d="M80 690 h1040" stroke="{MAGENTA}" stroke-width="8" stroke-dasharray="30 18" filter="url(#glow)"/>'
             f'<text x="600" y="830" text-anchor="middle" font-family="Bangers, Impact, sans-serif" font-size="150" fill="{GOLD}" '
             f'stroke="{INK}" stroke-width="10" paint-order="stroke">CRUNCH!</text>'
             + "".join(f'<path d="M{x} 470 l0 -60" stroke="#fff" stroke-opacity=".45" stroke-width="16" stroke-linecap="round"/>' for x in (150, 450, 750, 1050))
             + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6b6f84" {O}/>' for x, y, r in [(260, 930, 26), (520, 980, 18), (900, 940, 30), (1060, 990, 16)]))
    return card("".join(b))


# ---- Tokens ----------------------------------------------------------------------
def pup(cx, cy, s, flip=1):
    t = f'transform="translate({cx} {cy}) scale({s * flip} {s})"'
    return (f'<g {t}>'
            f'<path d="M-80 -40 L-60 -130 L-20 -70 Z M80 -40 L60 -130 L20 -70 Z" fill="#6e5236" {O}/>'
            f'<path d="M-62 -100 L-36 -72 M62 -100 L36 -72" stroke="{MAGENTA}" stroke-width="10"/>'
            f'<ellipse cx="0" cy="0" rx="100" ry="88" fill="#8a6745" {O}/>'
            f'<ellipse cx="0" cy="40" rx="58" ry="44" fill="#c9a77f" {O}/>'
            f'<ellipse cx="-38" cy="-16" rx="22" ry="26" fill="#fff" {O}/><ellipse cx="38" cy="-16" rx="22" ry="26" fill="#fff" {O}/>'
            f'<circle cx="-34" cy="-12" r="11" fill="{MAGENTA}"/><circle cx="34" cy="-12" r="11" fill="{MAGENTA}"/>'
            f'<circle cx="-30" cy="-18" r="4" fill="#fff"/><circle cx="38" cy="-18" r="4" fill="#fff"/>'
            f'<ellipse cx="0" cy="20" rx="20" ry="14" fill="{INK}"/>'
            f'<path d="M-24 52 Q0 70 24 52" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-12 56 l6 14 l6 -12 M6 56 l6 14 l6 -12" fill="#fff" stroke="{INK}" stroke-width="3"/></g>')


def pups_token():
    links = "".join(f'<ellipse cx="{300 + i * 70}" cy="{560 + (i % 2) * 8}" rx="40" ry="24" fill="none" stroke="{GOLD}" '
                    f'stroke-width="16"/><ellipse cx="{300 + i * 70}" cy="{560 + (i % 2) * 8}" rx="40" ry="24" fill="none" '
                    f'stroke="{INK}" stroke-width="4"/>' for i in range(7))
    body = (f'<rect width="1200" height="1200" fill="{VOID}"/>'
            f'<circle cx="600" cy="600" r="540" fill="{PLUM}" stroke="{CYAN}" stroke-width="22" filter="url(#glow)"/>'
            f'<circle cx="600" cy="600" r="520" fill="{PLUM}" {O}/>'
            f'<circle cx="600" cy="600" r="470" fill="none" stroke="{GOLD}" stroke-width="8" stroke-dasharray="4 18"/>'
            f'<circle cx="840" cy="330" r="90" fill="{PARCH}" opacity=".9" filter="url(#glow)"/>'
            + links +
            pup(330, 470, 1.15) + pup(600, 400, 1.3) + pup(870, 480, 1.15, -1) + pup(470, 770, 1.0) + pup(760, 790, 1.0, -1)
            + f'<path d="M820 560 h120 q40 0 40 40 v40 h-60 v-30 h-100 Z" fill="{GOLD}" {O}/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">{DEFS}{body}</svg>')


def crest_token():
    cx = cy = 600
    teeth = []
    for i in range(12):  # puzzle teeth around the rim
        a = math.radians(i * 30)
        x, y = cx + 470 * math.cos(a), cy + 470 * math.sin(a)
        teeth.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="38" fill="{VOID}" stroke="{INK}" stroke-width="6"/>')
    stars = "".join(f'<path transform="translate({cx + 470 * math.cos(math.radians(i * 30 + 15)):.0f} {cy + 470 * math.sin(math.radians(i * 30 + 15)):.0f})" '
                    f'd="M0 -22 L6 -6 L22 0 L6 6 L0 22 L-6 6 L-22 0 L-6 -6 Z" fill="#5a5448"/>' for i in range(12))
    axe = (lambda rot: f'<g transform="rotate({rot} 600 600)"><rect x="588" y="250" width="24" height="560" rx="10" fill="url(#wood)" {O}/>'
           f'<path d="M612 300 Q760 280 760 400 Q700 360 612 380 Z" fill="url(#steel)" {O}/>'
           f'<path d="M588 300 Q440 280 440 400 Q500 360 588 380 Z" fill="url(#steel)" {O}/></g>')
    tower = (f'<path d="M520 820 L540 470 H660 L680 820 Z" fill="url(#silver)" {O}/>'
             f'<path d="M500 470 H700 V420 H675 V385 H645 V420 H615 V385 H585 V420 H555 V385 H525 V420 H500 Z" fill="url(#silver)" {O}/>'
             f'<path d="M570 820 V720 Q600 680 630 720 V820" fill="{PLUM}" {O}/>'
             f'<rect x="586" y="540" width="28" height="70" rx="14" fill="{CYAN}" filter="url(#glow)"/>'
             + "".join(f'<path d="M{525 + i * 30} 470 l15 -36 l15 36" fill="#c9ccd6" stroke="{INK}" stroke-width="4"/>' for i in range(5)))
    body = (f'<rect width="1200" height="1200" fill="#141218"/>'
            f'<circle cx="600" cy="600" r="545" fill="none" stroke="{CYAN}" stroke-width="26" filter="url(#glow)"/>'
            f'<circle cx="600" cy="600" r="530" fill="url(#silver)" {O}/>'
            + "".join(teeth) + stars +
            f'<circle cx="600" cy="600" r="400" fill="{PLUM}" {O}/>'
            f'<circle cx="600" cy="600" r="380" fill="none" stroke="#b9b2a2" stroke-width="10"/>'
            + axe(-35) + axe(35) + tower)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">{DEFS}{body}</svg>')


ART = {
    "penalty_1": (arrows(), 1200, 1050), "penalty_2": (vines(), 1200, 1050),
    "penalty_3": (heat_metal(), 1200, 1050), "penalty_4": (blinding(), 1200, 1050),
    "penalty_5": (flame_jet(), 1200, 1050), "penalty_6": (grease(), 1200, 1050),
    "penalty_7": (pendulum(), 1200, 1050), "penalty_8": (ceiling_surge(), 1200, 1050),
    "pups_token": (pups_token(), 1200, 1200), "armory_crest_token": (crest_token(), 1200, 1200),
}

for name, (svg, w, h) in ART.items():
    src = SRC / f"{name}.svg"
    src.write_text(svg)
    html = SRC / f"{name}.html"
    html.write_text('<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Bangers&display=swap" '
                    f'rel="stylesheet"><style>html,body{{margin:0;background:#000}}</style></head><body>{svg}</body></html>')
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    "--virtual-time-budget=4000", f"--screenshot={D / (name + '.png')}", html.as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("wrote", name + ".png")
