from pathlib import Path
import html
d=Path(__file__).parent
css="""@page{size:letter;margin:.5in}*{box-sizing:border-box}body{margin:0;background:#ddd;color:#25152e;font-family:Georgia,serif}.page{width:7.5in;height:9.95in;background:white;margin:20px auto;padding:0;break-after:page;overflow:hidden}h1{font-size:23px;margin:0 0 12px}h2{font-size:16px;margin:12px 0 6px}p,li{font-size:13px;line-height:1.35}.row{display:flex;justify-content:center;gap:.15in;align-items:flex-start}.cut{border:1px dashed #999}.alcove{width:5in;height:7in;position:relative;margin:.2in auto}.alcove img{width:100%;height:100%;object-fit:contain;background:#0e0b16}.label{position:absolute;bottom:.15in;left:1in;right:1in;text-align:center;background:#d7b45d;border:3px double #2c1438;color:#150d19;font-size:23px;font-weight:bold}.wand{width:2.5in;height:7.5in;object-fit:contain}.reveal{width:2.4in;height:3.36in;object-fit:contain}.plaque{width:6in;height:4in;object-fit:contain;display:block;margin:0 auto}.crest{width:3in;height:3in;object-fit:contain;display:block;margin:.15in auto}.token{width:.65in;height:.65in;border:3px double #ffd700;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font:bold 9px Arial;text-align:center;margin:.1in}.purple{background:#672782}.green{background:#226522}table{border-collapse:collapse;width:100%;font:11px/1.25 Arial}th,td{border:1px solid #aaa;padding:6px;vertical-align:top}th{background:#eee}small{font:11px Arial}.strip{border:3px dotted #bb9736;padding:10px;text-align:center;font-weight:bold}.screen{padding:15px;max-width:900px;margin:auto}@media print{body{background:white}.screen{display:none}.page{margin:0}button{display:none}}"""
def page(title,body):return '<section class="page"><h1>'+title+'</h1>'+body+'</section>'
def doc(title,body):return '<!doctype html><html><head><meta charset="utf-8"><title>'+title+'</title><style>'+css+'</style></head><body><div class="screen"><button onclick="print()">Print</button> Print at 100%, Letter, background graphics ON, browser headers/footers OFF. Cut on dashed edges.</div>'+body+'</body></html>'
players=''
for n in ['I','II','III','IV']:
 players+=page('The Mimic Menagerie',f'<div class="alcove cut"><img src="alcove_master.png"><div class="label">ALCOVE {n}</div></div><p>Cut out the 5 × 7 inch card.</p>')
for a,b in [('bright_light','poison'),('acid','mage_hand')]:
 players+=page('Magical Testing Wands',f'<div class="row"><img class="wand cut" src="wand_{a}.png"><img class="wand cut" src="wand_{b}.png"></div><p>Bookmark cards: 2.5 × 7.5 inches, preserving the generated proportions.</p>')
players+=page('Table Tokens','<h2>Removable charge tokens</h2><div class="row"><div class="token purple">POISON<br>1</div><div class="token green">ACID<br>1</div></div><p>Place each token on its wand’s socket. Hand the token to the DM when used.</p><h2>Brass stud line — table marker</h2><div class="strip">TESTING SIDE • • • • • • • • • • • • • • • • • ALCOVES</div><h2>Investigation notes</h2><table><tr><th>Alcove</th><th>What we tested</th><th>What happened</th></tr>'+''.join(f'<tr style="height:.75in"><td>{n}</td><td></td><td></td></tr>' for n in ['I','II','III','IV'])+'</table>')
(d/'Station_4_Player_Print_Pack.html').write_text(doc('Station 4 — player starting props',players))
reveals=page('DM-held reveals — keep hidden until earned','<p>Place each on the tested alcove only after its reveal. No card has a fixed alcove number.</p><div class="row">'+''.join(f'<img class="reveal cut" src="reveal_{x}.png">' for x in ['illusion','mimic','construct'])+'</div><h2>Mimic standee</h2><p>Cut the mimic silhouette and leave its base tab. Use a standee clip, or fold the tab and tape to a small cardstock foot.</p><h2>Menagerie Crest #4 — success only</h2><img class="crest cut" src="menagerie_crest_token.png">')
reveals+=page('DM-held plaque — Clue 3 only','<p>Keep behind the screen until the wand-rack search earns it, or the 8–9 minute nudge.</p><img class="plaque cut" src="menagerie_plaque.png"><h2>Assembly</h2><p>Cut the 6 × 4 inch plaque apart from these instructions. Print single-sided; do not put a solution on the back.</p>')
(d/'Station_4_Reveals_Print_Pack.html').write_text(doc('Station 4 — DM-held reveal props',reveals))
station=Path('Stations/Station_4_Mimic_Menagerie_Wands_and_Keys.md').read_text()
def table_under(heading):
 part=station.split(heading,1)[1]
 rows=[l for l in part.splitlines() if l.startswith('|')]
 # stop at first table only
 out=[]
 for l in rows:
  if out and ('Layout' in l or 'Wand →' in l):break
  out.append(l)
 return out
# Extract exact tables by contiguous blocks rather than retyping reactions.
def table_after(heading):
 lines=station.split(heading,1)[1].splitlines();rows=[];started=False
 for l in lines:
  if l.startswith('|'): rows.append(l);started=True
  elif started:break
 result='<table>'
 for i,l in enumerate(rows):
  if i==1:continue
  tag='th' if i==0 else 'td'
  result+='<tr>'+''.join(f'<{tag}>'+html.escape(c.strip()).replace('**','').replace('*','')+f'</{tag}>' for c in l.strip('|').split('|'))+'</tr>'
 return result+'</table>'
dm=page('DM ONLY — Menagerie control sheet','<p><b>Starting layout: ____  Current: ____  Pair: __________________</b></p>'+table_after('### Shuffle Tracker')+'<h2>Wand reactions</h2>'+table_after('### Wand Reaction Matrix')+'<h2>Reset</h2><p>Advance A → B → C → D → A. Remove all reveal cards, return both charge tokens, and announce that the contents have moved. Keep alcove cards in place.</p><h2>Hazards</h2><p>Mimic: AC 12, HP 15, +5 bite; 1d8+2 piercing +2 acid (average 6 piercing). Mage Hand absorbs the bite. Murray can restrain it for 2 rounds. Construct: DC 12 Dex, 2d4 damage, half on success. Illusion: gong, no damage. Wrong retrieval resets.</p>')
dm+=page('DM ONLY — Coaching & clue timing','<h2>Start neutrally</h2><p>Four identical silver wolf-crest keys wait under arches. Four wands rest on a table. Describe each key the same way. Do not expose the reveal cards, plaque or crest.</p><h2>2–3 minutes: orientation</h2><p>“What happened to the last people here?” Describe scorches, tooth gouges and sticky residue beyond the brass studs, spread across all four alcoves. Point out the two single charge sockets.</p><h2>5–6 minutes: character hook</h2><p>“Scooby, anything on your sheet that a snack helps with?” Alive identifies the current mimic; fake identifies the current illusion. Neither identifies the real key. Use the current layout.</p><h2>8–9 minutes: logic clue</h2><p>Reveal the plaque after the rack search, or when dust is smeared away. Do not assign its verses to alcove numbers.</p><h2>11 minutes, or reset after 10: emergency</h2><p>Prompt Murray to tap with his bandage whip. Mimic: wet snore. Construct: ticking. Illusion: passes through key. Real: hollow brass bell. Give locations from the current layout. Accept a player’s clever early tap.</p><h2>13–15 minutes</h2><p>At 13 minutes the real key glows if needed. Finish by 15 minutes with a funny cost. Do not stall an early solve.</p><h2>Keep tests fair</h2><p>Use the reaction table’s identical words for identical outcomes. A plain result still conveys evidence. Collect Poison/Acid tokens before resolving the test. A reset clears every previous observation.</p><p><b>Source:</b> Stations/Station_4_Mimic_Menagerie_Wands_and_Keys.md. This is a quick reference; use the station sheet for full adjudication.</p>')
(d/'Station_4_DM_Notes.html').write_text(doc('Station 4 — DM only',dm))
print('Created player pack (7 pages), reveal pack (2 pages), DM notes (2 pages).')
