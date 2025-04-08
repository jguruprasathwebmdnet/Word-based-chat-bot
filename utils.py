from flask import Flask, request, jsonify
from utils import extract_text_from_docx, ask_together_ai

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Word Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        text = extract_text_from_docx(file)
        response = ask_together_ai(text)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
