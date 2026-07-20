from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag_model.chunker import Chunker
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pandas as pd


model_em = SentenceTransformer("all-MiniLM-L6-v2")
def pdf(pdf_path):

    pdf = PdfReader(pdf_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
        # print(text)
    return text
def chunker(text):

    chuks = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,)

    return chuks.split_text(text)


def embbeding(extrct_text):
    em = model_em.encode(extrct_text)
    print("text_embeding")
    return em

def run_faiss(emm):


    embedding = np.array(emm).astype('float32')

    index = faiss.IndexFlatL2(embedding.shape[1])
    index.add(embedding)

    return index
def query():

    text = pdf('/home/parshav/PycharmProjects/sugarcaneAIagent1/backend/rag_model/soya.pdf')
    p = chunker(text)
    em = embbeding(p)
    index = run_faiss(em)
    while True:
        uset_text = input("\nplease enter your query")

        if uset_text == "q":
            break

        f_uset_text = model_em.encode(uset_text)
        query = np.array(f_uset_text).astype('float32').reshape(1, -1)
        dis, indicis = index.search(query, 5)
        contex = []
        for i in indicis[0]:
            contex.append(p[i])
        print(contex)




    #

    #
    #

    #


    #


query()









