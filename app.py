from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils import extract_text_from_docx, ask_together_ai

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request_data: ChatRequest):
    user_message = request_data.message
    if not user_message:
        return JSONResponse(content={"error": "No message provided"}, status_code=400)

    try:
        with open("default.docx", "rb") as f:
            doc_text = extract_text_from_docx(f)

        prompt = f"{doc_text}\n\nUser: {user_message}\nAI:"
        response = ask_together_ai(prompt)
        return {"response": response}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
