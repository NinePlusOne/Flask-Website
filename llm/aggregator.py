def aggregate_responses(responses: list) -> str:
    if not responses:
        return "No responses received."

    # Sanitize: only join valid strings
    safe_responses = [r if isinstance(r, str) else str(r) for r in responses]

    combined = "\n".join(safe_responses)

    return f"Final synthesized response based on multiple agents:\n{combined}"
