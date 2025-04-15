# 🧠 Socrates-II

**Socrates-II** (aka **S2**) is a Discord bot inspired by the legendary Greek philosopher, Socrates. It’s an AI-powered bot that can ponder, ask philosophical questions, invent new words, and drop thought-provoking quotes — all while chatting intelligently in natural language.


---

## 📌 Features

- 🤖 **Conversational AI** – Responds intelligently using GPT (OpenAI)
- 🧠 **Philosophical Questions** – Generates and refines deep questions using Markov chains and GPT
- 💬 **Socratic Thoughts** – Shares random Socrates-inspired musings
- 🔤 **Word Creation** – Invents unique words and definitions
- 📚 **Simple Explanations** – Breaks down complex ideas for young audiences
- 🔒 **Secure Secrets** – Uses environment variables for API keys

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/abhi-srivathsa/Socrates-II.git
cd Socrates-II
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Add Environment Variables
Create a .env file in the root directory with the following contents:
```bash
TOKEN=your_discord_bot_token
openai.api_key=your_openai_api_key
```

🔑 You can get a Discord bot token from Discord Developer Portal and an OpenAI key from OpenAI.

### ▶️ Running the Bot
python src/main.py

Make sure your bot has access to a text channel named:
conversation-with-socrates

### 🧪 Sample Commands

| Command      | Description                           |
|--------------|---------------------------------------|
| `hi` / `hello` | Friendly philosophical welcome          |
| `question`     | Asks a philosophical question       |
| `thought`      | Shares a Socratic thought           |
| `new word`      | Creates a unique, made-up word and its meaning           |
| `Any other message`      | GPT-powered philosophical-style response           |


### 🔮 TODO
	•	Refactor into separate modules (bot.py, utils.py, gpt.py)
	•	Upgrade to gpt-4 using ChatCompletion
	•	Use data from all philosophical writings available


⸻

