from printkit.common import ROOT, render_html, merge_pdfs

def build():
    """Build finale script, cards, five-crest gate and complete Letter print kit."""
    from pathlib import Path
    import html,re,math
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor,white
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak
    from pypdf import PdfReader
    D=ROOT / "Finale"
    PURPLE=HexColor('#2C1438'); GOLD=HexColor('#B78C39'); PALE=HexColor('#F2EEF7')
    styles={
     'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.5,leading=14,spaceAfter=6,textColor=PURPLE),
     'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=21,leading=25,spaceAfter=12,textColor=PURPLE,keepWithNext=True),
     'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=14,leading=18,spaceBefore=10,spaceAfter=6,textColor=PURPLE,keepWithNext=True),
     'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=11.5,leading=15,spaceBefore=6,spaceAfter=4,textColor=PURPLE,keepWithNext=True),
     'quote':ParagraphStyle('quote',fontName='Times-Roman',fontSize=12,leading=16,spaceAfter=8,leftIndent=10,rightIndent=10,textColor=PURPLE),
     'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.5,leading=11,textColor=PURPLE),
    }
    def inline(s):
     s=html.escape(s).replace('✔','Yes').replace('✘','No')
     s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
     s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
     s=re.sub(r'`([^`]+)`',r'\1',s)
     return s

    def mdflows(text):
     ls=text.splitlines();out=[];i=0
     while i<len(ls):
      l=ls[i].strip()
      if not l or l=='---' or l.startswith('<!--'):i+=1;continue
      if l.startswith('|'):
       rows=[]
       while i<len(ls) and ls[i].strip().startswith('|'):
        raw=ls[i].strip().strip('|').split('|')
        if not all(re.fullmatch(r'\s*:?-+:?\s*',v) for v in raw):rows.append([Paragraph(inline(v.strip()),styles['small']) for v in raw])
        i+=1
       t=Table(rows,colWidths=[540/len(rows[0])]*len(rows[0]),hAlign='LEFT',repeatRows=1)
       t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,GOLD),('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5)]));out.extend([t,Spacer(1,8)]);continue
      h=re.match(r'^(#{1,3}) (.+)',l)
      if h:
       if h[2].startswith('6 · The Unmasking'):out.append(PageBreak())
       out.append(Paragraph(inline(h[2]),styles['h'+str(len(h[1]))]));i+=1;continue
      if l.startswith('>'):
       q=[]
       while i<len(ls) and ls[i].strip().startswith('>'):q.append(ls[i].strip()[1:].strip());i+=1
       out.append(KeepTogether([Paragraph('<br/>'.join(inline(v) for v in q),styles['quote'])]));continue
      if l.startswith('- ') or re.match(r'^\d+\. ',l):out.append(Paragraph(inline(l),styles['body']));i+=1;continue
      parts=[l];i+=1
      while i<len(ls) and ls[i].strip() and not re.match(r'^(#|\||>|- |\d+\. |<!--)',ls[i].strip()):parts.append(ls[i].strip());i+=1
      out.append(Paragraph(inline(' '.join(parts)),styles['body']))
     return out

    def pagefooter(c,doc):
     c.setFillColor(PURPLE);c.setFont('Helvetica',8);c.drawString(36,20,'DM ONLY - Finale script');c.drawRightString(576,20,str(doc.page))
    script=(D/'Finale_Script.md').read_text()
    SimpleDocTemplate(str(D/'Finale_DM_Script.pdf'),pagesize=(612,792),leftMargin=36,rightMargin=36,topMargin=36,bottomMargin=40).build(mdflows(script),onFirstPage=pagefooter,onLaterPages=pagefooter)

    def title(c,s,sub=''):
     c.setFillColor(PURPLE);c.setFont('Helvetica-Bold',20);c.drawString(36,754,s);c.setStrokeColor(GOLD);c.line(36,742,576,742)
     if sub:
      p=Paragraph(inline(sub),styles['body']);_,h=p.wrap(540,100);p.drawOn(c,36,728-h)
    def footer(c,s):c.setFillColor(PURPLE);c.setFont('Helvetica',8);c.drawString(36,19,s)
    def card(c,title,body,x,y,w,h,cert=False):
     c.setFillColor(PALE if cert else white);c.setStrokeColor(GOLD);c.setDash(3,3);c.roundRect(x,y,w,h,6,stroke=1,fill=1);c.setDash()
     st=ParagraphStyle('cardtitle',parent=styles['h3'],spaceBefore=0,fontSize=18 if cert else 13,leading=22 if cert else 16,alignment=1 if cert else 0)
     t=Paragraph(inline(title),st);_,th=t.wrap(w-20,h);t.drawOn(c,x+10,y+h-12-th)
     flows=mdflows(body);available=h-th-28;used=0
     for f in flows:
      _,fh=f.wrap(w-20,available)
      assert used+fh<=available,(title,used+fh,available)
      f.drawOn(c,x+10,y+h-20-th-used-fh);used+=fh+5

    src=(D/'Finale_Print_Kit.md').read_text()
    cards=re.findall(r'<!-- card(?:\.(\w+))?: (.*?) -->\n(.*?)<!-- /card -->',src,re.S)
    assert len(cards)==19,len(cards)
    c=canvas.Canvas(str(D/'Finale_Print_Kit.pdf'),pagesize=(612,792))
    title(c,'Who Is the Phantom?','Show this board when the first pair returns to the Grand Gate.')
    for i,(_,t,b) in enumerate(cards[:4]):card(c,t,b,36+(i%2)*276,384-(i//2)*266,264,244)
    footer(c,'Player-facing suspect descriptions - combine the evidence from every station.');c.showPage()
    title(c,'Spare Evidence Cards','Use only if a station\'s evidence card is missing; these duplicate E1-E5.')
    for i,(_,t,b) in enumerate(cards[4:9]):card(c,t,b,36+(i%2)*276,486-(i//2)*213,264,196)
    footer(c,'Cut apart. Give evidence at its station reward or replace a missing card at the Gate.');c.showPage()
    title(c,'Minion and Bruiser References','DM / helpers only. Give each helper a cluster. Every player acts once each round.')
    for i,(_,t,b) in enumerate(cards[9:15]):card(c,t,b,36+(i%2)*276,486-(i//2)*213,264,196)
    footer(c,'Keep combat brisk; use the script for waves, capture and unmasking.');c.showPage()
    for copy in range(3):
     title(c,'Case Closed Certificates','Keep hidden until after the unmasking. Four per page; twelve certificates total.')
     for i,(_,t,b) in enumerate(cards[15:19]):card(c,t,b,36+(i%2)*276,378-(i//2)*318,264,300,cert=True)
     footer(c,'Award after the case is solved.');c.showPage()
    c.save()
    # Diagram-native board; five 3-inch crest areas fit on a 15 x 10 inch joined mat.
    c=canvas.Canvas(str(D/'Grand_Gate_Board.pdf'),pagesize=(612,792))
    def gate(c):
     c.setFillColor(PURPLE);c.rect(0,0,1080,720,fill=1,stroke=0)
     c.setStrokeColor(GOLD);c.setLineWidth(6);c.roundRect(20,20,1040,680,28,fill=0)
     c.setFillColor(HexColor('#FFD700'));c.setFont('Times-Bold',30);c.drawCentredString(540,675,'THE GRAND GATE')
     slots=[(540,540,'1 - LIBRARY'),(825,385,'2 - LABORATORY'),(720,140,'3 - OBSERVATORY'),(360,140,'4 - MENAGERIE'),(255,385,'5 - ARMORY')]
     for x,y,label in slots:
      c.setStrokeColor(HexColor('#00C6DA'));c.setLineWidth(2);c.circle(x,y,110,stroke=1,fill=0)
      c.setFillColor(HexColor('#E0D7EC'));c.setFont('Helvetica-Bold',13);c.drawCentredString(x,y-5,label)
     c.setFillColor(HexColor('#FFD700'));c.setFont('Times-Bold',18);c.drawCentredString(540,370,'FIVE CRESTS');c.drawCentredString(540,345,'ONE GATE')
    for half in range(2):
     c.saveState();p=c.beginPath();p.rect(36,36,540,720);c.clipPath(p,stroke=0);c.translate(36-half*540,36);gate(c);c.restoreState()
     footer(c,f'Gate half {half+1}/2 - 100% print. Trim margins and tape centre edges.');c.showPage()
    c.save()
    merge_pdfs([D/name for name in ['Finale_DM_Script.pdf','Grand_Gate_Board.pdf','Finale_Print_Kit.pdf']], D/'Finale_Complete_Print_Pack.pdf')
    print('Built complete finale print pack')
