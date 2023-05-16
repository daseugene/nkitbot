import PyPDF2

class Parse:
    def parse_pdf(file_path, keywords):
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text = page.extractText()
                for keywords in keywords:
                    if keywords in text:
                        return text
        return None
