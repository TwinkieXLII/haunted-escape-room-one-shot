from printkit.common import ROOT, render_html, merge_pdfs

def build():
    """Build Station 2 Letter PDFs from approved artwork. No answer marks on vials.
    Run with the bundled Python runtime (reportlab, pypdf).
    """
    from pathlib import Path
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from pypdf import PdfReader

    D=ROOT / "Art/Station_2"

    TMP=ROOT/'tmp/pdfs/station2'; TMP.mkdir(parents=True,exist_ok=True)
    W,H=612,792
    PURPLE=HexColor('#2C1438'); GOLD=HexColor('#B78C39')
    style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=15,textColor=PURPLE)

    def para(c,text,x,y,width):
     p=Paragraph(text,style); _,height=p.wrap(width,700); p.drawOn(c,x,y-height); return height

    def title(c,text,sub=None):
     c.setFillColor(PURPLE); c.setFont('Helvetica-Bold',19); c.drawString(36,754,text)
     c.setStrokeColor(GOLD); c.line(36,742,576,742)
     if sub: para(c,sub,36,730,540)

    def footer(c,text):
     c.setFillColor(PURPLE); c.setFont('Helvetica',8); c.drawString(36,19,text)

    def image(c,name,x,y,w,h):
     c.drawImage(str(D/name),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')

    def cell(c,name,col,row,cols,rows,x,y,w,h):
     # PDF clipping selects one card without altering the approved source PNG.
     c.saveState(); p=c.beginPath(); p.rect(x,y,w,h); c.clipPath(p,stroke=0)
     c.drawImage(str(D/name),x-col*w,y-(rows-1-row)*h,width=cols*w,height=rows*h,mask='auto')
     c.restoreState()

    def new(name): return canvas.Canvas(str(D/name),pagesize=(W,H))

    c=new('Station_2_Player_Print_Pack.pdf')
    # Two portrait halves form a 15 x 10 inch board; join at the trimmed image edges.
    for half in range(2):
     c.saveState(); p=c.beginPath(); p.rect(36,36,540,720); c.clipPath(p,stroke=0)
     c.drawImage(str(D/'balance_scale_mat.png'),36-half*540,36,width=1080,height=720)
     c.restoreState(); footer(c,f'Scale half {half+1}/2 - print 100%. Trim white margins; tape halves together at centre.'); c.showPage()
    title(c,'Ten Numbered Vials','Cut on the white gutters. Keep backs blank and identical. Each card is approximately 0.8 x 1.33 inches.')
    image(c,'numbered_vials_sheet.png',162,470,288,192)
    para(c,'Place cards inside the matching pan when making a weighing. Five cards fit side by side across the centre of each assembled pan. Keep the numbers visible.',36,435,540)
    c.setStrokeColor(GOLD); c.rect(126,130,360,235)
    para(c,'<b>OFF THE SCALE</b><br/><br/>Put bottles that are on neither pan here.',150,335,312)
    footer(c,'Starting props - no clue or answer is printed on this page.'); c.showPage()
    title(c,'Weighing Log','Write the vial numbers on each pan, then record the DM\'s result. Use a pencil.')
    widths=[54,162,162,162]; xs=[36,90,252,414,576]
    headers=['#','LEFT PAN','RIGHT PAN','RESULT']
    for i in range(4):
     c.setFillColor(PURPLE); c.rect(xs[i],660,widths[i],34,fill=1,stroke=0)
     c.setFillColor(white); c.setFont('Helvetica-Bold',10); c.drawString(xs[i]+8,672,headers[i])
    for r in range(7):
     y=606-r*54
     for i in range(4): c.setStrokeColor(GOLD); c.rect(xs[i],y,widths[i],54,stroke=1)
     c.setFillColor(PURPLE); c.setFont('Helvetica-Bold',12); c.drawString(48,y+24,str(r+1))
     if r==3: para(c,'The scale creaks.',422,y+42,146)
     if r>=4: para(c,'The bat shrieks.',422,y+42,146)
    para(c,'<b>SCALE RESULT</b> - move the marker after each weighing.',36,242,540)
    for i,label in enumerate(['LEFT RISES','LEVEL','RIGHT RISES']):
     x=36+i*180; c.setStrokeColor(GOLD); c.rect(x,155,180,60)
     c.setFillColor(PURPLE); c.setFont('Helvetica-Bold',12); c.drawCentredString(x+90,181,label)
    c.setDash(3,3); c.rect(36,70,108,48); c.setDash(); c.setFont('Helvetica-Bold',12); c.drawCentredString(90,90,'MARKER')
    para(c,'Cut out the marker and place it on LEVEL before play. Keep this result strip beside the scale.',165,114,400)
    footer(c,'Rows 5 onward remain usable; a side effect does not stop the scale.'); c.showPage()
    title(c,'The Jester\'s Altar','Cut out the figure; mount in a standee clip or tape it to a folded cardstock base.')
    image(c,'tricksters_altar_standee.png',150,130,312,437)
    footer(c,'Starting prop - the altar inscription is held separately by the DM.'); c.showPage(); c.save()

    c=new('Station_2_Reveals_Print_Pack.pdf')
    title(c,'DM-held Clues - Envelopes 1 and 3','Cut the two parchment cards apart at their centre line. Keep the ledger hidden until its trigger.')
    image(c,'parchment_handouts.png',63,45,486,629)
    footer(c,'Top: Envelope 1, altar inscription. Bottom: Envelope 3, ledger.'); c.showPage()
    title(c,'Side-effect Cards - DM-held','Cut the six cards apart. Hand over only the rolled card; effects end after 5 minutes or at station end.')
    names=['Bubble Burps','Helium Voice','Radioactive Glow','Sneezing Fit','Heavy Boots','Tingling Fingers']
    effects=['Pink bubbles escape whenever you speak.','Speak in a squeaky helium voice.','You glow! Disadvantage on Stealth.','An uncontrollable fit of sneezes.','Speed reduced by 2 squares.','Move cards using two fingers of each hand.']
    for i in range(6):
     col=i%3; row=i//3; x=36+col*184; top=671-row*300
     cell(c,'comedic_penalty_cards.png',col,row,3,2,x,top-172,172,172)
     c.setStrokeColor(GOLD); c.setDash(3,3); c.rect(x,top-285,172,285); c.setDash()
     para(c,f'<b>{i+1}. {names[i]}</b><br/>{effects[i]}',x+8,top-184,156)
    footer(c,'No damage. Roll d6 for wrong offerings, taste-testing, or the fifth and later weighing.'); c.showPage()
    title(c,'Reward - Envelope 5','Cut out the 3-inch crest. Add Evidence E2 from the helper pack to the same envelope.')
    image(c,'alchemist_crest_token.png',198,354,216,216)
    para(c,'Give the crest and E2 together on completion. The players carry both to the Grand Gate.',72,300,468)
    footer(c,'DM-held reward - do not put it on the starting table.'); c.showPage(); c.save()

    # Keep current helper rules and staged envelopes as the authoritative DM material.
    c=canvas.Canvas(str(TMP/'tracker.pdf'),pagesize=(W,H))
    title(c,'DM ONLY - Suspect Tracker','Choose a mode before play: Fixed (#6) or Trickster\'s Shuffle. Never show this page to players.')
    para(c,'<b>Shuffle procedure:</b> only on equal-count weighings, split current suspects into LEFT / RIGHT / OFF. Keep the largest group; ties may be chosen either way. LEFT group = left rises; RIGHT group = right rises; OFF group = level. Cross off other suspects before announcing the result. Unequal counts give no suspect information.',36,690,540)
    for i in range(10):
     x=36+(i%5)*108; y=478-(i//5)*70; c.setStrokeColor(GOLD); c.rect(x,y,100,58); c.setFillColor(PURPLE); c.setFont('Helvetica-Bold',20); c.drawCentredString(x+50,y+20,str(i+1))
    para(c,'<b>Clear a suspect:</b> cross off its box. Esmeralda clears the lowest-numbered suspect only while at least three remain. An offering while at least two suspects remain is rejected and that offered vial is cleared. Once one remains, it is the counterfeit.<br/><br/><b>Fixed mode:</b> #6 is always the counterfeit. Announce scale results honestly; a level result means #6 was on neither pan.<br/><br/><b>Before sealing:</b> place helper-only instructions in a separate sleeve. Cut the helper labels/contents apart; use the illustrated altar and ledger cards instead of duplicate text cards. Envelope 5 needs both crest and E2.',36,365,540)
    footer(c,'Use the helper sheet for clue timing, penalties, character hooks, and emergency coaching.'); c.showPage(); c.save()
    merge_pdfs([ROOT/'Helpers/Station_2_Helper_Cards.pdf', TMP/'tracker.pdf'], D/'Station_2_DM_Print_Pack.pdf')
    merge_pdfs([D/name for name in ['Station_2_Player_Introduction.pdf', 'Station_2_Player_Print_Pack.pdf', 'Station_2_Reveals_Print_Pack.pdf', 'Station_2_DM_Print_Pack.pdf']], D/'Station_2_Complete_Print_Pack.pdf')
    print('Built Station 2 print packs')
