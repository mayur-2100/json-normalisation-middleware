from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def normalise(data):
    if isinstance(data, list):
        return data[0] if data else {}
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"raw": data}
    elif data is None:
        return {}
    elif isinstance(data, dict):
        return data
    else:
        return {"value": data}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "json-normalisation-middleware"}), 200

@app.route('/normalise', methods=['POST'])
def normalise_payload():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    if "data" not in body:
        return jsonify({"error": "Missing required field: data"}), 422

    raw = body["data"]
    result = normalise(raw)

    return jsonify({
        "status":          "ok",
        "input_type":      type(raw).__name__,
        "normalised":      result
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)