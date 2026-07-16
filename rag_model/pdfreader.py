from pypdf import PdfReader


class pdf():
    def __init__(self, filename):
        self.filename = filename
        self.reader = PdfReader(self.filename)
        text = []
        for page in self.reader.pages:
            text += page.extract_text()



pdf = pdf("/home/parshav/PycharmProjects/sugarcaneAIagent/rag_model/soya_soya2_merged.pdf")
