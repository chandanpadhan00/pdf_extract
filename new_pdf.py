import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def extract_section_content(pdf_path, start_header, end_header):
    content = []
    tables = []
    start_found = False
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 1:  # Skip the second page which is index
                continue
            text = page.extract_text()
            if text:
                if start_header in text and not start_found:
                    start_found = True
                    # Extract text after the start header
                    start_index = text.find(start_header)
                    content.append(text[start_index:])
                    tables.extend(page.extract_tables())
                elif end_header in text and start_found:
                    # Extract text before the end header
                    end_index = text.find(end_header)
                    content.append(text[:end_index])
                    break
                elif start_found:
                    content.append(text)
                    tables.extend(page.extract_tables())
    
    return "\n".join(content), tables

def create_pdf_from_text_and_tables(content, tables, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    
    # Add text content
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    paragraphs = [Paragraph(line, style) for line in content.split('\n')]
    elements.extend(paragraphs)
    
    # Add tables
    for table_data in tables:
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    
    doc.build(elements)

# Main processing
pdf_path = "path_to_your_pdf.pdf"
start_header = "HOW SUPPLIED/STORAGE AND HANDLING"
end_header = "PATIENT COUNSELING INFORMATION"
content, tables = extract_section_content(pdf_path, start_header, end_header)

if content:
    output_path = "output_section.pdf"
    create_pdf_from_text_and_tables(content, tables, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
