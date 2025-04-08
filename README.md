# Word File AI Chatbot 🤖📄

A Flask-based API that takes `.docx` files as input, extracts the text, and sends it to Together AI (LLM) for a response.

## Endpoints

- `GET /` — Health check
- `POST /chat` — Accepts `.docx` file, returns chatbot response

## Example Usage (curl)

```bash
curl -X POST https://your-render-url/chat \
  -F "file=@yourfile.docx"
