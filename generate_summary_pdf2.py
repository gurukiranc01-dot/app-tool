from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

# Paths
SUMMARY_MD = "PROJECT_LEARNING_SUMMARY.md"
LOGO_PATH = os.path.join("static", "bosch.png")
PDF_PATH = "PROJECT_LEARNING_SUMMARY.pdf"

# Read summary
with open(SUMMARY_MD, encoding="utf-8") as f:
    content = f.read()

# Split into sections for better formatting
sections = content.split("---\n")

# PDF setup
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CenterTitle', parent=styles['Title'], alignment=TA_CENTER, fontSize=22, spaceAfter=20))
styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], textColor=colors.HexColor('#b60000'), spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], fontSize=11, leading=15))

story = []

# Add Bosch logo
if os.path.exists(LOGO_PATH):
    story.append(Image(LOGO_PATH, width=2.5*inch, height=0.7*inch))
    story.append(Spacer(1, 0.2*inch))

# Add title
story.append(Paragraph("BikeVault Project - Complete Learning Summary", styles['CenterTitle']))

for section in sections:
    lines = section.strip().splitlines()
    if not lines:
        continue
    # Section header
    if lines[0].startswith("## "):
        header = lines[0][3:]
        story.append(Paragraph(header, styles['SectionHeader']))
        lines = lines[1:]
    elif lines[0].startswith("# "):
        header = lines[0][2:]
        story.append(Paragraph(header, styles['SectionHeader']))
        lines = lines[1:]
    # Add section content
    text = "<br/>".join(lines)
    story.append(Paragraph(text, styles['NormalText']))
    story.append(Spacer(1, 0.18*inch))

# Save PDF
SimpleDocTemplate(PDF_PATH, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36).build(story)
print(f"PDF generated: {PDF_PATH}")
