from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai
import os

app = FastAPI()

# Mount static directory to serve HTML and other frontend assets
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

# Serve the chatbot HTML on the root route
@app.get("/")
async def serve_chat_page():
    return FileResponse(os.path.join("static", "chat.html"))

# Chat endpoint
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
        return {"reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
