# Matrix MCP v2.0

> **Public Beta**  
> AI-powered desktop and web workspace for **Model Context Protocol (MCP)**.  
> Connect MCP servers, manage AI profiles, use personas, and run tools in **browser or desktop mode**.

---

## What it does

- Connects to MCP servers over **stdio** and **SSE**
- Supports multiple AI provider profiles through OpenAI-compatible APIs
- Includes a persona-based prompt system
- Provides both **Web** and **Desktop** runtime modes
- Shows MCP tool calls and results in a unified workspace UI

---

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
```
> Fill in your API key in `.env`.

### 4. Run

**Web mode:**
```bash
python run_web_server.py
```

**Desktop mode:**
```bash
python run_desktop_app.py
```

> **Note**: Recommended to start with Web mode first.

---

## Run Modes

| Mode | Command | Notes |
|---|---|---|
| Web | `python run_web_server.py` | Best for first run, easy to reproduce across environments |
| Desktop | `python run_desktop_app.py` | Native Windows experience, requires WebView2 |

> Recommended: verify Web mode first in a new environment.

---

## 🔗 Connecting MCP Servers

Add MCP servers under **Settings → Servers** in the UI.

- **stdio**: Run local Python/Node scripts (`python your_server.py`)
- **SSE**: Remote server URL (`http://host/sse`)

Refer to `user_data/servers/servers.example.json` for structure examples.

---

## 🛡️ Security Principles

- **API Keys**: Never hardcode keys. Always use the `.env` file.
- **Local Privacy**: `user_data/` is ignored by `.gitignore` to keep your history and profiles private.
- **Pure Code**: Real server URLs and personal chat histories are purged from the public repo.

---

## 📄 License

This project is distributed under the **PolyForm Noncommercial License 1.0**.

- ✅ Personal, Research, Educational, and Non-commercial use permitted.
- ❌ Commercial use requires a separate license.

Commercial inquiries: Lim Arsenal (lim-asdk) / rfcon0@gmail.com

---

# Matrix MCP v2.0 (한국어)

> **Public Beta**  
> **Model Context Protocol (MCP)**를 위한 AI 지원 데스크톱 및 웹 작업 공간입니다.  
> MCP 서버를 연결하고, AI 프로필 및 페르소나를 관리하며, **브라우저 또는 데스크톱 모드**에서 도구를 실행하세요.

---

## 주요 기능

- **stdio** 및 **SSE**를 통한 MCP 서버 연결
- OpenAI 호환 API를 통한 다중 AI 제공업체 프로필 지원
- 페르소나 기반 프롬프트 시스템 포함
- **웹** 및 **데스크톱** 실행 모드 모두 제공
- 통합 워크스페이스 UI에서 MCP 도구 호출 및 결과 확인

---

## 빠른 시작

### 1. 가상 환경 생성

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 설정

```bash
copy .env.example .env
```
> `.env` 파일에 API 키를 입력하세요.

### 4. 실행

**웹 모드:**
```bash
python run_web_server.py
```

**데스크톱 모드:**
```bash
python run_desktop_app.py
```

> **참고**: 웹 모드를 먼저 확인하는 것을 권장합니다.

---

## 실행 모드

| 모드 | 명령어 | 특징 |
|---|---|---|
| 웹 | `python run_web_server.py` | 첫 실행 시 권장, 환경 간 재현 용이 |
| 데스크톱 | `python run_desktop_app.py` | 윈도우 네티브 환경, WebView2 필요 |

---

## 🗺️ Roadmap

- [ ] PyPI Package Distribution
- [ ] IQ-Pack Marketplace
- [ ] Multi-Agent Orchestration
- [ ] Cloud Synchronization

---

## 🏛️ Project Identity

**Matrix MCP** is a project by **Lim Arsenal**, dedicated to bridging the gap between Large Language Models and real-world tools through the Model Context Protocol.

- **Founder & Lead Developer**: [Lim Hwa Chan](https://github.com/lim-asdk)
- **Organization**: [Lim Arsenal](https://github.com/lim-asdk)
- **Status**: Public Beta (v2.0.0)

*"Building the next generation of AI workspaces, one protocol at a time."*

---

© 2026 Lim Arsenal. All rights reserved.
