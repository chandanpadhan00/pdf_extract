import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def extract_section_content(pdf_path, start_header, end_header):
    content_elements = []
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
                    content_elements.append(('text', text[start_index:]))
                elif end_header in text and start_found:
                    # Extract text before the end header
                    end_index = text.find(end_header)
                    content_elements.append(('text', text[:end_index]))
                    break
                elif start_found:
                    content_elements.append(('text', text))
            
            if start_found:
                tables = page.extract_tables()
                for table in tables:
                    content_elements.append(('table', table))
    
    return content_elements

def create_pdf_from_elements(content_elements, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    for element_type, element_content in content_elements:
        if element_type == 'text':
            paragraphs = [Paragraph(line, style) for line in element_content.split('\n')]
            elements.extend(paragraphs)
            elements.append(Spacer(1, 0.2 * inch))  # Add space between sections
        elif element_type == 'table':
            table = Table(element_content)
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
            elements.append(Spacer(1, 0.2 * inch))  # Add space after table

    doc.build(elements)

# Main processing
pdf_path = "path_to_your_pdf.pdf"
start_header = "HOW SUPPLIED/STORAGE AND HANDLING"
end_header = "PATIENT COUNSELING INFORMATION"
content_elements = extract_section_content(pdf_path, start_header, end_header)

if content_elements:
    output_path = "output_section.pdf"
    create_pdf_from_elements(content_elements, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
