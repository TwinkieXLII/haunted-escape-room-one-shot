from printkit.common import ROOT, render_html, merge_pdfs

def build():
    """Build the ornate DM Guide (HTML + PDF) from DM_Guide.md.

    Markdown subset: # / ## / ### headings, paragraphs, "- " bullets (two-space
    indent for a nested level), "> " quotes, | tables |, **bold**, *italic*,
    ![alt](path) images. Layout markers (HTML comments, invisible on GitHub):
      <!-- page -->                              new printed page
      <!-- cover --> ... <!-- /cover -->          cover page
      <!-- station: N · crest_N --> ... <!-- /station -->   station banner
      <!-- box.kind: Title --> ... <!-- /box -->  ornate box (lore, read, rules,
                                                  hint, secret, bound, note)
    Run:  python3 build_dm_guide.py
    """
    from pathlib import Path
    import html
    import re

    D = ROOT / "DM_Guide"
    ART = D.parent / "Art"

    # --- Crest seals: small copies of the station crest art -----------------------
    CRESTS = {1: "Station_1/archive_crest_token.png", 2: "Station_2/alchemist_crest_token.png",
              3: "Station_3/observatory_crest_token.png", 4: "Station_4/menagerie_crest_token.png",
              5: "Station_5/armory_crest_token.png"}
    (D / "img").mkdir(exist_ok=True)
    try:
        from PIL import Image
        for n, rel in CRESTS.items():
            out = D / "img" / f"crest_{n}.png"
            if (ART / rel).exists() and not out.exists():
                im = Image.open(ART / rel).convert("RGB")
                im.thumbnail((520, 520))
                im.save(out, optimize=True)
    except ImportError:
        print("Pillow not available: crest seals must already exist in img/")

    CSS = """
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&family=Cinzel:wght@600;800&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Patrick+Hand&family=Bangers&display=swap');
    @page { size: letter; margin: 0.55in 0.55in 0.6in;
      @bottom-center { content: "❦  The Von Zarovich Estate · Dungeon Master's Grimoire · " counter(page) "  ❦";
                       font: 9pt 'Cinzel', serif; color: #6b4f7a; } }
    @page cover { margin: 0; @bottom-center { content: none; } }
    * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    :root { --plum:#2C1438; --void:#0E0B16; --gold:#B8860B; --gold2:#FFD700; --cyan:#00F0FF; --mag:#FF007F;
            --green:#39FF14; --parch:#F6F0E2; --ink:#1A1A1A; }
    html { background: #3a2f45; }
    body { margin: 0; font: 10.4pt/1.33 'EB Garamond', Georgia, serif; color: var(--ink); }
    .frame { position: fixed; top: -0.42in; bottom: -0.47in; left: -0.4in; right: -0.4in; pointer-events: none;
             border: 3px double #6b4f7a; border-radius: 6px; }
    .frame::before, .frame::after { content: "✠"; position: absolute; color: #8a6d2f; font-size: 15px; }
    .frame::before { top: -11px; left: 50%; transform: translateX(-50%); background: var(--parch); padding: 0 6px; }
    .frame::after { bottom: -11px; left: 50%; transform: translateX(-50%); background: var(--parch); padding: 0 6px; }
    .sheet { background: radial-gradient(ellipse at 50% 30%, #fbf7ee, var(--parch) 70%); }
    @media screen { .sheet { width: 8.5in; margin: 20px auto; padding: 0.7in 0.65in; box-shadow: 0 8px 30px #0008; }
                    .frame { display: none; } }
    section.page { break-after: page; }
    h1 { font: 700 28pt/1.1 'UnifrakturCook', serif; color: var(--plum); text-align: center; margin: 0 0 6px; }
    h1::after { content: "❧ ✦ ☙"; display: block; font: 13pt 'EB Garamond', serif; color: var(--gold); margin-top: 4px; letter-spacing: 6px; }
    h2 { font: 800 15pt 'Cinzel', serif; color: var(--plum); margin: 10px 0 4px; }
    h3 { font: 800 12pt 'Cinzel', serif; color: var(--plum); margin: 8px 0 3px; }
    p { margin: 4px 0; }
    ul { margin: 2px 0 4px; padding-left: 18px; } li { margin: 1px 0; } li::marker { color: var(--gold); }
    blockquote { margin: 4px 0; padding: 4px 9px; font: 11.5pt/1.28 'Patrick Hand', cursive; background: #fff8; border-left: 4px solid var(--mag); }
    table { border-collapse: collapse; width: 100%; margin: 4px 0 6px; font-size: 9.4pt; background: #fffc; }
    th { background: var(--plum); color: #f3e9ff; font: 600 9.5pt 'Cinzel', serif; text-align: left; padding: 4px 6px; }
    td { border: 1px solid #c9b9d6; padding: 3px 6px; vertical-align: top; }
    tr:nth-child(even) td { background: #f3ecf8; }
    .box { position: relative; margin: 7px 0; padding: 7px 12px 6px; border-radius: 8px; }
    .box.read, .box.bound, .box.note, .box.secret, .box.hint { break-inside: avoid; }
    .box .bt, h1, h2, h3, .station { break-after: avoid; }
    tr, li, blockquote, table { break-inside: avoid; }
    .box .bt { font: 800 11.5pt 'Cinzel', serif; letter-spacing: .5px; margin: -2px 0 5px; }
    .box.lore { background: #fffaf0; border: 2px solid var(--gold); box-shadow: inset 0 0 0 4px #fffaf0, inset 0 0 0 5px #d8b765; }
    .box.lore .bt { color: #7a5a12; text-align: center; }
    .box.lore .bt::before, .box.lore .bt::after { content: " ❦ "; color: var(--gold); }
    .box.lore > p:first-of-type::first-letter { font: 700 30pt/0.9 'UnifrakturCook', serif; float: left; color: var(--plum); margin: 3px 6px 0 0; }
    .box.read { background: #fff0f7; border: 2px solid var(--mag); }
    .box.read .bt { color: var(--mag); } .box.read .bt::before { content: "🕯 "; }
    .box.read blockquote { background: transparent; border: 0; padding: 0; font-size: 12.5pt; }
    .box.rules { background: #fff; border: 2px solid var(--plum); padding-top: 0; }
    .box.rules .bt { background: var(--plum); color: var(--gold2); margin: 0 -14px 7px; padding: 5px 14px; border-radius: 6px 6px 0 0; }
    .box.hint { background: #effcfd; border: 2px solid #0aa9b5; }
    .box.hint .bt { color: #077a83; } .box.hint .bt::before { content: "✉ "; }
    .box.secret { background: var(--void); color: #ece4f5; border: 3px double var(--gold2); }
    .box.secret .bt { color: var(--gold2); } .box.secret .bt::before { content: "🔒 "; }
    .box.secret table { background: #1d1527; } .box.secret td { border-color: #4b3a5c; color: #ece4f5; }
    .box.secret tr:nth-child(even) td { background: #261b33; } .box.secret th { background: #4a2361; }
    .box.secret b, .box.secret strong { color: var(--gold2); }
    .box.bound { background: #f3fbef; border: 2px solid #3d8b2f; }
    .box.bound .bt { color: #2c6b20; } .box.bound .bt::before { content: "⚔ "; }
    .box.note { background: #f5f1fa; border: 1.5px dashed #6b4f7a; }
    .box.note .bt { color: var(--plum); } .box.note .bt::before { content: "✦ "; }
    .station { display: flex; align-items: center; gap: 16px; background: linear-gradient(90deg, var(--void), var(--plum));
               border: 3px double var(--gold2); border-radius: 12px; padding: 10px 16px; margin-bottom: 10px; color: #e9ddf5; }
    .station img { width: 0.95in; height: 0.95in; border-radius: 50%; flex: none; box-shadow: 0 0 12px var(--cyan); }
    .station h1 { color: var(--gold2); text-align: left; font-size: 21pt; } .station h1::after { content: none; }
    .station p { font-style: italic; color: #d9c8ea; }
    .station b { color: var(--cyan); font-style: normal; }
    .cover { page: cover; height: 11in; background: radial-gradient(ellipse at 50% 35%, #3b1d4c, var(--void) 75%);
             color: #eadff5; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
             padding: 0.9in; border: 10px double var(--gold2); break-after: page; }
    .cover .seals { display: flex; gap: 12px; margin-bottom: 28px; }
    .cover .seals img { width: 1.05in; height: 1.05in; border-radius: 50%; box-shadow: 0 0 16px var(--cyan); }
    .cover h1 { color: var(--gold2); font-size: 50pt; text-shadow: 0 0 18px #b35cff; }
    .cover h1::after { color: var(--gold2); }
    .cover h2 { font-size: 21pt; color: var(--cyan); letter-spacing: 3px; margin: 10px 0 18px; }
    .cover p { font-size: 13pt; max-width: 5.6in; }
    .cover em { color: #c9b5dd; }
    @media screen { .cover { width: 8.5in; margin: 20px auto; } }
    """


    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
        return s


    def blocks(lines):
        out, i = [], 0
        while i < len(lines):
            ln = lines[i].rstrip()
            if not ln.strip():
                i += 1
            elif ln.startswith(("# ", "## ", "### ")):
                n = len(ln.split(" ")[0])
                out.append(f"<h{n}>{inline(ln[n + 1:])}</h{n}>"); i += 1
            elif ln.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
                t = "<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
                t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[2:])
                out.append(t + "</table>")
            elif ln.startswith("- "):
                html_list, open_sub = "<ul>", False
                while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("  - ")):
                    if lines[i].startswith("  - "):
                        if not open_sub:
                            html_list = html_list[:-5] + "<ul>"; open_sub = True
                        html_list += f"<li>{inline(lines[i][4:])}</li>"
                    else:
                        if open_sub:
                            html_list += "</ul></li>"; open_sub = False
                        html_list += f"<li>{inline(lines[i][2:])}</li>"
                    i += 1
                if open_sub:
                    html_list += "</ul></li>"
                out.append(html_list + "</ul>")
            elif ln.startswith(">"):
                paras, cur = [], []
                while i < len(lines) and lines[i].startswith(">"):
                    t = lines[i][1:].strip()
                    if t:
                        cur.append(inline(t))
                    elif cur:
                        paras.append(" ".join(cur)); cur = []
                    i += 1
                if cur:
                    paras.append(" ".join(cur))
                out.append("<blockquote>" + "".join(f"<p>{p}</p>" for p in paras) + "</blockquote>")
            else:
                para = []
                while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |>|<!--)", lines[i]):
                    para.append(inline(lines[i].strip())); i += 1
                if para:
                    out.append("<p>" + " ".join(para) + "</p>")
                else:
                    i += 1
        return "".join(out)


    BOX = re.compile(r"<!-- box\.(\w+): (.+?) -->\n(.*?)<!-- /box -->", re.S)
    STATION = re.compile(r"<!-- station: (\d) · (crest_\d) -->\n(.*?)<!-- /station -->", re.S)
    COVER = re.compile(r"<!-- cover -->\n(.*?)<!-- /cover -->", re.S)


    def render_chunk(chunk):
        pieces, pos = [], 0
        pattern = re.compile("|".join(f"(?:{p.pattern})" for p in (BOX, STATION, COVER)), re.S)
        for m in pattern.finditer(chunk):
            pieces.append(blocks(chunk[pos:m.start()].splitlines()))
            text = m.group(0)
            if (b := BOX.match(text)):
                kind, title, body = b.groups()
                pieces.append(f'<div class="box {kind}"><div class="bt">{inline(title)}</div>{blocks(body.splitlines())}</div>')
            elif (s := STATION.match(text)):
                _, crest, body = s.groups()
                pieces.append(f'<div class="station"><img src="img/{crest}.png" alt=""><div>{blocks(body.splitlines())}</div></div>')
            elif (c := COVER.match(text)):
                body = c.group(1).splitlines()
                seals = blocks(body[:1]).replace("<p>", '<div class="seals">').replace("</p>", "</div>")
                pieces.append(f'<div class="cover">{seals}{blocks(body[1:])}</div>')
            pos = m.end()
        pieces.append(blocks(chunk[pos:].splitlines()))
        return "".join(pieces)


    md = (D / "DM_Guide.md").read_text()
    chunks = md.split("<!-- page -->")
    cover, rest = chunks[0], chunks[1:]
    body = render_chunk(cover) + '<div class="sheet">' + "".join(
        f'<section class="page">{render_chunk(c)}</section>' for c in rest) + "</div>"
    out = D / "DM_Guide.html"
    out.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                   "<title>The Von Zarovich Estate — Dungeon Master's Grimoire</title>"
                   f"<style>{CSS}</style></head><body>{body}</body></html>")
    render_html(out, D / 'DM_Guide.pdf', budget_ms=10000)
    print('Built DM Guide HTML + PDF')
