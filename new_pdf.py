import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

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
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            pass

        def footer(self):
            pass

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    
    pdf.output(output_path)

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
