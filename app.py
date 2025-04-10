from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai

app = FastAPI()
route = 

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI application. Please use the /chat endpoint to interact."}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a .docx file and extract its text.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .docx file.")
    try:
        document_text = extract_text_from_docx(file.file)
        return {"document_text": document_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/chat/")
async def chat(question: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to ask a question based on the uploaded .docx document.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .docx file.")
    try:
        document_text = extract_text_from_docx(file.file)
        answer = ask_together_ai(document_text, question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
