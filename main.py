from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY. Add it to your .env file before starting the app.")

genai.configure(api_key=api_key)

ask_model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    system_instruction="Act like a helpful personal assistant",
)

summary_model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    system_instruction="Act like an expert email assistant",
)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")

    if not question:
        return jsonify({"response": "Please provide a question."}), 400

    response = ask_model.generate_content(
        question,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 512,
        },
    )

    answer = response.text.strip()
    return jsonify({"response": answer}), 200


@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email")

    if not email_text:
        return jsonify({"response": "Please provide email text to summarize."}), 400

    prompt = f"Summarize the following email in 2-3 sentences: {email_text}"
    response = summary_model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 512,
        },
    )

    summary = response.text.strip()
    return jsonify({"response": summary}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
