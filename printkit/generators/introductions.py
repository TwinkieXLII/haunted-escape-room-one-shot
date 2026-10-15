"""Single-page player introductions, sourced from editable Markdown."""
import re
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader
from printkit.common import ROOT, merge_pdfs


def read_entry(number):
    source = ROOT / f'Stations/Introductions/Station_{number}_Player_Introduction.md'
    lead, note = source.read_text().split('\n---\n', 1)
    blocks = lead.strip().split('\n\n')
    title = blocks[0].split(': ', 1)[1]
    subtitle = blocks[1].strip('*')
    note = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', note.strip())
    return title, subtitle, blocks[2:], note


def build(stations=None):
    style = ParagraphStyle('body', fontName='Times-Roman', fontSize=14.5, leading=20,
                           textColor=HexColor('#25152e'), spaceAfter=13)
    small = ParagraphStyle('small', fontName='Helvetica', fontSize=10.5, leading=14,
                           textColor=HexColor('#48394d'))
    for number in stations if stations is not None else range(1, 6):
        title, subtitle, paragraphs, note = read_entry(number)
        path = ROOT / f'Art/Station_{number}/Station_{number}_Player_Introduction.pdf'
        path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(path), pagesize=(612, 792))
        c.setTitle(f'Station {number}: {title} - Player Introduction')
        c.setFillColor(HexColor('#fcf8ef')); c.rect(36, 36, 540, 720, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#b48c42')); c.setLineWidth(1.5); c.rect(42, 42, 528, 708, fill=0, stroke=1)
        c.setFillColor(HexColor('#2c1438')); c.rect(42, 637, 528, 113, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffd700')); c.setFont('Helvetica-Bold', 10)
        c.drawString(62, 727, f'VON ZAROVICH ESTATE  /  STATION {number}')
        c.setFillColor(HexColor('#ffffff')); c.setFont('Times-Bold', 26); c.drawString(62, 690, title)
        c.setFillColor(HexColor('#ddd1e5')); c.setFont('Times-Italic', 13); c.drawString(62, 663, subtitle)
        y = 613
        for text in paragraphs:
            paragraph = Paragraph(text, style); _, height = paragraph.wrap(488, 600)
            paragraph.drawOn(c, 62, y-height); y -= height+12
        paragraph = Paragraph(note, small); _, height = paragraph.wrap(468, 150)
        if y <= height+90:
            raise ValueError(f'Station {number} introduction no longer fits one page')
        c.setStrokeColor(HexColor('#b48c42')); c.line(62, 91+height, 550, 91+height)
        paragraph.drawOn(c, 72, 76)
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#665b69'))
        c.drawString(62, 53, 'PLAYER INTRODUCTION  •  Read together before you begin.')
        c.showPage(); c.save()
        if len(PdfReader(path).pages) != 1:
            raise ValueError(f'Station {number} introduction must have one page')
    if stations is None:
        merge_pdfs([ROOT/f'Art/Station_{i}/Station_{i}_Player_Introduction.pdf' for i in range(1, 6)],
                   ROOT/'Stations/Introductions/All_Stations_Player_Introductions.pdf')
    print('Built player introductions from Markdown')
