import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

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

def extract_pages_with_blanks(pdf_path, start_page, end_page, start_offset, end_offset, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    if end_page is None:
        end_page = len(reader.pages)
        
    for page_num in range(start_page - 1, end_page):  # pages are 0-indexed
        page = reader.pages[page_num]
        if page_num == start_page - 1:
            text = page.extract_text()
            new_text = text[start_offset:]
            page.clear_contents()
            page.insert_text(new_text)
        elif page_num == end_page - 1:
            text = page.extract_text()
            new_text = text[:end_offset]
            page.clear_contents()
            page.insert_text(new_text)
        writer.add_page(page)
    
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Main processing
pdf_path = "path_to_your_pdf.pdf"
start_page, end_page, start_offset, end_offset = find_section_pages(pdf_path)

if start_page is not None:
    print(f"Start Page: {start_page}, End Page: {end_page}")
    output_path = "output_section.pdf"
    extract_pages_with_blanks(pdf_path, start_page, end_page, start_offset, end_offset, output_path)
    print(f"Extracted content to {output_path}")
else:
    print("16th section not found in the document.")
