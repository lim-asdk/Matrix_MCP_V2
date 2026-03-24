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

## 📖 프로젝트 개요 (Project Overview)

Matrix MCP는 Model Context Protocol의 **운영(Operational)** 측면에 집중한 특화 워크스페이스입니다. 일반적인 챗봇 클라이언트가 단순히 채팅에 치중하는 것과 달리, Matrix MCP는 MCP 연결의 생애주기 관리와 AI 도구 호출(Tool-calling) 워크플로우를 위한 구조화된 환경을 제공합니다.

### 핵심 역량
- **기본 MCP 지원**: **stdio** 및 **SSE** 전송 계층과의 직접적인 통합.
- **제공자 중립성**: Grok, OpenAI, DeepSeek, Google Gemini 등 모든 OpenAI 호환 API를 도구 실행과 매끄럽게 연결합니다.
- **하이브리드 런타임**: 빠른 브라우저 기반 상호작용(Web-first)과 안정적인 Windows 데스크톱 실행 환경에 최적화되었습니다.
- **운영자용 검사기(Inspector)**: 원본 도구 요청/응답 데이터와 AI의 추론 체인을 실시간으로 모니터링할 수 있습니다.

---

## 🚀 빠른 시작 (Quick Start)

### 1. 설치 (Installation)
Python 3.10 이상의 버전이 설치되어 있어야 합니다.

```bash
# 저장소 복제 (Clone)
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2

# 가상환경 생성 (Virtual Environment)
python -m venv .venv
```

**가상환경 활성화 (Activate Environment):**
- **Windows (PowerShell/CMD)**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 설정 (Configuration)
예시 환경 파일을 복사하고 사용자 API 인증 정보를 입력하세요.

```bash
# 템플릿 복사
copy .env.example .env

# .env 파일을 열어 설정값 입력:
# OPENAI_API_KEY=사용자_키_입력
# OPENAI_BASE_URL=https://api.x.ai/v1 (또는 원하는 제공자 URL)
```

### 3. 실행 (Execution)
원하는 모드에 맞춰 프로젝트를 시작하세요.

- **웹 모드 (Web Mode)**: `python run_web_server.py`
- **데스크톱 모드 (Desktop Mode)**: `python run_desktop_app.py`

---

## ⚙️ 실행 모드 (Run Modes)

| 모드 | 진입점 | 플랫폼 | 설명 |
| :--- | :--- | :--- | :--- |
| **Web-First** | `run_web_server.py` | 공통 / 브라우저 | **권장 모드**. 로컬 서버로 앱을 띄워 브라우저로 접속합니다. 최신 웹 기술이 즉시 반영됩니다. |
| **Desktop** | `run_desktop_app.py` | Windows | **WebView2** 기반의 전용 창으로 실행됩니다. 데스크톱 앱과 같은 안정적인 사용성을 제공합니다. |

---

## 🏛️ 아키텍처 개요 (L1-L5)

이 프로젝트는 프로토콜의 유연성과 유지보수성을 극대화하기 위해 계층화된 모듈 구조를 따릅니다.

| Layer | 역할 | 설명 |
| :--- | :--- | :--- |
| **L5 (Presentation)** | UI/UX | Frontend 로직 및 자산 (`lim_arsenal/engine/L5_Presentation`). |
| **L4 (Bridge)** | API Gateway | 프로토콜 변환 및 API 통신 브리지 (`bridge_api.py`). |
| **L3 (Protocol)** | MCP Logic | 핵심 Model Context Protocol 처리 및 서버 관리. |
| **L2 (Engine)** | Core Logic | 백엔드 서비스 및 시스템 관리 모듈. |
| **L1 (Infrastructure)** | Runtime/OS | Python 환경, 파일 시스템 지속성 및 OS 수준 상호작용. |

---

## 🔗 공식 테스트 노드 (Official Test Node)

즉시 사용 가능한 공식 SSE 테스트 노드로 설정을 검증하세요:
- **SSE URL**: `http://35.202.58.51:8766/sse`
- **소스**: [Open World News MCP](https://github.com/lim-asdk/open-world-news-mcp)

---

## 🏗️ 디렉토리 구조 (Directory Structure)
- `lim_arsenal/engine/`: 핵심 백엔드 및 프론트엔드 자산.
- `installer_output/`: 빌드 아티팩트 및 설치 파일.
- `config/`: 애플리케이션 및 사용자 설정 파일.
- `docs/`: 기술 문서 및 설계 자료.

---

## 🏛️ 프로젝트 정체성
Matrix MCP는 **Lim Arsenal (lim-asdk)**의 프로젝트입니다.  
**PolyForm Noncommercial License 1.0** 라이선스를 따릅니다.

© 2026 Lim Arsenal. All rights reserved.
