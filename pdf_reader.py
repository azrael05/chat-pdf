import pymupdf
# from pypdf2 import PDFReader as pr
import pdfplumber
class PDFReader:
    def __init__(self):
        pass

    def read_pdf(self, pdf_path):
        doc = pymupdf.open(pdf_path)
        text = ""
        for page in doc:
            text += " " + page.get_textpage()
        return text

    def read_pdfs(self, pdf_paths):
        text = ""
        for pdf in pdf_paths:
            text += "\n" + self.read_pdf(pdf)
        return text
    
    def read(self, pdf_docs):
        text = ""
        for pdf in pdf_docs:
            with pdfplumber.open(pdf) as file:
                all_pages = file.pages
                for page in all_pages:
                    text += page.extract_text() # you can print and check the data from any page in pdf
                
        return text
    # def get_content(self, pdf_docs):
    #     text = ""
    #     for pdf in pdf_docs:
    #         pdf_reader = pr(pdf)
    #         for page in pdf_reader.pages:
    #             text += page.extract_text()
    #     return text