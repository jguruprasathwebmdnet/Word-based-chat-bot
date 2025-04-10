import os
import requests
from docx import Document
from typing import BinaryIO

def extract_text_from_docx(file: BinaryIO) -> str:
    """
    Extracts text from a .docx Word document provided as a file-like object.

    Args:
        file (BinaryIO): A file-like object representing the .docx document.

    Returns:
        str: The extracted text from the document.
    """
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)

def ask_together_ai(document_text: str, question: str) -> str:
    """
    Sends the extracted document text and user question to Together AI
    and returns the model's answer.

    Args:
        document_text (str): The text extracted from the document.
        question (str): The user's question.

    Returns:
        str: The AI-generated answer.

    Raises:
        ValueError: If the TOGETHER_API_KEY environment variable is missing
                    or if the document text is empty.
        RuntimeError: If the Together AI API returns an error response.
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
