import os
import re
import pdfplumber
from docx import Document

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else None

def extract_name(text):
    # Very basic: take the first line as name
    lines = text.strip().splitlines()
    return lines[0] if lines else None

def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        text = parse_pdf(file_path)
    elif ext == '.docx':
        text = parse_docx(file_path)
    else:
        text = parse_txt(file_path)
    # Extract basic info
    name = extract_name(text)
    email = extract_email(text)
    return {
        'raw_text': text,
        'name': name,
        'email': email
    } 