from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("1924, 1824.pdf")

number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

print(text)
