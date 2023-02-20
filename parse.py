from PyPDF2 import PdfReader


reader = PdfReader("1824.pdf")
num_of_pages = len(reader.pages)
page = reader.pages[0]
print(page.extract_text((0, 90)))
 



class StudentParse:
    pass




class TeacherParse:
    pass

