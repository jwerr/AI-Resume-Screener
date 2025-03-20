import PyPDF2
import os

def extract_text_pypdf2(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

pdf_folder = "data/output"  # Folder containing PDFs
output_folder = "output_texts/"  # Folder to save extracted text files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all PDFs in the folder
for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):  # Process only PDF files
        pdf_path = os.path.join(pdf_folder, file)
        text = extract_text_pypdf2(pdf_path)

        # Save extracted text to a .txt file
        txt_filename = os.path.splitext(file)[0] + ".txt"  # Change .pdf to .txt
        txt_path = os.path.join(output_folder, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        print(f"Extracted text saved to {txt_path}")
