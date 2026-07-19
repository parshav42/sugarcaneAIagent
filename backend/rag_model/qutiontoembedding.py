"""RAG orchestration: embeddings + retrieval + LLM generation.

This module returns a plain string answer. It never exposes internal exceptions to users.
If DEBUG=true, additional debug information (retrieved context and error text) is returned.
"""
import os
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from . import jaiss as j
from .llmmodule import LLM

logger = logging.getLogger(__name__)
DEBUG = os.getenv('DEBUG', '').lower() == 'true'

class quembedding:
    def __init__(self, embed_model='all-MiniLM-L6-v2', llm_model=None):
        self.model = SentenceTransformer(embed_model)
        self.llm_model = llm_model or os.getenv('RAG_LLM_MODEL', 'google/flan-t5-base')

    def get_answer(self, question, top_k_faiss=3, top_k_bm25=3):
        try:
            # Embed query
            query_embedding = self.model.encode(question)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')

            # FAISS search
            try:
                distances, indices = j.index.search(query_embedding, top_k_faiss)
                faiss_indices = list(indices[0])
            except Exception:
                faiss_indices = []

            # BM25 search
            tokenized_query = question.split()
            try:
                bm25_scores = j.bm25.get_scores(tokenized_query)
                bm25_indices = list(np.argsort(bm25_scores)[::-1][:top_k_bm25])
            except Exception:
                bm25_indices = []

            # Combine results (preserve order, unique)
            results = list(dict.fromkeys(faiss_indices + bm25_indices))

            # Build context text but DO NOT expose it unless DEBUG
            if results:
                context_items = [j.chunks[i]['sentence_chunk'] for i in results]
                context_text = '\n\n'.join(context_items)
            else:
                context_text = ''

            # Build prompt
            prompt = f"Use the following context to answer the question. If the answer is not contained in the context, answer concisely based on general knowledge.\n\nContext:\n{context_text}\n\nQuestion: {question}\n\nAnswer:"

            # Call LLM (safe - LLM.generate returns None on failure)
            llm = LLM(model_name=self.llm_model)
            answer = llm.generate(prompt)

            if answer is None or (isinstance(answer, str) and answer.strip() == ''):
                # Log detailed info server-side
                logger.error("LLM returned no answer for question. Model: %s", self.llm_model)
                logger.debug("Context used: %s", context_text)

                if DEBUG:
                    # Return helpful debug text for developers (not for production users)
                    return f"[ERROR generating answer]\n\nContext:\n{context_text}\n\nQuestion:\n{question}"

                # Friendly user-facing message
                return "Sorry, I couldn't generate an answer. Please try again."

            # Successful answer
            return answer

        except Exception as e:
            # Catch-all: log full trace and return friendly message
            logger.exception("Unexpected error in get_answer")
            if DEBUG:
                return f"[UNEXPECTED ERROR] {e}"
            return "Sorry, I couldn't generate an answer. Please try again."
