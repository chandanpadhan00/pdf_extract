import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def extract_section_content(pdf_path, start_header, end_header):
    content = []
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
                elif end_header in text and start_found:
                    # Extract text before the end header
                    end_index = text.find(end_header)
                    content.append(text[:end_index])
                    break
                elif start_found:
                    content.append(text)
    
    return "\n".join(content)

def create_pdf_from_text(content, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica", 12)
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    
    text_object = c.beginText(0.5 * inch, height - 0.5 * inch)
    text_object.setFont("Helvetica", 12)
    text_object.setTextOrigin(0.5 * inch, height - 0.5 * inch)
    
    for line in content.split('\n'):
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()

# Main processing
pdf_path = "path_to_your_pdf.pdf"
start_header = "HOW SUPPLIED/STORAGE AND HANDLING"
end_header = "PATIENT COUNSELING INFORMATION"
content = extract_section_content(pdf_path, start_header, end_header)

if content:
    output_path = "output_section.pdf"
    create_pdf_from_text(content, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
