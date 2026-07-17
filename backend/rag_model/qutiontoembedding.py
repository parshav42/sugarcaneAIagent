from sentence_transformers import SentenceTransformer

import numpy as np
from . import jaiss as j
from  .chunker import Chunker

# def get_answer(question):
#
#     print("Question:", question)
#
#     # Later your RAG pipeline goes here
#     answer = "This is the answer from Parshav."
#
#     return answer

class quembedding:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")


    def get_answer(self,question):

        embeddings = self.model.encode(question)
        # print(len(chunks))
        # print(embeddings.shape)
        query= np.array([embeddings]).astype('float32')
        #
        dis , indicis = j.index.search(query, 5)
        #
        #
        contex=[]
        #
        c = Chunker()
        for i in indicis[0]:
            contex.append(j.chunks[i])

        #
        # print(contex)
        return contex


