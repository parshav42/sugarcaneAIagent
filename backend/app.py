from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from predict import predict
import shutil
import os

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

@app.post("/predict")
async def detect(file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict(image_path)
    return result