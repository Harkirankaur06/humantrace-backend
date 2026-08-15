from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from models.predict import HumanTracePredictor


app = Flask(__name__)

CORS(app)


# Load the trained model once when the server starts.
predictor = None

def get_predictor():
    global predictor

    if predictor is None:
        predictor = HumanTracePredictor()

    return predictor


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "HumanTrace API is running",
        "status": "ok"
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required."
            }), 400

        text = data.get("text")

        if not isinstance(text, str):
            return jsonify({
                "error": "Text must be a string."
            }), 400

        if not text.strip():
            return jsonify({
                "error": "Text cannot be empty."
            }), 400

        result = get_predictor().predict(text)

        return jsonify(result), 200

    except Exception as exc:

        return jsonify({
            "error": str(exc)
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )