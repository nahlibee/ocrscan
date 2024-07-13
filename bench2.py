import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Iterate through the pages and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    
    return text

def main(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    print(text)

# Path to your PDF file
pdf_path = r'C:\Users\yahya\Desktop\stag2\output\OCRmyPDF\output.pdf'
main(pdf_path)