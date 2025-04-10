import os
import requests
from docx import Document
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def extract_text_from_docx(file) -> str:
    doc = Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text

def ask_together_ai(prompt: str) -> str:
    if not TOGETHER_API_KEY:
        raise ValueError("TOGETHER_API_KEY is not set in environment.")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-7b-instruct",  # You can switch to llama-2, qwen, etc.
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("API error:", response.status_code, response.text)
        return "Sorry, the AI couldn't respond right now."
