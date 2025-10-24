# CS3IP — Data Management & Information Retrieval

Student: Christian Endale (230035665)  
Supervisor: Dr Amal Htait

## Overview

Web application to upload CSV/XML, as well as parse and store in MongoDB. CRUD via UI as well as fielded & semantic search.

## Tech

-   Frontend: React
-   Backend: FastAPI (Python) + Node.js
-   DB: MongoDB

## Quick start (backend)

See backend/README or run:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
