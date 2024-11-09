import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

if __name__ == "__main__":
    file_path = '/Users/kishore/Downloads/Intel Ethernet Network Adapter E810-CQDA1_CQDA2_61.pdf'
    pdf_text = read_pdf(file_path)
    print(pdf_text)