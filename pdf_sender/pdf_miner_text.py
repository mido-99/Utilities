from pdfminer.high_level import extract_text
import re


pdf_file = 'Antrag DSGVO.pdf'

text_1 = extract_text(pdf_file, page_numbers=[0])
# last = text_1.find('Bewerberdaten,')
# last_len = len("Bewerberdaten,")
# text_1_edit_1 = text_1[: last+last_len]

match_1 = re.search(r"Bewerberdaten,", text_1)
text_1_edit_1 = text_1[:match_1.end()]
corrupted = text_1[match_1.end():]
page_text = re.sub(r"([A-z0-9]{1})(\n{1})", r'\1', corrupted)
page_header = re.sub(r"(.+)(\n{1})", r'\1', page_text)[:-1].lstrip()

with open('cont_1.txt', 'w') as f:
    f.write(page_header + 2*'\n')
    f.write(text_1_edit_1)