from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI application. Please use the /chat endpoint to interact."}

@app.post("/chat")
async def chat(request_data: ChatRequest):
    user_message = request_data.message
    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        with open("default.docx", "rb") as f:
            doc_text = extract_text_from_docx(f)

        prompt = f"{doc_text}\n\nUser: {user_message}\nAI:"
        response = ask_together_ai(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
