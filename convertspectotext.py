import PyPDF2
import sys

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convertspectotext.py <pdf_file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    pdf_text = read_pdf(file_path)
    print(pdf_text)