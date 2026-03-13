# 🤖 Nexus AI — AI Coding Assistant Web App

A sleek, full-stack AI-powered coding assistant built with **React + Vite** on the frontend and **FastAPI + Google Gemini** on the backend. Ask it to write code, debug errors, explain architectures, or help with any programming task.

---

## 📸 Features

- ✨ **Modern Dark UI** — Premium glassmorphic design with smooth animations and micro-interactions
- 💬 **Real-time Chat** — Conversational interface with typing indicators and auto-scroll
- 🧠 **Powered by Gemini 2.5 Flash** — Fast, intelligent responses via Google's latest AI model
- 📝 **Markdown & Syntax Highlighting** — AI responses rendered with full Markdown support including code blocks
- 📋 **One-Click Code Copy** — Copy code snippets directly from the chat
- 📱 **Responsive Layout** — Collapsible sidebar, works on desktop and tablets
- ⚡ **Quick Suggestions** — Pre-built prompt cards to get started instantly

---

## 🗂️ Project Structure

```
AI coding Assistant web app/
├── .env                    # Environment variables (API keys)
├── venv/                   # Python virtual environment (Python 3.11)
│
├── backend/
│   ├── main.py             # FastAPI server with CORS and /api/chat endpoint
│   ├── agent.py            # Gemini AI agent logic and system prompt
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── index.html          # HTML entry point
    ├── package.json        # Node.js dependencies and scripts
    ├── vite.config.js      # Vite configuration
    └── src/
        ├── main.jsx        # React entry point
        ├── App.jsx         # Main application component (Chat UI)
        ├── App.css         # Component-level styles
        └── index.css       # Global design system and theme
```

---

## 🛠️ Tech Stack

| Layer      | Technology                                                   |
|------------|--------------------------------------------------------------|
| Frontend   | React 19, Vite 8, Lucide React (icons), React Markdown      |
| Backend    | FastAPI, Uvicorn, Pydantic                                   |
| AI Model   | Google Gemini 2.5 Flash (via `google-genai` SDK)             |
| Styling    | Vanilla CSS with CSS custom properties, glassmorphism        |
| Language   | Python 3.11, JavaScript (ES Modules)                         |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11** installed ([Download](https://www.python.org/downloads/))
- **Node.js 18+** installed ([Download](https://nodejs.org/))
- A **Google Gemini API Key** ([Get one here](https://aistudio.google.com/apikey))

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "AI coding Assistant web app"
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Set Up the Backend

```bash
# Create and activate virtual environment
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install Python dependencies
pip install -r backend/requirements.txt
```

### 4. Set Up the Frontend

```bash
cd frontend
npm install
```

### 5. Run the Application

Open **two terminals**:

**Terminal 1 — Backend (FastAPI):**
```bash
cd backend
python main.py
```
> Backend runs at: `http://localhost:8000`

**Terminal 2 — Frontend (Vite + React):**
```bash
cd frontend
npm run dev
```
> Frontend runs at: `http://localhost:5173`

Open your browser and navigate to **[http://localhost:5173](http://localhost:5173)** 🎉

---

## 🔌 API Reference

### `POST /api/chat`

Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "Write a Python function to reverse a string"
}
```

**Response:**
```json
{
  "response": "Here's a Python function to reverse a string:\n\n```python\ndef reverse_string(s):\n    return s[::-1]\n```",
  "error": null
}
```

---

## ⚙️ Configuration

| Variable         | Description                          | Required |
|------------------|--------------------------------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key           | ✅ Yes   |

The AI model and system prompt can be customized in `backend/agent.py`.

---

## 📦 Python Dependencies

| Package          | Version   | Purpose                            |
|------------------|-----------|------------------------------------|
| `fastapi`        | 0.110.0   | Web framework for the REST API     |
| `uvicorn`        | 0.28.0    | ASGI server to run FastAPI         |
| `pydantic`       | 2.6.4     | Data validation and serialization  |
| `python-dotenv`  | 1.0.1     | Load environment variables         |
| `google-genai`   | 1.2.0     | Google Gemini AI SDK               |

---

## 🧩 Frontend Dependencies

| Package          | Purpose                              |
|------------------|--------------------------------------|
| `react`          | UI component library                 |
| `react-dom`      | React DOM rendering                  |
| `react-markdown` | Render Markdown in AI responses      |
| `axios`          | HTTP client (available if needed)    |
| `lucide-react`   | Modern icon library                  |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Google Gemini](https://ai.google.dev/) — AI model powering the assistant
- [FastAPI](https://fastapi.tiangolo.com/) — High-performance Python web framework
- [Vite](https://vitejs.dev/) — Next-generation frontend tooling
- [Lucide Icons](https://lucide.dev/) — Beautiful open-source icons
