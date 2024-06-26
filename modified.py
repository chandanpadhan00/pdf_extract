import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def find_section_pages(pdf_path):
    start_page, end_page = None, None
    section_17_start_page = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 1:  # Skip the second page which is index
                continue
            text = page.extract_text()
            if text:
                if "HOW SUPPLIED/STORAGE AND HANDLING" in text and start_page is None:
                    start_page = i + 1  # Pages are 1-indexed
                elif "PATIENT COUNSELING INFORMATION" in text:
                    if start_page is not None:
                        section_17_start_page = i + 1  # Page where section 17 starts
                    break
    
    if section_17_start_page and section_17_start_page == end_page + 1:
        end_page = section_17_start_page - 1
    else:
        end_page = section_17_start_page

    return start_page, end_page

def extract_pages(pdf_path, start_page, end_page, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    if end_page is None:
        end_page = len(reader.pages)
        
    for page_num in range(start_page - 1, end_page):  # pages are 0-indexed
        writer.add_page(reader.pages[page_num])
    
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Main processing
pdf_path = "path_to_your_pdf.pdf"  # Update this path with the actual PDF file path
start_page, end_page = find_section_pages(pdf_path)

if start_page is not None:
    print(f"Start Page: {start_page}, End Page: {end_page}")
    output_path = "output_section.pdf"
    extract_pages(pdf_path, start_page, end_page, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
