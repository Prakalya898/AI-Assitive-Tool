# 🤖 AI Assistive Tool

A Streamlit app to help blind and autistic users understand image content using AI, translation, and speech.

Live Demo

You can access the live application at: [(https://assistool.streamlit.app/)](https://assistool.streamlit.app/)
---

## 🚀 Features

```text
📸 Upload Image
💬 Ask a query
🧠 Extract Caption (via Gemini)
🌐 Translate to Tamil (free API)
🔊 Audio Output (via gTTS)
🎞️ Lottie Animations
🦾 Fallback Text Option
```

---

## 📦 Setup

```bash
git clone https://github.com/yourusername/ai-assistive-tool.git
cd ai-assistive-tool

python -m venv .venv
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔑 API Key

```python
# In agent.py
os.environ["GOOGLE_API_KEY"] = "your_google_gemini_api_key"
```

---

## ▶️ Run the App

```bash
streamlit run agent.py
```

---

## 📁 Project Structure

```text
.
├── app.py                 # Streamlit App
├── tool.py                # Gemini Tool
├── ttstool.py             # Translator & TTS
├── output/                # Stores audio files
├── animations/            # Lottie files
│   ├── assistive_ai.json
│   ├── loading.json
│   └── audio_loading.json
├── requirements.txt
└── README.md
```

## 🛠 Dependencies

```text
streamlit
langchain
langchain-google-genai
gtts
deep-translator
streamlit-lottie
```

---
