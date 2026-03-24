# Matrix MCP v2.0

[English](./README.md) | 한국어

[![Status](https://img.shields.io/badge/상태-공개_베타-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/라이선스-PolyForm--비상업용-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)

**Model Context Protocol(MCP)을 위한 AI 기반 통합 데스크톱 및 웹 워크스페이스입니다.**  
MCP 서버 연결, AI 프로필 관리, 페르소나 시스템을 지원하며 브라우저 또는 데스크톱 환경에서 즉시 실행 가능합니다.

---

## 🚀 주요 특징

- **MCP 네이티브 지원**: **stdio** 및 **SSE**를 통한 로컬/원격 MCP 서버 연결.
- **멀티 AI 프로필**: OpenAI, xAI Grok, DeepSeek 등 모든 OpenAI 호환 API 지원.
- **하이브리드 런타임**: **Windows 데스크톱** 앱과 **웹 서버** 모드 동시 지원.
- **AI 페르소나 시스템**: `.txt` 파일 기반의 역할 설정으로 AI 행동 양식 제어.
- **도구 작업 공간**: MCP 도구 호출 과정 및 결과를 채팅창에서 실시간으로 확인.

---

## ⚡ 빠른 시작 (3분 가이드)

### 1. 설치 및 환경 준비
```bash
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2
python -m venv .venv
```

**가상환경 활성화:**
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. 설정
```bash
copy .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력하세요.
```

### 3. 실행 모드 선택
- **웹 모드 (권장)**: `python run_web_server.py` (브라우저에서 즉시 확인)
- **데스크톱 모드**: `python run_desktop_app.py` (Windows 전용, WebView2 필요)

---

## ⚙️ 실행 모드 비교

| 모드 | 실행 명령어 | 특징 |
|:---:|---|---|
| **웹** | `python run_web_server.py` | 모든 브라우저 지원, 가장 안정적인 첫 실행 방법 |
| **데스크톱** | `python run_desktop_app.py` | Windows 네이티브 창 실행, WebView2 환경 필요 |

---

## 🔗 기본 제공 테스트 노드

사용자가 클론 즉시 성능을 체험할 수 있도록 공식 테스트 노드를 사전 제공합니다:
- **SSE URL**: `http://35.202.58.51:8766/sse`
- **프로젝트**: [Open World News MCP (GitHub)](https://github.com/lim-asdk/open-world-news-mcp)

---

## 📄 세부 문서 바로가기
- [상세 빠른 시작 가이드](./docs/ko/QUICK_START.md)
- [시스템 아키텍처 개요](./docs/ko/ARCHITECTURE.md)
- [최신 릴리스 노트](./docs/ko/RELEASE_NOTES_v2.0.0-beta1.md)

---

## 🏛️ 프로젝트 정체성
Matrix MCP는 **Lim Arsenal (lim-asdk)**의 프로젝트입니다.  
본 프로젝트는 **PolyForm Noncommercial License 1.0**에 따라 배포됩니다.

© 2026 Lim Arsenal. All rights reserved.
