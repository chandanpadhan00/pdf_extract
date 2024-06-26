import os
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
    
    if section_17_start_page:
        if section_17_start_page == start_page + 1:
            end_page = section_17_start_page - 1
        else:
            end_page = section_17_start_page
    else:
        end_page = len(pdf.pages)

    return start_page, end_page

def extract_pages(pdf_path, start_page, end_page, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
        
    for page_num in range(start_page - 1, end_page):  # pages are 0-indexed
        writer.add_page(reader.pages[page_num])
    
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

def process_all_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            start_page, end_page = find_section_pages(pdf_path)

            if start_page is not None:
                output_filename = f"{os.path.splitext(filename)[0]}_16thSec.pdf"
                output_path = os.path.join(output_folder, output_filename)
                extract_pages(pdf_path, start_page, end_page, output_path)
                print(f"Extracted content to {output_path}")
            else:
                print(f"16th section not found in {filename}")

# Main processing
input_folder = "path_to_your_input_folder"  # Update this path with the actual input folder path
output_folder = "path_to_your_output_folder"  # Update this path with the actual output folder path

process_all_pdfs(input_folder, output_folder)
