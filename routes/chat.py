from flask import Blueprint, request, jsonify
from llm.agents import query_all_llms_sync
from llm.aggregator import aggregate_responses

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("prompt", "")
    settings = data.get("settings", {})

    if not user_input:
        return jsonify({"error": "Empty prompt."}), 400

    try:
        agent_outputs = query_all_llms_sync(user_input, settings)
        final_response = aggregate_responses(agent_outputs)
        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
