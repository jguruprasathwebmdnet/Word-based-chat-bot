import os
import requests
from docx import Document

# 📄 Path to your pre-uploaded Word file
DOC_PATH = "sample_doc.docx"  # Make sure this file is in your root or correct location

def extract_text_from_docx(file_path):
    """Extracts text from a .docx Word document."""
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)

# 🧠 Load the document once globally for reuse
try:
    document_text = extract_text_from_docx(DOC_PATH)
except Exception as e:
    document_text = ""
    print(f"❌ Failed to load document '{DOC_PATH}': {e}")

def ask_together_ai(question):
    """
    Sends the extracted document and user question to Together AI
    and returns the model's answer.
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable is missing.")

    if not document_text:
        raise ValueError("Document text is empty or failed to load.")

    prompt = f"""You are an expert assistant. Answer the question using the document below.

Document:
\"\"\"
{document_text}
\"\"\"

Question: {question}
Answer:"""

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Together API error: {response.status_code} - {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
