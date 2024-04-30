import PyPDF2

pdf_file = 'Antrag DSGVO.pdf'

with open(pdf_file, 'rb') as f:
    pdf_reader = PyPDF2.PdfReader(f)
    num_pages = len(pdf_reader.pages)
    pdf_writer = PyPDF2.PdfWriter(f)
    
    page_1 = pdf_reader.pages[0]
    text_1 = page_1.extract_text()
    
    with open('cont_1.txt', 'w', encoding='utf-8') as f:
        f.write(text_1.replace('\n', ' '))
    