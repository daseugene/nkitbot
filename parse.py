import requests

# from PyPDF2 import PdfReader

# class Reader:
#     @staticmethod
#     async def reader():
#         reader = PdfReader("1824.pdf")
#         num_of_pages = len(reader.pages)
#         page = reader.pages[0]
#         print(page.extract_text((0, 90)))
 



# class StudentParse:
#     pass




# class TeacherParse:
#     pass



res = requests.get('https://www.nkit89.ru/sveden/education/#raspisanie')
print(res.text)
