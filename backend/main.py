from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_response, clear_memory
from fastapi import UploadFile, File
from pdf_reader import extract_text_from_pdf
import shutil
import os

app = FastAPI()
pdf_text = ""

# Allow Streamlit to communicate with FastAPI
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

    return {
        "reply": get_response(
            request.message,
            pdf_text
        )
    }

    return {
        "reply": reply
    }

@app.post("/clear")
def clear_chat():
    clear_memory()
    return {"message": "Chat memory cleared"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf_text = extract_text_from_pdf(file_path)

    return {
        "message": "PDF uploaded successfully!",
        "characters": len(pdf_text)
    }