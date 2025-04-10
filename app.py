from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI AI Chatbot. Use /chat to talk with the bot."}

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
        logging.info(f"AI response: {response}")

        return {"reply": response or "Sorry, I didn't get that."}

    except Exception as e:
        logging.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
