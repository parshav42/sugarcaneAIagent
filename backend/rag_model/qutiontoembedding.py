from sentence_transformers import SentenceTransformer
from langchain_core.prompts import ChatPromptTemplate

import numpy as np
from . import jaiss as j
# from  .chunker import Chunker

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


        query_embedding = self.model.encode(question)
        query_embedding = query_embedding.reshape(1, -1).astype("float32")

        distances, indices = j.index.search(query_embedding, 2)
        tokenized_query = question.split()

        bm25_scores = j.bm25.get_scores(tokenized_query)
        bm25_indices = np.argsort(bm25_scores)[::-1][:2]
        results = set(indices[0]) | set(bm25_indices)

        context = [j.chunks[i] for i in results]

        #
        #
        # # Create your multi-turn prompt layout with dynamic variables
        # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", "You are a helpful assistant assigned to the role of {role}."),
        #     ("placeholder", "{chat_history}"),
        #     ("human", "{query}"),
        #     ("placeholder", "{agent_scratchpad}"),  # LangChain injects tool outputs here automatically
        # ])

        return context



