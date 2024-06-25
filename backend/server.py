# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    processed_file_path = process_csv(file_path)
    return FileResponse(processed_file_path, media_type='application/octet-stream',
                        filename=os.path.basename(processed_file_path))


def process_csv(file_path):
    df = pd.read_csv(file_path)
    # Perform your data processing here
    # Example: df['new_column'] = df['existing_column'] * 2
    processed_file_path = os.path.join(PROCESSED_FOLDER, 'processed_' + os.path.basename(file_path))
    df.to_csv(processed_file_path, index=False)
    return processed_file_path
