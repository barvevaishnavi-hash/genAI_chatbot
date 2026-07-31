from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_response, clear_memory
from pdf_reader import extract_text_from_pdf
import shutil
import os

app = FastAPI()

# Store extracted PDF text
pdf_text = ""

# Enable CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "GenAI Chatbot Backend Running 🚀"}


@app.post("/chat")
def chat(request: ChatRequest):
    global pdf_text

    reply = get_response(request.message, pdf_text)

    return {
        "reply": reply
    }


@app.post("/clear")
def clear_chat():
    global pdf_text

    clear_memory()
    pdf_text = ""

    return {
        "message": "Chat memory cleared successfully!"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text

    # Accept only PDF files
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Please upload a PDF file only."
        }

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(file_path)

    # Check if PDF contains readable text
    if not pdf_text.strip():
        return {
            "message": "PDF uploaded, but no readable text was found.",
            "characters": 0
        }

    return {
        "message": "PDF uploaded successfully!",
        "characters": len(pdf_text)
    }