import asyncio
import httpx
import os

OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
}

ALLOWED_MODELS = [
    "deepseek/deepseek-chat-v3-0324:free",
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-4-maverick:free",
    "microsoft/mai-ds-r1:free",
    "meta-llama/llama-4-scout:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwq-32b:free",
    "qwen/qwen2.5-vl-72b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "google/gemini-2.5-pro-exp-03-25:free",
    "deepseek/deepseek-r1:free",
]

async def call_openrouter(model: str, prompt: str) -> str:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(OPENROUTER_BASE, headers=HEADERS, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

async def query_llm_agent(name: str, prompt: str, settings: dict) -> str:
    selected_model = settings.get("models", {}).get(name)

    if not selected_model:
        return f"[{name}] No model selected."

    # Auto-append ":free" if missing
    if not selected_model.endswith(":free"):
        selected_model += ":free"

    if selected_model not in ALLOWED_MODELS:
        return f"[{name}] Model '{selected_model}' is not supported."

    try:
        response = await call_openrouter(selected_model, prompt)
        return f"[{name}] {response}"
    except Exception as e:
        return f"[{name}] Error: {str(e)}"

async def query_all_llms(prompt: str, settings: dict) -> list:
    agents = ["LLM-A", "LLM-B", "LLM-C"]
    tasks = [query_llm_agent(agent, prompt, settings) for agent in agents]
    results = await asyncio.gather(*tasks)
    return results

def query_all_llms_sync(prompt: str, settings: dict) -> list:
    return asyncio.run(query_all_llms(prompt, settings))
