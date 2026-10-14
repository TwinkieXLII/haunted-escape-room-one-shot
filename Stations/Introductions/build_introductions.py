from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter
root=Path(__file__).resolve().parents[2]
out=root/'Stations/Introductions'
entries=[
('The Library','Empty hands. Watchful eyes.',[
'The door sighs shut behind you, stirring a cloud of dust that glitters in the candlelight. Tall bookshelves crowd the walls, their shelves bowed beneath cracked leather volumes. Somewhere among them, a page turns. Neither of you touched a book.',
'Six stone ancestors stand in shadowed alcoves, their empty hands extended as if expecting gifts. Small nameplates identify Victoria, Alexi, Teresa, Valerius, Borislav, and Barov. Their faces are stern enough to make whispering feel compulsory. Barov stands higher than the others, on a tall plinth.',
'A rumpled velvet runner covers part of a heavy reading table. Six carved relics rest upon it: a book, a scythe, a dagger, a spear, a hammer, and a crown. Candle flames tremble across their edges. Behind the statues, the Archive Gate remains firmly closed.',
'Above the fireplace crouches a stone gargoyle. You could swear its eyes follow your hands. A log cracks in the hearth, loud as a snapped bone. For a moment, every statue seems to be waiting for you to make the first move.'
]),
('The Alchemist’s Laboratory','Something sweet. Something sulfurous.',[
'Warm air rolls out of the laboratory, carrying the smell of burnt sugar, old candle wax, and something that probably should not be bubbling. Glass tubes twist through the shadows like transparent roots. Somewhere behind a cupboard, a tiny drip keeps time.',
'Ten amber bottles stand in a brass rack, numbered one through ten. Each has the same dark contents and a black wax seal. In the wavering lamplight, they look exactly alike. No helpful label says what is inside.',
'A two-pan brass balance occupies the workbench. Its beam hangs beneath the spread wings of a grinning metal bat. Both pans are empty. Nearby, a writing desk disappears beneath papers and ink stains, while dusty ingredient jars crowd a crooked shelf.',
'In front of the sealed iron exit, a stone jester holds out a shallow brass bowl. Its cap curls into horns; its carved grin is much too wide. The bowl is empty. The jester looks delighted about that.',
'A green bubble rises in a distant flask and bursts with a rude little pop. The silence afterward feels expectant.'
]),
('The Clockwork Observatory','The stars are watching. The clock is moving.',[
'The stairs curl upward into a round room of brass, cold glass, and midnight blue. A painted sky sweeps across the domed ceiling. Constellations glitter overhead, their shapes half-lost among the stars. The air smells of metal polish and long-cold candle smoke.',
'A huge brass vault door fills the far wall. Four empty pegs sit in a row, numbered one through four, with a crank handle at the center. A small arrow and a bronze inscription catch the light above the mechanism.',
'On the worktable lie seven loose brass gears. Their teeth make uneven little shadows across the tabletop. Beside them sit an astrolabe and a star chart. Everything looks as though its owner stepped away in the middle of an experiment and never came back.',
'Then the great wall clock strikes.',
'Something steps out of its face: an empty suit of armor, suspended around a knot of whirring gears. A pendulum blade swings from one gauntlet. There is no person inside. There is only the ticking.',
'The phantom turns toward you. The vault stays shut. Tick. Tick. Tick.'
]),
('The Mimic Menagerie','Four arches. Four keys. An uncomfortable silence.',[
'The door seals behind you with a soft, final click. Dust and old lamp oil hang in the air. The room is round, its walls disappearing upward into purple-lit shadow.',
'Four stone arches stand along the far wall, numbered I, II, III, and IV in tarnished brass. Beneath each arch, a silver key with a wolf-shaped crest rests on a plain stone pedestal. The keys look exactly alike. So do the waiting pedestals.',
'A stone table stands back from the arches. Four wands rest in carved cradles: one shines with a sunlike crystal, one curls around a little serpent skull, one gleams green, and one ends in a ghostly sculpted hand. Their labels read Bright Light, Poison, Acid, and Mage Hand.',
'Brass studs form a line across the flagstones between the table and the arches. Along the walls, torch flames lean and straighten though you feel no breeze.',
'Nothing leaps out. Nothing growls. Nothing conveniently explains itself. The four silver keys simply wait, as if they have all the time in the world.',
'Behind you, the door handle refuses to turn.'
]),
('The Collapsing Armory','Watch your step. Mind your words.',[
'A narrow armory stretches toward a heavy metal door. Eight weapon racks line the walls, each bearing a brass tag etched in an unfamiliar script. Dust hangs between the blades like old cobwebs.',
'A warning above the entrance catches your eye: “Mind your tongue. The forbidden word is T---.” Beneath it, four letters are scratched out so deeply that the stone has splintered.',
'Then the ceiling moves.',
'Iron pistons groan. Long spikes descend by a slow, unmistakable inch. Strange glowing words flicker across the stone above you, too scattered to take in at a glance. A carved gargoyle face peers down from the center of the ceiling.',
'Directly below it lies a narrow iron drainage grate. Cold, damp air breathes up between the bars. Somewhere below the floor, metal gives a faint clink.',
'At the far end, a stone mouth is carved into the closed blast door. Its lips remain pressed together. The weapons do not move. The ceiling does.',
'The room seems to be listening.'
])]
style=ParagraphStyle('body',fontName='Times-Roman',fontSize=14.5,leading=20,textColor=HexColor('#25152e'),spaceAfter=13)
small=ParagraphStyle('small',fontName='Helvetica',fontSize=10.5,leading=14,textColor=HexColor('#48394d'))
writer=PdfWriter()
for i,(title,sub,paras) in enumerate(entries,1):
 station_dir=root/f'Art/Station_{i}'
 station_dir.mkdir(parents=True,exist_ok=True)
 path=station_dir/f'Station_{i}_Player_Introduction.pdf'
 c=canvas.Canvas(str(path),pagesize=(612,792))
 c.setTitle(f'Station {i}: {title} - Player Introduction')
 c.setFillColor(HexColor('#fcf8ef'));c.rect(36,36,540,720,fill=1,stroke=0)
 c.setStrokeColor(HexColor('#b48c42'));c.setLineWidth(1.5);c.rect(42,42,528,708,fill=0,stroke=1)
 c.setFillColor(HexColor('#2c1438'));c.rect(42,637,528,113,fill=1,stroke=0)
 c.setFillColor(HexColor('#ffd700'));c.setFont('Helvetica-Bold',10);c.drawString(62,727,f'VON ZAROVICH ESTATE  /  STATION {i}')
 c.setFillColor(HexColor('#ffffff'));c.setFont('Times-Bold',26);c.drawString(62,690,title)
 c.setFillColor(HexColor('#ddd1e5'));c.setFont('Times-Italic',13);c.drawString(62,663,sub)
 y=613
 for text in paras:
  p=Paragraph(text,style);w,h=p.wrap(488,600)
  p.drawOn(c,62,y-h);y-=h+12
 if i==5:
  note='Before entering, read silently: the forbidden word is <b>TRAP</b>. Saying it, its forms (such as “trapped”), compounds, or spelling it aloud triggers the room. Writing or pointing is allowed. Confirm the rule with the DM before the timer starts.'
 else:note='What do you do? Talk with your partner. Tell the DM what you want to examine or try. Your character sheet may give you ideas.'
 p=Paragraph(note,small);w,h=p.wrap(468,150)
 assert y>h+90,(i,y,h)
 c.setStrokeColor(HexColor('#b48c42'));c.line(62,91+h,550,91+h)
 p.drawOn(c,72,76)
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#665b69'));c.drawString(62,53,'PLAYER INTRODUCTION  •  Read together before you begin.')
 c.showPage();c.save()
 reader=PdfReader(str(path));assert len(reader.pages)==1
 writer.add_page(reader.pages[0])
 md=f'# Station {i}: {title}\n\n*{sub}*\n\n'+'\n\n'.join(paras)+'\n\n---\n\n'+note.replace('<b>','**').replace('</b>','**')+'\n'
 (root/'Stations/Introductions'/f'Station_{i}_Player_Introduction.md').write_text(md)
with (out/'All_Stations_Player_Introductions.pdf').open('wb') as f:writer.write(f)
print('Verified five single-page PDFs and a five-page combined pack.')
