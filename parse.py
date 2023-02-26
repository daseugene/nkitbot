from PyPDF2 import PdfReader


reader = PdfReader("1924, 1824.pdf")
page = reader.pages[0]


parts = []

def visitor_body(text, cm, tm, fontDict, fontSize):
    y = tm[5]
    if y > 50 and y < 720:
        parts.append(text)



page.extract_text(visitor_text=visitor_body)
text_body = "".join(parts)

print(parts)