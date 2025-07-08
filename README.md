# 🛠️ Prompt Fixer – Your Prompt Engineering Assistant

**Prompt Fixer** is an AI-powered assistant that helps you analyze, critique, and improve prompts for Large Language Models (LLMs) like Gemini and GPT.

Whether you're building chatbots, fine-tuning LLMs, or crafting killer content — Prompt Fixer helps you write *clearer, sharper, and more effective* prompts.

---

## 🚀 What It Does

🔍 **Analyze Your Prompt**  
- Detects flaws like vagueness, ambiguity, or lack of context.

🧠 **Get Smart Suggestions**  
- Explains problems and improves your prompt with a better version.

🎭 **Style Variants**  
- Generates two tone-specific versions (e.g., formal, casual, direct, creative).

📊 **Prompt Score**  
- Rates your prompt on a scale of 1–10 with justification.

💡 **Pro Tip**  
- Gives one helpful tip to level up your prompt writing game.

---

## 🎨 Live Demo

> 🔗 [COMING SOON on Hugging Face Spaces](https://huggingface.co/spaces/your-username/prompt-fixer)

---

## 🧱 Built With

- [Streamlit](https://streamlit.io) – clean interactive UI
- [Gemini API](https://ai.google.dev) – for LLM-based analysis
- `httpx` + `asyncio` – async HTTP calls
- Custom `style.css` – themed dark UI with clean layout

---

| Prompt Input + Analyze                                                                                                    | Flaw Detection + Scoring                                                                                                  | Prompt Variants + Tip                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| ![Screenshot 1](https://github.com/Vaish-d30/Prompt-Fixer/blob/1d32c4eb7900f0519ee907112fd0127400c5e34c/ss1.png?raw=true) | ![Screenshot 2](https://github.com/Vaish-d30/Prompt-Fixer/blob/1d32c4eb7900f0519ee907112fd0127400c5e34c/ss2.png?raw=true) | ![Screenshot 3](https://github.com/Vaish-d30/Prompt-Fixer/blob/1d32c4eb7900f0519ee907112fd0127400c5e34c/ss3.png?raw=true) |

---

## 🧑‍💻 How to Run Locally

```bash
git clone https://github.com/yourusername/prompt-fixer.git
cd prompt-fixer
pip install -r requirements.txt
streamlit run app.py
