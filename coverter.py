import os
import fitz  # PyMuPDF
import matplotlib.pyplot as plt

def pdf_to_images(pdf_path, output_dir, dpi=300):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each page
    for i in range(len(pdf_document)):
        page = pdf_document.load_page(i)
        
        # Render the page to a pixmap with specified DPI
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

        # Save the pixmap as an image file
        image_path = os.path.join(output_dir, f'page_{i+1}.png')
        pix.save(image_path, 'png')
        print(f'Saved: {image_path}')

    # Close the PDF document
    pdf_document.close()

if __name__ == "__main__":
    pdf_path = r'C:\Users\yahya\Desktop\ocrscan\cinpdf.pdf'
    output_dir = r'C:\Users\yahya\Desktop\ocrscan\output'
    
    # Check if the PDF path exists
    if not os.path.isfile(pdf_path):
        print(f"Error: The PDF file at {pdf_path} does not exist.")
    else:
        print(f"PDF file found at {pdf_path}.")
        pdf_to_images(pdf_path, output_dir)
