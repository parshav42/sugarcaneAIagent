from pypdf import PdfReader


class PDFReader:

    def __init__(self, filename):
        self.filename = filename

    def get_text(self):
        reader = PdfReader(self.filename)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text