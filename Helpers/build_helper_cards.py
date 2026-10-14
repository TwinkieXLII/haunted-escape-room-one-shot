"""Turn the Station_N_Helper_Cards.md files into printable HTML (and PDF if
Google Chrome is installed).

Markdown subset: #/##/### headings, paragraphs, "- " bullets, "> " quotes,
| tables |, **bold**, *italic*. Two HTML-comment markers (invisible on GitHub):
  <!-- page -->                  start a new printed page
  <!-- card: Title -->  ...  <!-- /card -->   a dashed cut-out card

Run:  python3 build_helper_cards.py
"""
from pathlib import Path
import html
import re
import shutil
import subprocess

D = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Patrick+Hand&family=Montserrat:wght@700;900&display=swap');
@page { size: letter; margin: 0.5in; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #555; font: 10.5pt/1.32 Arial, Helvetica, sans-serif; color: #1A1A1A; }
.page { width: 7.5in; min-height: 10in; margin: 18px auto; background: #fff; padding: 0; break-after: page; }
@media print { body { background: #fff; } .page { margin: 0; min-height: 0; } }
h1 { font: 26px Bangers, Impact, sans-serif; letter-spacing: 1px; color: #2C1438; margin: 0 0 4px;
     border-bottom: 4px solid #00F0FF; padding-bottom: 3px; }
h2 { font: 900 12.5pt Montserrat, Arial; color: #fff; background: #2C1438; padding: 3px 8px; margin: 10px 0 5px; border-radius: 3px; }
h3 { font: 900 10.5pt Montserrat, Arial; color: #2C1438; margin: 8px 0 3px; }
p { margin: 3px 0; }
ul { margin: 2px 0 4px; padding-left: 18px; } li { margin: 1px 0; }
blockquote { margin: 4px 0; padding: 5px 9px; background: #F2EEF7; border-left: 4px solid #FF007F;
             font: 11.5pt/1.25 'Patrick Hand', 'Comic Sans MS', cursive; }
table { border-collapse: collapse; width: 100%; margin: 3px 0 5px; font-size: 9.5pt; }
th, td { border: 1px solid #9a93a6; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #E0D7EC; }
.cards { display: flex; flex-wrap: wrap; gap: 0.12in; }
.card { width: 3.64in; border: 1.5px dashed #888; border-radius: 6px; padding: 7px 9px; break-inside: avoid; }
.card.wide { width: 100%; }
.card .ct { font: 20px Bangers, Impact, sans-serif; letter-spacing: .5px; color: #FF007F; margin-bottom: 2px; }
.card.label { background: #0E0B16; color: #fff; text-align: center; padding: 5px 8px; }
.card.label .ct { color: #FFD700; font-size: 22px; }
.card.label p { color: #E0D7EC; }
.card.cert { height: 4.4in; text-align: center; font-size: 13pt; display: flex; flex-direction: column; justify-content: center;
             border: 3px double #2C1438; background: #F7F3FB; }
.card.cert .ct { font-size: 40px; color: #2C1438; }
.card.cert p { margin: 7px 0; }
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return s


def blocks(lines):
    out, i = [], 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
        elif ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1
        elif ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>"); i += 1
        elif ln.startswith("# "):
            out.append(f"<h1>{inline(ln[2:])}</h1>"); i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i].strip().strip("|").split("|")); i += 1
            t = "<table>" + "<tr>" + "".join(f"<th>{inline(c.strip())}</th>" for c in rows[0]) + "</tr>"
            for r in rows[2:]:
                t += "<tr>" + "".join(f"<td>{inline(c.strip())}</td>" for c in r) + "</tr>"
            out.append(t + "</table>")
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif ln.startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(inline(lines[i][1:].strip())); i += 1
            out.append("<blockquote>" + "<br>".join(x for x in q if x) + "</blockquote>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |>|<!--)", lines[i]):
                para.append(inline(lines[i].strip())); i += 1
            if para:
                out.append("<p>" + " ".join(para) + "</p>")
            else:
                i += 1
    return "".join(out)


CARD_RE = re.compile(r"<!-- card(?:\.(\w+))?: (.+?) -->\n(.*?)<!-- /card -->", re.S)


def render(md):
    pages = []
    for chunk in md.split("<!-- page -->"):
        parts, pos, cards = [], 0, []
        for m in CARD_RE.finditer(chunk):
            if chunk[pos:m.start()].strip():
                if cards:
                    parts.append('<div class="cards">' + "".join(cards) + "</div>"); cards = []
                parts.append(blocks(chunk[pos:m.start()].splitlines()))
            kind, title, body = m.group(1) or "", m.group(2), m.group(3)
            cards.append(f'<div class="card {kind}"><div class="ct">{inline(title)}</div>{blocks(body.splitlines())}</div>')
            pos = m.end()
        if cards:
            parts.append('<div class="cards">' + "".join(cards) + "</div>")
        parts.append(blocks(chunk[pos:].splitlines()))
        pages.append('<section class="page">' + "".join(parts) + "</section>")
    return "".join(pages)


def doc(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")


sources = sorted(D.glob("Station_*_Helper_Cards.md"))
bodies = []
for src in sources:
    body = render(src.read_text())
    bodies.append(body)
    out = src.with_suffix(".html")
    out.write_text(doc(src.stem.replace("_", " "), body))
(D / "All_Helper_GM_Cards.html").write_text(doc("All Helper GM Cards", "".join(bodies)))

# The finale print kit uses the same card format.
kit = D.parent / "Finale" / "Finale_Print_Kit.md"
extra = []
if kit.exists():
    kit.with_suffix(".html").write_text(doc("Finale Print Kit", render(kit.read_text())))
    extra.append(kit.with_suffix(".html"))

if Path(CHROME).exists():
    for h in [s.with_suffix(".html") for s in sources] + [D / "All_Helper_GM_Cards.html"] + extra:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={h.with_suffix('.pdf')}", h.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(f"Built {len(sources)} helper kits" + (" (+ PDFs)" if Path(CHROME).exists() else ""))
