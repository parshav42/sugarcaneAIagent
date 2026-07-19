from .pdfreader import PDFReader
from .chunker import Chunker
from .embedding import embedding
import faiss
import numpy as np
from rank_bm25 import BM25Okapi

# Read and chunk the PDF
reader = PDFReader("/home/parshav/PycharmProjects/sugarcaneAIagent/backend/rag_model/soya_soya2_merged.pdf")
text = reader.get_text()

chunker = Chunker()
chunks_raw = chunker.split_text(text)

# Prepare BM25
tokenized_chunks = [c.split() for c in chunks_raw]
bm25 = BM25Okapi(tokenized_chunks)

# Prepare embeddings and FAISS index
embedder = embedding()
embeddings = embedder.mo(chunks_raw)
embeddings = np.array(embeddings).astype('float32')

_index = faiss.IndexFlatL2(embeddings.shape[1])
_index.add(embeddings)

# Export variables expected by other modules
# chunks is a list of dicts with key 'sentence_chunk' to match prompt formatting
chunks = [{"sentence_chunk": c} for c in chunks_raw]
index = _index

# bm25 is already defined above

