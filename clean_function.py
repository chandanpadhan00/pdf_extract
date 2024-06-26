from copy import deepcopy

def clean_docx(docx_path, cleaned_docx_path):
    doc = Document(docx_path)
    section_16_pattern = re.compile(r"16\s+HOW\s+SUPPLIED/STORAGE\s+AND\s+HANDLING", re.IGNORECASE)
    section_17_pattern = re.compile(r"17\s+PATIENT\s+COUNSELING\s+INFORMATION", re.IGNORECASE)
    
    new_doc = Document()
    copy = False
    
    for element in doc.element.body:
        if element.tag.endswith('p'):
            paragraph = element.xpath('.')[0]
            if section_16_pattern.search(paragraph.text):
                copy = True
            if section_17_pattern.search(paragraph.text):
                break  # Stop copying when section 17 is reached
            if copy:
                new_para = new_doc.add_paragraph()
                new_para._element = deepcopy(paragraph)
        elif element.tag.endswith('tbl') and copy:
            new_table = new_doc.add_table(rows=0, cols=0)
            new_table._element = deepcopy(element)
    
    # Ensure the document has content
    if len(new_doc.paragraphs) == 0 and len(new_doc.tables) == 0:
        new_doc.add_paragraph("No content found between sections 16 and 17.")
    
    new_doc.save(cleaned_docx_path)
