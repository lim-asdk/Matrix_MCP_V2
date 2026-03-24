# Matrix MCP v2.0

[English](./README.md) | 한국어

[![Status](https://img.shields.io/badge/상태-공개_베타-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/라이선스-PolyForm--비상업용-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)

**전문적인 MCP 운영 워크스페이스.**  
Model Context Protocol(MCP) 서버와 AI 프로필을 연결, 테스트 및 관리하기 위한 전문 환경입니다.

---

[**🚀 제품 홈페이지 바로가기**](https://lim-asdk.github.io/Matrix_MCP_V2/) | [**💾 최신 릴리스 다운로드**](https://github.com/lim-asdk/Matrix_MCP_V2/releases/latest)

---

## 📖 기술 개요 (Technical Overview)

Matrix MCP는 Model Context Protocol의 **운영(Operational)** 측면에 집중한 특화 워크스페이스입니다. 일반적인 챗봇 클라이언트가 단순히 채팅에 치중하는 것과 달리, Matrix MCP는 MCP 연결의 생애주기 관리와 AI 도구 호출(Tool-calling) 워크플로우를 위한 구조화된 환경을 제공합니다.

### 핵심 역량
- **기본 MCP 지원**: **stdio** 및 **SSE** 전송 계층과의 직접적인 통합.
- **제공자 중립성**: Grok, OpenAI, DeepSeek, Google Gemini 등 모든 OpenAI 호환 API를 도구 실행과 매끄럽게 연결합니다.
- **하이브리드 런타임**: 빠른 브라우저 기반 상호작용(Web-first)과 안정적인 Windows 데스크톱 실행 환경에 최적화되었습니다.
- **운영자용 검사기(Inspector)**: 원본 도구 요청/응답 데이터와 AI의 추론 체인을 실시간으로 모니터링할 수 있습니다.

---

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
