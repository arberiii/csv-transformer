from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import os

from processing import get_csv_headers, find_most_similar_word

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
    header = get_csv_headers(df)
    concept = "date time"
    most_similar_word, similarity = find_most_similar_word(header, "date time")
    print(f"The most similar word to '{concept}' is '{most_similar_word}' with a similarity score of {similarity:.4f}")

    filtered_columns = [col for col in df.columns if most_similar_word in col]
    filtered_df = df[filtered_columns]
    new_date_time_header_title = 'Date time'
    new_headers = {col: f"{new_date_time_header_title}" for i, col in enumerate(filtered_columns)}
    filtered_df = filtered_df.rename(columns=new_headers)
    processed_file_path = os.path.join(PROCESSED_FOLDER, 'processed_' + os.path.basename(file_path))
    filtered_df.to_csv(processed_file_path, index=False)
    return processed_file_path
