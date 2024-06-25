import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def find_section_pages(pdf_path):
    start_page, end_page = None, None
    start_offset, end_offset = 0, 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 1:  # Skip the second page which is index
                continue
            text = page.extract_text()
            if text:
                if "HOW SUPPLIED/STORAGE AND HANDLING" in text and start_page is None:
                    start_page = i + 1  # Pages are 1-indexed
                    start_offset = text.find("HOW SUPPLIED/STORAGE AND HANDLING")
                elif "PATIENT COUNSELING INFORMATION" in text and start_page is not None:
                    end_page = i + 1  # Include the current page as well
                    end_offset = text.find("PATIENT COUNSELING INFORMATION")
                    break
    
    return start_page, end_page, start_offset, end_offset

def extract_section_content(pdf_path, start_page, end_page, start_offset, end_offset):
    content = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page - 1, end_page):
            page = pdf.pages[i]
            text = page.extract_text()
            if i == start_page - 1:
                text = text[start_offset:]
            if i == end_page - 1:
                text = text[:end_offset]
            content += text + "\n"
    
    return content

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
start_page, end_page, start_offset, end_offset = find_section_pages(pdf_path)

if start_page is not None:
    print(f"Start Page: {start_page}, End Page: {end_page}")
    content = extract_section_content(pdf_path, start_page, end_page, start_offset, end_offset)
    output_path = "output_section.pdf"
    create_pdf_from_text(content, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
