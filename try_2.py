import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def find_section_pages(pdf_path):
    start_page, end_page = None, None
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[2:], start=3):  # Start from the third page
            text = page.extract_text()
            if "HOW SUPPLIED/STORAGE AND HANDLING" in text and start_page is None:
                start_page = i  # Pages are 1-indexed
            if "PATIENT COUNSELING INFORMATION" in text and start_page is not None:
                end_page = i - 1  # End page is the page before this one
                break
    
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
pdf_path = "path_to_your_pdf.pdf"
start_page, end_page = find_section_pages(pdf_path)

if start_page is not None:
    print(f"Start Page: {start_page}, End Page: {end_page}")
    output_path = "output_section.pdf"
    extract_pages(pdf_path, start_page, end_page, output_path)
else:
    print("16th section not found in the document.")
