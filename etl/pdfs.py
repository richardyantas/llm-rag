import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:                
                text += page_text
    pattern = r'([A-Za-zÁÉÍÓÚÑáéíóúñ\s]+:)(.*?)(?=[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+:|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    paragraphs = []
    for match in matches:
        title = match[0].strip() 
        content = match[1].strip() 
        paragraphs.append(f"{title} {content}")
    return paragraphs
