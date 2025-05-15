from fastapi import FastAPI, UploadFile, File, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from .resume_parser import parse_resume
from .llm_screening import screen_resume_with_llm

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/screen_resumes/")
def screen_resumes(
    job_code: str = Header(None),
    position_name: str = Header(None),
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not job_code or not position_name:
        return {"error": "Job code and position name headers are required."}
    if not job_description:
        return {"error": "Job description is required."}
    results = []
    for file in files:
        # Save the uploaded file temporarily
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f_out:
            f_out.write(file.file.read())
        try:
            resume_info = parse_resume(file_location)
            resume_info['filename'] = file.filename
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})
            continue
        screening = screen_resume_with_llm(job_description, resume_info)
        results.append(screening)
        # Optionally, remove the file after processing
        os.remove(file_location)
    return {"results": results} 