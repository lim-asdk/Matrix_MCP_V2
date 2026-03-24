# Matrix MCP v2.0

English | [한국어](./README.ko-KR.md)

[![Status](https://img.shields.io/badge/Status-Public--Beta-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/License-PolyForm--Noncommercial-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)
[![MCP](https://img.shields.io/badge/MCP-Native-blueviolet?style=for-the-badge)](https://modelcontextprotocol.io)

**Professional MCP Operation Workspace.**  
A specialized environment for connecting, testing, and managing Model Context Protocol (MCP) servers and AI profiles.

---

[**🚀 Launch Product Homepage**](https://lim-asdk.github.io/Matrix_MCP_V2/) | [**💾 Download Latest Release**](https://github.com/lim-asdk/Matrix_MCP_V2/releases/latest)

---

## 📖 Technical Overview

Matrix MCP is a specialized workspace focused on the **operational** aspects of the Model Context Protocol. While many clients focus on simple chat, Matrix MCP provides a structured environment for managing the lifecycle of MCP connections and AI tool-calling workflows.

### Core Capabilities
- **Native MCP Support**: Direct integration with **stdio** and **SSE** transport layers.
- **Provider Agnostic**: Seamlessly bridge any OpenAI-compatible API (Grok, OpenAI, DeepSeek, Google Gemini) for tool execution.
- **Dual Runtime**: Optimized for both **Web-first** browser interaction and **Windows Desktop** stability.
- **Operator Inspector**: Real-time monitoring of raw tool requests, responses, and AI reasoning chains.

---

---

## ⚡ Quick Start

### 1. Installation
```bash
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2
python -m venv .venv
```

**Activate Environment:**
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Configuration
```bash
copy .env.example .env
# Open .env and add your OPENAI_API_KEY
```

### 3. Run
- **Web Mode**: `python run_web_server.py` (Recommended)
- **Desktop Mode**: `python run_desktop_app.py` (Windows Only)

---

## ⚙️ Run Modes

| Mode | Command | Platform |
|:---:|---|---|
| **Web** | `python run_web_server.py` | Browser-based, Universal |
| **Desktop** | `python run_desktop_app.py` | Windows Native (WebView2) |

---

## 🔗 Official Test Node

Matrix MCP comes with a pre-configured SSE test node:
- **SSE URL**: `http://35.202.58.51:8766/sse`
- **Source**: [Open World News MCP](https://github.com/lim-asdk/open-world-news-mcp)

---

## 📄 Further Reading
- [Detailed Quick Start](./docs/en/QUICK_START.md)
- [Architecture Overview](./docs/en/ARCHITECTURE.md)
- [Release Notes](./docs/en/RELEASE_NOTES_v2.0.0-beta1.md)

---

## 🏛️ Project Identity
Matrix MCP is a project by **Lim Arsenal (lim-asdk)**.  
Licensed under **PolyForm Noncommercial License 1.0**.

© 2026 Lim Arsenal. All rights reserved.
