// === Global Model List ===
const MODEL_LIST = [
  { id: "deepseek/deepseek-chat-v3-0324:free", name: "DeepSeek Chat v3" },
  { id: "google/gemini-2.0-flash-exp:free", name: "Gemini 2.0 Flash" },
  { id: "meta-llama/llama-4-maverick:free", name: "LLaMA 4 Maverick" },
  { id: "microsoft/mai-ds-r1:free", name: "MAI DS R1" },
  { id: "meta-llama/llama-4-scout:free", name: "LLaMA 4 Scout" },
  { id: "google/gemma-3-27b-it:free", name: "Gemma 3 27B" },
  { id: "qwen/qwq-32b:free", name: "Qwen QWQ 32B" },
  { id: "qwen/qwen2.5-vl-72b-instruct:free", name: "Qwen2.5 VL 72B" },
  { id: "qwen/qwen-2.5-72b-instruct:free", name: "Qwen 2.5 72B" },
  { id: "google/gemini-2.5-pro-exp-03-25:free", name: "Gemini 2.5 Pro" },
  { id: "deepseek/deepseek-r1:free", name: "DeepSeek R1" },
];

function populateDropdown(dropdownId) {
  const select = document.getElementById(dropdownId);
  select.innerHTML = "";
  MODEL_LIST.forEach((model) => {
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = model.name;
    select.appendChild(option);
  });
}

// === Theme Toggle ===
const themeToggle = document.getElementById("themeToggle");
const toggleConfig = document.getElementById("toggleConfig");
const configPanel = document.getElementById("configPanel");
const html = document.documentElement;

function setInitialTheme() {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    html.classList.add("dark");
  } else if (savedTheme === "light") {
    html.classList.remove("dark");
  } else {
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;
    if (prefersDark) html.classList.add("dark");
    else html.classList.remove("dark");
  }
}

setInitialTheme();

themeToggle.addEventListener("click", () => {
  const isDark = html.classList.toggle("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
});

toggleConfig.addEventListener("click", () => {
  configPanel.classList.toggle("hidden");
});

// === Chat Handling ===
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatContainer = document.getElementById("chatContainer");
const modelA = document.getElementById("modelA");
const modelB = document.getElementById("modelB");
const modelC = document.getElementById("modelC");

populateDropdown("modelA");
populateDropdown("modelB");
populateDropdown("modelC");

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `p-3 rounded shadow max-w-2xl ${role === "user" ? "bg-blue text-fg0 self-end" : "bg-green text-fg0 self-start"}`;
  div.innerText = text;
  chatContainer.appendChild(div);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = userInput.value.trim();
  if (!prompt) return;

  appendMessage("user", prompt);
  userInput.value = "";

  appendMessage("bot", "Thinking...");

  const settings = {
    models: {
      "LLM-A": modelA.value,
      "LLM-B": modelB.value,
      "LLM-C": modelC.value,
    },
  };

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, settings }),
  });

  chatContainer.lastChild.remove(); // remove 'Thinking...'

  if (response.ok) {
    const data = await response.json();
    appendMessage("bot", data.response);
  } else {
    appendMessage(
      "bot",
      "An error occurred. Please check your model selections.",
    );
  }
});
