from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100
        )

    def split_text(self, text):
        
        return self.splitter.split_text(text)