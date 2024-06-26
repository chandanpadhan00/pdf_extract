import os
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import yellow

def find_section_content(pdf_path):
    start_page, end_page = None, None
    section_16_content = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 1:  # Skip the second page which is index
                continue
            text = page.extract_text()
            if text:
                if "HOW SUPPLIED/STORAGE AND HANDLING" in text and start_page is None:
                    start_page = i + 1  # Pages are 1-indexed
                    start_offset = text.find("HOW SUPPLIED/STORAGE AND HANDLING")
                    section_16_content += text[start_offset:] + "\n"
                elif "PATIENT COUNSELING INFORMATION" in text and start_page is not None:
                    end_page = i + 1
                    end_offset = text.find("PATIENT COUNSELING INFORMATION")
                    section_16_content += text[:end_offset] + "\n"
                    break
                elif start_page is not None:
                    section_16_content += text + "\n"
    
    return start_page, end_page, section_16_content

def highlight_text(content, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    text_object = c.beginText(0.5 * inch, height - 0.5 * inch)
    text_object.setFont("Helvetica", 12)
    
    for line in content.split('\n'):
        if "HOW SUPPLIED/STORAGE AND HANDLING" in line:
            c.setFillColor(yellow)
            c.rect(text_object.getX(), text_object.getY() - 12, width - inch, 14, fill=1, stroke=0)
            c.setFillColor("black")
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()

def process_all_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            start_page, end_page, section_16_content = find_section_content(pdf_path)

            if start_page is not None:
                output_filename = f"{os.path.splitext(filename)[0]}_16thSec.pdf"
                output_path = os.path.join(output_folder, output_filename)
                highlight_text(section_16_content, output_path)
                print(f"Extracted and highlighted content to {output_path}")
            else:
                print(f"16th section not found in {filename}")

# Main processing
input_folder = "path_to_your_input_folder"  # Update this path with the actual input folder path
output_folder = "path_to_your_output_folder"  # Update this path with the actual output folder path

process_all_pdfs(input_folder, output_folder)
