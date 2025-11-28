from flask import Flask, request, jsonify
from utils.scraper import extract_text_from_url
from utils.solver import solve_questions
import os

app = Flask(__name__)

# Secret verification
SERVER_SECRET = os.getenv("SERVER_SECRET", "tdsproject-secret")


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "tds-llm API running"
    }), 200


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "JSON body missing"}), 400

    email = data.get("email")
    secret = data.get("secret")
    url = data.get("url")

    # SECRET CHECK
    if secret != SERVER_SECRET:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    # 1) SCRAPE THE URL
    scraped_text = extract_text_from_url(url)

    if not scraped_text or scraped_text.startswith("[Error"):
        return jsonify({
            "status": "error",
            "message": "Failed to extract text",
            "details": scraped_text
        }), 500

    # 2) SOLVE / GENERATE ANSWERS
    results = solve_questions(scraped_text)

    return jsonify({
        "status": "ok",
        "message": "Answers generated",
        "results": results
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
