# Quick Start Guide (English)

Welcome to Matrix MCP v2.0. This guide will help you get the system up and running in less than 3 minutes.

## 1. Prerequisites
- Python 3.10 or higher
- Git

## 2. Installation

### Clone the Repository
```bash
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2
```

### Setup Virtual Environment
```bash
python -m venv .venv
```

**Activate:**
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Configuration

### Environment Variables
1. Copy the example file: `copy .env.example .env`
2. Open `.env` and enter your `OPENAI_API_KEY`.
3. (Optional) Set `OPENAI_BASE_URL` if using xAI Grok or DeepSeek.

### MCP Servers
The system comes with `user_data/servers/servers.example.json`. The UI will automatically detect this and allow you to connect to the official SSE test node.

## 4. Launching the Workspace

### Web Mode (Recommended)
Highly portable and stable.
```bash
python run_web_server.py
```
After launching, open your browser and navigate to the printed URL (default: `http://127.0.0.1:2027`).

### Desktop Mode
Windows Native experience.
```bash
python run_desktop_app.py
```
*Note: Requires WebView2 runtime installed on Windows.*

## 5. First Steps in the UI
1. Go to **Settings → AI Profiles** and ensure your API key and model are selected.
2. Go to **Settings → Servers**, select `servers.example` from the list, and click **Save & Restart**.
3. Start chatting! The AI will automatically use available MCP tools based on your persona.
