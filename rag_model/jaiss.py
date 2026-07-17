from pdfreader import PDFReader
from chunker import Chunker
from embedding import embedding
import faiss
import numpy as np



reader = PDFReader("soya_soya2_merged.pdf")
text = reader.get_text()

chunker = Chunker()
chunks = chunker.split_text(text)

embedder = embedding()
embedding = embedder.mo(chunks)

embedding= np.array(embedding).astype('float32')

index= faiss.IndexFlatL2(embedding.shape[1])
index.add(embedding)

# query =  embedder.model.encode(["What factors influence soybean growth, development, and seed yield?"])
#
# query= np.array(query).astype('float32')
#
# dis , indicis = index.search(query, 5)
#
#
# contex=[]
#
# for i in indicis[0]:
#     contex.append(chunks[i])
#
# print(contex)
