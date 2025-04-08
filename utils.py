import os
import requests
from docx import Document

# 📄 Load your Word file once when the app starts
DOC_PATH = "sample_doc.docx"  # Make sure this file is in your project root

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)

# 🧠 Loaded globally and reused across requests
document_text = extract_text_from_docx(DOC_PATH)

# 🧠 Ask Together AI using the document content as context
def ask_together_ai(question):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable is missing.")

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
