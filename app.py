from flask import Flask, render_template, request, jsonify
from llm.agents import query_all_llms_sync  # fixed: use the sync wrapper
from llm.aggregator import aggregate_responses
import os
import dotenv

# Load secrets from .env
dotenv.load_dotenv()

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("prompt", "")
    settings = data.get("settings", {})

    if not user_input:
        return jsonify({"error": "Empty prompt."}), 400

    try:
        # ✅ fixed: run the async LLM queries safely in sync context
        agent_outputs = query_all_llms_sync(user_input, settings)

        final_response = aggregate_responses(agent_outputs)

        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
