from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request_data: ChatRequest):
    user_message = request_data.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        with open("default.docx", "rb") as f:
            doc_text = extract_text_from_docx(f)

        prompt = f"{doc_text.strip()}\n\nUser: {user_message}\nAI:"
        logging.info(f"Prompt: {prompt}")

        response = ask_together_ai(prompt)
        return {"reply": response or "Sorry, I didn't get that."}

    except Exception as e:
        logging.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
