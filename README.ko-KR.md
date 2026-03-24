# Matrix MCP v2.0

> [!NOTE]
> **제품 소개 및 가치 제안**: [공식 홈페이지](https://lim-asdk.github.io/Matrix_MCP_V2/)를 방문해 주세요.  
> **기술 문서 및 개발 가이드**: 현재 읽고 계신 파일은 `README.ko-KR.md` 기술 문서입니다.

[English](./README.md) | 한국어

[![Status](https://img.shields.io/badge/Status-Public--Beta-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/라이선스-PolyForm--비상업용-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)

**전문적인 MCP 운영 워크스페이스.**  
Model Context Protocol(MCP) 서버와 AI 프로필을 연결, 테스트 및 관리하기 위한 전문 환경입니다.

---

## 📖 기술 개요 (Technical Overview)

Matrix MCP는 Model Context Protocol의 **운영(Operational)** 측면에 집중한 특화 워크스페이스입니다. 일반적인 챗봇 클라이언트가 단순히 채팅에 치중하는 것과 달리, Matrix MCP는 MCP 연결의 생애주기 관리와 AI 도구 호출(Tool-calling) 워크플로우를 위한 구조화된 환경을 제공합니다.

### 핵심 역량
- **기본 MCP 지원**: **stdio** 및 **SSE** 전송 계층과의 직접적인 통합.
- **제공자 중립성**: Grok, OpenAI, DeepSeek, Google Gemini 등 모든 OpenAI 호환 API를 도구 실행과 매끄럽게 연결합니다.
- **하이브리드 런타임**: 빠른 브라우저 기반 상호작용(Web-first)과 안정적인 Windows 데스크톱 실행 환경에 최적화되었습니다.
- **운영자용 검사기(Inspector)**: 원본 도구 요청/응답 데이터와 AI의 추론 체인을 실시간으로 모니터링할 수 있습니다.

---

## 🚀 빠른 시작 (Quick Start)

### 1. 설치 (Installation)
```bash
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2
python -m venv .venv
```

**가상환경 활성화 (Activate Environment):**
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. 환경 설정 (Configuration)
```bash
# 예시 환경 파일 복사
copy .env.example .env
# .env 파일을 열어 API Key (OPENAI_API_KEY 등)를 입력하세요.
```

### 3. 실행 (Execution)
- **웹 모드 (Web Mode)**: `python run_web_server.py`
- **데스크톱 모드 (Desktop Mode)**: `python run_desktop_app.py`

---

## ⚙️ 실행 모드 (Run Modes)

| 모드 | 명령문 | 플랫폼 | 설명 |
| :--- | :--- | :--- | :--- |
| **Web (기본)** | `python run_web_server.py` | 공통 | 권장 모드. 로컬 웹 서버로 앱을 띄워 브라우저로 접속합니다. |
| **Desktop** | `python run_desktop_app.py` | Windows | WebView2 기반의 단독 창으로 실행하며 데스크톱 앱과 같은 사용성을 제공합니다. |

---

## 🔗 공식 테스트 노드 (Official Test Node)

Matrix MCP는 즉시 사용 가능한 SSE 테스트 노드를 기본적으로 포함하고 있습니다.
- **SSE URL**: `http://35.202.58.51:8766/sse`
- **소스**: [Open World News MCP](https://github.com/lim-asdk/open-world-news-mcp)

---

## 🏛️ 프로젝트 정체성
Matrix MCP는 **Lim Arsenal (lim-asdk)**의 프로젝트입니다.  
**PolyForm Noncommercial License 1.0** 라이선스를 따릅니다.

© 2026 Lim Arsenal. All rights reserved.
