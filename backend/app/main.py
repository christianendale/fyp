# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from .parser import parse_xml_body_lines, parse_csv_content

import os

app = FastAPI(title="CS3IP Backend")

# CORS for local frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection (change string if using Atlas)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client['forensic_db']
collection = db['records']

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode('utf-8', errors='replace')
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to decode file")
    docs = []
    if file.filename.lower().endswith('.xml'):
        docs = parse_xml_body_lines(text)
    elif file.filename.lower().endswith('.csv'):
        docs = parse_csv_content(text)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    if not docs:
        raise HTTPException(status_code=400, detail="No records parsed")
    # Insert docs in batches to avoid giant single writes
    result = collection.insert_many(docs)
    return {"inserted_count": len(result.inserted_ids)}

@app.get("/records/")
def list_records(limit: int = 20):
    docs = list(collection.find().limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"count": len(docs), "docs": docs}
