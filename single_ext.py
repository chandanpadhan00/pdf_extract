import PyPDF2
import pdfplumber
import re
from PyPDF2 import PdfFileReader, PdfFileWriter

def extract_index(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[1]  # 2nd page is index, pages are 0-indexed
        text = page.extract_text()
    return text

def find_section_page_range(index_text):
    lines = index_text.split('\n')
    start_page, end_page = None, None
    for i, line in enumerate(lines):
        if "16  HOW SUPPLIED/STORAGE AND HANDLING" in line:
            # Extract start page from the next line
            start_page = int(re.findall(r'\d+', lines[i+1])[0])
            # Look for the next section to determine the end page
            for j in range(i+2, len(lines)):
                if re.match(r'^\d+\s', lines[j]):  # This line starts with a section number
                    end_page = int(re.findall(r'\d+', lines[j])[0]) - 1
                    break
            break
    return start_page, end_page

def extract_pages(pdf_path, start_page, end_page, output_path):
    reader = PdfFileReader(pdf_path)
    writer = PdfFileWriter()
    
    if end_page is None:
        end_page = reader.getNumPages()
        
    for page_num in range(start_page - 1, end_page):  # pages are 0-indexed
        writer.addPage(reader.getPage(page_num))
    
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Main processing
pdf_path = "path_to_your_pdf.pdf"
index_text = extract_index(pdf_path)
start_page, end_page = find_section_page_range(index_text)

if start_page is not None:
    print(f"Start Page: {start_page}, End Page: {end_page}")
    output_path = "output_section.pdf"
    extract_pages(pdf_path, start_page, end_page, output_path)
else:
    print("16th section not found in the index.")
