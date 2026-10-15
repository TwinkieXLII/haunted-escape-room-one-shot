from printkit.common import ROOT, render_html, merge_pdfs

def build():
    """Build exact-count Station 3 PDFs using generated illustrated surfaces.
    ReportLab paths guarantee teeth/stars; raster art remains unmodified.
    """
    from pathlib import Path
    import math
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from pypdf import PdfReader
    D=ROOT / "Art/Station_3";
    W,H=612,792; PURPLE=HexColor('#2C1438'); GOLD=HexColor('#FFD700'); BRASS=HexColor('#AD813E')
    style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=15,textColor=PURPLE)
    COUNTS=[6,3,7,5,8,4,7] # deliberately scrambled; both 7s use identical art.
    CONSTELLATIONS=[
    ('THE BAT',0,226,[(-63,0),(-22,42),(22,42),(63,0)]),
    ('THE COFFIN',194,112,[(-38,45),(38,45),(45,-20),(0,-55),(-45,-20)]),
    ('THE DRAGON',194,-112,[(-48,66),(0,84),(48,54),(24,6),(-24,-18),(-48,-60),(12,-72)]),
    ('THE RAVEN',0,-226,[(-64,24),(-27,50),(0,12),(27,50),(64,24),(0,-45)]),
    ('THE WOLF',-194,-112,[(-55,48),(-18,72),(24,48),(60,24),(24,-12),(60,-48),(0,-60),(-54,-18)]),
    ('THE SCYTHE',-194,112,[(-58,35),(40,66),(40,-65)])]
    assert sorted(COUNTS)==[3,4,5,6,7,7,8]
    assert [len(x[3]) for x in CONSTELLATIONS]==[4,5,7,6,8,3]

    def para(c,s,x,y,w):
     p=Paragraph(s,style); _,h=p.wrap(w,700);p.drawOn(c,x,y-h);return h

    def title(c,s,sub=None):
     c.setFillColor(PURPLE);c.setFont('Helvetica-Bold',19);c.drawString(36,754,s);c.setStrokeColor(BRASS);c.line(36,742,576,742)
     if sub:para(c,sub,36,729,540)

    def foot(c,s):c.setFillColor(PURPLE);c.setFont('Helvetica',8);c.drawString(36,19,s)
    def img(c,n,x,y,w,h):c.drawImage(str(D/n),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
    def arrow(c,x,y):
     c.setStrokeColor(GOLD);c.setFillColor(GOLD);c.setLineWidth(4);c.line(x,y-23,x,y)
     p=c.beginPath();p.moveTo(x,y+9);p.lineTo(x-9,y-5);p.lineTo(x+9,y-5);p.close();c.drawPath(p,fill=1,stroke=0)
    def gearpath(c,n,x,y,r):
     p=c.beginPath()
     for k in range(n*5):
      a=math.pi/2+2*math.pi*(k/(5*n));radius=r if k%5==2 else r*.55
      xx=x+radius*math.cos(a); yy=y+radius*math.sin(a)
      if k==0:p.moveTo(xx,yy)
      else:p.lineTo(xx,yy)
     p.close();return p

    def gear(c,n,x,y,r=72):
     p=gearpath(c,n,x,y,r)
     c.setFillColor(BRASS);c.drawPath(p,fill=1,stroke=0)
     c.saveState();c.clipPath(p,stroke=0);c.drawImage(str(D/'gear_material_art.png'),x-r,y-r,width=2*r,height=2*r,mask='auto');c.restoreState()
     c.setStrokeColor(PURPLE);c.setLineWidth(2);c.drawPath(p,fill=0,stroke=1)
     # Uniform concentric hub details, independent of tooth count.
     c.setStrokeColor(HexColor('#E5C477'));c.setLineWidth(2);c.circle(x,y,r*.46,stroke=1)
     c.setFillColor(HexColor('#0E0B16'));c.setStrokeColor(BRASS);c.circle(x,y,10,fill=1)

    def drawdoor(c):
     c.drawImage(str(D/'vault_door_art.png'),0,0,width=1080,height=720)
     # Layout labels at actual socket positions; no answer symbols.
     for i,x in enumerate([188,421,656,891]):
      c.setFillColor(PURPLE);c.roundRect(x-49,467,98,30,6,fill=1,stroke=0)
      c.setFillColor(GOLD);c.setFont('Helvetica-Bold',17);c.drawCentredString(x,477,f'PEG {i+1}')
     arrow(c,188,536)

    def drawchart(c):
     c.drawImage(str(D/'star_chart_frame.png'),0,0,width=720,height=720)
     cx=cy=360
     # No decorative stars anywhere; each round point belongs to a labelled figure.
     for name,dx,dy,points in CONSTELLATIONS:
      cx1=cx+dx*.85;cy1=cy+dy*.85
      points=[(px*.9,py*.9) for px,py in points]
      c.setStrokeColor(HexColor('#9DA4BE'));c.setLineWidth(1.8)
      for a,b in zip(points,points[1:]):c.line(cx1+a[0],cy1+a[1],cx1+b[0],cy1+b[1])
      for px,py in points:
       c.setFillColor(GOLD);c.setStrokeColor(HexColor('#5B3C16'));c.setLineWidth(1);c.circle(cx1+px,cy1+py,9,fill=1,stroke=1)
      ly=cy1+min(p[1] for p in points)-30
      c.setFillColor(HexColor('#0E0B16'));c.roundRect(cx1-75,ly-7,150,26,5,fill=1,stroke=0)
      c.setFillColor(GOLD);c.setFont('Helvetica-Bold',14);c.drawCentredString(cx1,ly,name)
     c.setFillColor(HexColor('#0E0B16'));c.setStrokeColor(GOLD);c.setLineWidth(2);c.circle(360,360,45,fill=1)
     c.setFillColor(GOLD);c.setFont('Times-Bold',28);c.drawCentredString(360,350,'XXI')
     arrow(c,360,685)

    def halves(c,draw,width,height,label):
     for half in range(2):
      x=36 if width==1080 else 126
      clipwidth=width/2
      c.saveState(); p=c.beginPath();p.rect(x,36,clipwidth,height);c.clipPath(p,stroke=0)
      c.translate(x-half*clipwidth,36);draw(c);c.restoreState()
      foot(c,f'{label} half {half+1}/2 - 100% print. Trim margins; tape centre edges together.');c.showPage()

    c=canvas.Canvas(str(D/'Station_3_Player_Print_Pack.pdf'),pagesize=(W,H))
    halves(c,drawdoor,1080,720,'Vault door')
    for rowpage,subset in enumerate([COUNTS[:4],COUNTS[4:]]):
     title(c,'Loose Brass Gears','Cut around each toothed silhouette. Keep backs blank and identical. Mix all seven before play.')
     for j,n in enumerate(subset):
      col=j%2;row=j//2; gear(c,n,198+col*216,595-row*230)
     foot(c,'Gear tokens: approximately 2 inches across. All faces use the same material, size and hub.');c.showPage()
    # Starting riddle is player-safe; progressive crank inscription is NOT printed here.
    title(c,'The Gilded Door Plaque','Give this plaque when the players look at the door. Cut the illustrated card out.')
    img(c,'plaque_frame.png',54,327,504,336)
    lines=['Where the arrow wakes the midnight sky,',"The first wing\'s lights on Peg One lie.",'The great wyrm coils through Two and Three -',"One beast, two pegs: alike they\'ll be.",'The reaper\'s blade cuts last of all:',"On Peg Four its lights bid the Phantom fall.",'Let every star bite into brass;',"The sky\'s heart counts the whole - then pass."]
    c.setFillColor(PURPLE);c.setFont('Times-Bold',15)
    for i,s in enumerate(lines):c.drawCentredString(306,565-i*23,s)
    foot(c,'Starting riddle. Keep the progressive clues and answer key with the helper.');c.showPage()
    halves(c,drawchart,720,720,'Astrolabe chart')
    title(c,'The Clockwork Phantom','Cut out the figure and mount in a clip or on a folded cardstock foot.')
    img(c,'clockwork_phantom.png',176,290,260,360)
    para(c,'The Phantom is visible in the room at entry. The helper controls its ticking and attacks; keep its statistics and clue text hidden.',36,240,540)
    foot(c,'Five-inch-tall standee illustration, preserving its generated proportions.');c.showPage();c.save()

    c=canvas.Canvas(str(D/'Station_3_Reveals_Print_Pack.pdf'),pagesize=(W,H))
    title(c,'Reward - Envelope 5','Cut out the 3-inch crest. Put it with Evidence E3 from the helper pack.')
    img(c,'observatory_crest_token.png',198,352,216,216)
    para(c,'Award both crest and E3 on completion. Send the pair to the Grand Gate.',72,300,468)
    foot(c,'DM-held until solve. Progressive clues are in the helper pack.');c.showPage();c.save()

    c=canvas.Canvas(str(ROOT/'tmp/pdfs/station3/assembly.pdf'),pagesize=(W,H))
    title(c,'DM ONLY - Assembly and Validation')
    para(c,'<b>Answer:</b> Pegs 1-4 = 4, 7, 7, 3. Either seven-tooth token fits either middle peg. Seven tokens total: 3, 4, 5, 6, 7, 7, 8. Faces use the same material and size; keep backs unmarked or concealed.<br/><br/><b>Chart:</b> Bat 4 (top, beneath arrow); Coffin 5 (upper right); Dragon 7 (lower right); Raven 6 (bottom); Wolf 8 (lower left); Scythe 3 (upper left). Each circular gold point counts once; lines do not add points. Centre XXI = 21. Sum alone is insufficient: 3+4+6+8 also totals 21.<br/><br/><b>Setup:</b> tape door halves into a 15 x 10 inch board. Tape chart halves into a 10-inch square; optionally cut the circle. Jumble seven gear tokens. Place Phantom. Give plaque on door inspection and chart on astrolabe/desk inspection. Keep the crank inscription behind the screen until Envelope 3.<br/><br/><b>Coaching:</b> ask about pictures, arrow, matching counts and character features before revealing numbers. Phantom strikes at 3:00 then every 2 minutes and after wrong cranks. No initiative; spend at most 30 seconds on a strike. See the helper pages for statistics, bailout, and character hooks.<br/><br/><b>Envelopes:</b> cut helper page 3 into labels/contents. Clues 1-4 are read aloud by the helper at their triggers. Never give players the intact sheet. Envelope 5 needs crest and E3.<br/><br/><b>Before sealing:</b> sample-print at 100%, check gear fit and all counts, add dice, pencil, tape, standee clip and two timers. The complete pack contains DM answers and is for assembly.',36,719,540)
    foot(c,'Exact shapes and counts are added in PDF layout over generated illustrated surfaces.');c.showPage();c.save()
    merge_pdfs([ROOT/'Helpers/Station_3_Helper_Cards.pdf', ROOT/'tmp/pdfs/station3/assembly.pdf'], D/'Station_3_DM_Print_Pack.pdf')
    merge_pdfs([D/name for name in ['Station_3_Player_Introduction.pdf', 'Station_3_Player_Print_Pack.pdf', 'Station_3_Reveals_Print_Pack.pdf', 'Station_3_DM_Print_Pack.pdf']], D/'Station_3_Complete_Print_Pack.pdf')
    print('Built Station 3 print packs')
