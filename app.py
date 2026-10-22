
import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=message
        )

        return jsonify({"reply": interaction.output_text})

    except Exception as error:
        app.logger.exception("Gemini interaction failed")
        return jsonify({
            "error": f"Gemini error: {str(error)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
