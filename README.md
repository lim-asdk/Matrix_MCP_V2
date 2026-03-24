# Matrix MCP v2.0

> [!NOTE]
> **Official Promotional Homepage**: [https://lim-asdk.github.io/Matrix_MCP_V2/](https://lim-asdk.github.io/Matrix_MCP_V2/)  
> **Technical Documentation (README)**: This guide focuses on installation, configuration, and architecture.

English | [한국어](./README.ko-KR.md)

[![Status](https://img.shields.io/badge/Status-Public--Beta-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/License-PolyForm--Noncommercial-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)
[![MCP](https://img.shields.io/badge/MCP-Native-blueviolet?style=for-the-badge)](https://modelcontextprotocol.io)

**Professional MCP Operation Workspace.**  
A specialized environment for connecting, testing, and managing Model Context Protocol (MCP) servers and AI profiles across Web and Desktop environments.

---

## 📖 Project Overview

Matrix MCP is a specialized workspace focused on the **operational** aspects of the Model Context Protocol. Unlike standard chat clients, it provides a structured environment for managing the full lifecycle of MCP connections and AI tool-calling workflows.

### Key Capabilities
- **Native MCP Support**: Direct integration with **stdio** and **SSE** transport layers for real-time tool execution.
- **Provider Agnostic**: Seamlessly bridge any OpenAI-compatible API (Grok, OpenAI, DeepSeek, Google Gemini) to your MCP tools.
- **Hybrid Runtime**: Optimized for both **Web-first** browser interaction and **Windows Desktop** native stability (WebView2).
- **Operator Inspector**: Real-time monitoring of raw tool requests, responses, and AI reasoning chains for debugging and optimization.

---

## 🚀 Quick Start

### 1. Installation
Ensure you have Python 3.10+ installed on your system.

```bash
# Clone the repository
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2

# Create a virtual environment
python -m venv .venv
```

**Activate Environment:**
- **Windows (PowerShell/CMD)**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Copy the template environment file and provide your AI API credentials.

```bash
# Copy template
copy .env.example .env

# Edit .env and provide your settings:
# OPENAI_API_KEY=your_key_here
# OPENAI_BASE_URL=https://api.x.ai/v1 (or preferred provider)
```

### 3. Execution
Run the workspace in your preferred mode.

- **Web Mode** (Primary): `python run_web_server.py`
- **Desktop Mode** (Windows Native): `python run_desktop_app.py`

---

## ⚙️ Run Modes

| Mode | Entry Point | Target Platform | Description |
| :--- | :--- | :--- | :--- |
| **Web-First** | `run_web_server.py` | Universal / Browser | **Recommended**. Runs as a local server accessible via any modern browser. Supports the latest web features. |
| **Desktop** | `run_desktop_app.py` | Windows Native | Wrapper utilizing **WebView2**. Provides a dedicated window experience and desktop lifecycle management. |

---

## 🏛️ Architecture Overview (L1-L5)

The project follows a layered modular architecture optimized for separation of concerns and protocol flexibility.

| Layer | Responsibility | Description |
| :--- | :--- | :--- |
| **L5 (Presentation)** | UI/UX | Frontend logic and assets located in `lim_arsenal/engine/L5_Presentation`. |
| **L4 (Bridge)** | API Gateway | Protocol transformation and communication bridge (`bridge_api.py`). |
| **L3 (Protocol)** | MCP Logic | Core Model Context Protocol handling and server management. |
| **L2 (Engine)** | Core Logic | Backend services and system management modules. |
| **L1 (Infrastructure)** | Runtime/OS | Python environment, file system persistence, and OS-level interactions. |

---

## 🔗 Official Test Node

Validate your setup with our public SSE test endpoint:
- **SSE URL**: `http://35.202.58.51:8766/sse`
- **Source**: [Open World News MCP](https://github.com/lim-asdk/open-world-news-mcp)

---

## 🏗️ Directory Structure
- `lim_arsenal/engine/`: Core backend and frontend assets.
- `installer_output/`: Build artifacts and setup executables.
- `config/`: Application and user configuration files.
- `docs/`: Technical documentation and planning resources.

---

## 🏛️ Project Identity
Matrix MCP is a project by **Lim Arsenal (lim-asdk)**.  
Licensed under **PolyForm Noncommercial License 1.0**.

© 2026 Lim Arsenal. All rights reserved.
