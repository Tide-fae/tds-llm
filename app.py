from flask import Flask, request, jsonify
from utils.scraper import scrape_url
from utils.solver import solve_questions
import os

app = Flask(__name__)

# This is the secret you verify for basic protection
SERVER_SECRET = os.getenv("SERVER_SECRET", "abcd1234")


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "tds-llm API running"}), 200


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()

    # Validate request
    if not data:
        return jsonify({"status": "error", "message": "JSON body missing"}), 400

    email = data.get("email")
    secret = data.get("secret")
    url = data.get("url")

    if secret != SERVER_SECRET:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    # 1) SCRAPE IT
    scraped_text = scrape_url(url)

    if scraped_text is None:
        return jsonify({"status": "error", "message": "Could not scrape URL"}), 500

    # 2) SOLVE IT
    result = solve_questions(scraped_text)

    return jsonify({
        "status": "ok",
        "message": "Answers generated",
        "results": result
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
