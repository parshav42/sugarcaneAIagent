from sentence_transformers import SentenceTransformer


class embedding:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")


    def mo(self, chunks):

        embeddings = self.model.encode(chunks)
        # print(len(chunks))
        # print(embeddings.shape)
        return embeddings













