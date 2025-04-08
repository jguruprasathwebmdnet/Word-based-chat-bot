from flask import Flask, request, jsonify, render_template
from utils import extract_text_from_docx, ask_together_ai

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        with open("default.docx", "rb") as f:
            doc_text = extract_text_from_docx(f)

        # Combine doc text + user message as a prompt
        prompt = f"{doc_text}\n\nUser: {user_message}\nAI:"
        response = ask_together_ai(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
