from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from predict import predict
import shutil
import os
from rag_model.qutiontoembedding import quembedding

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------
# Image Prediction
# ------------------------

@app.post("/predict")
async def detect(file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict(image_path)
    return result


class ChatRequest(BaseModel):
    question: str

# Initialize RAG QA object once (cold start may load models)
qu = quembedding()

@app.post("/shetimitra")
async def chat(request: ChatRequest):
    # Return only the final answer string. Backend errors are logged but not exposed.
    answer = qu.get_answer(request.question)
    return {"answer": answer}
