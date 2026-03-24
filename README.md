# Matrix MCP v2.0

[![Status](https://img.shields.io/badge/Status-Public--Beta-orange?style=for-the-badge)](https://github.com/lim-asdk/Matrix_MCP_V2)
[![License](https://img.shields.io/badge/License-PolyForm--Noncommercial-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)](requirements.txt)
[![MCP](https://img.shields.io/badge/MCP-Native-blueviolet?style=for-the-badge)](https://modelcontextprotocol.io)

**AI-Powered Desktop & Web Workspace — Model Context Protocol (MCP) Native**

> Matrix MCP는 MCP 서버와 AI LLM을 연결하는 통합 데스크톱/웹 작업 환경입니다.  
> 실제 MCP 도구 호출, 실시간 AI 응답, 데스크톱/브라우저 이중 실행을 지원합니다.

---

## 핵심 기능

- 🔗 **MCP 서버 연결** — stdio / SSE 방식 모두 지원, 다중 서버 동시 연결
- 🤖 **AI 프로필 관리** — OpenAI, xAI Grok, DeepSeek 등 모든 OpenAI 호환 API
- 🧠 **페르소나 시스템** — 역할별 AI 행동 정의 (.txt 파일 기반)
- 🛠️ **도구 호출 로그** — 실시간 MCP 도구 호출/결과 채팅 뷰
- 🌐 **이중 실행 모드** — 데스크톱(pywebview) / 웹 브라우저

---

## 아키텍처 개요

```
Matrix_MCP_v2_0/
├── lim_arsenal/         # 코어 엔진 (분리된 계층 구조)
│   └── engine/
│       ├── L1_Infrastructure/   # 경로·설정·MCP 핸들러
│       ├── L2_AI_Engine/        # AI 응답 처리
│       ├── L3_Orchestration/    # Bridge API, Orchestrator
│       ├── L4_Prompt/           # 프롬프트·페르소나 로더
│       └── L5_Presentation/     # HTML/JS UI
├── user_data/           # 사용자 로컬 데이터 (git 미포함)
├── run_web_server.py    # 웹 실행 진입점
├── run_desktop_app.py   # 데스크톱 실행 진입점
└── requirements.txt
```

---

## 🚀 왜 Matrix MCP인가?

- **Zero Configuration AI**: OpenAI 호환 API만 있으면 즉시 시작 가능
- **Multi-Server Orchestration**: 여러 MCP 서버의 도구를 하나의 채팅창에서 통합 제어
- **Hybrid Execution**: 로컬 보안을 위한 데스크톱 앱과 접근성을 위한 웹 서버 동시 제공

---

## ⚡ 빠른 시작 (3분)

### 1. 서비스 준비

```bash
# 저장소 복제 및 이동
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2

# 가상환경 및 의존성 설치
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. 설정 (`.env`)

```bash
copy .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력하세요.
```

### 3. 즉시 실행

```bash
# 🌐 웹 모드 (권장: 브라우저에서 즉시 확인 가능)
python run_web_server.py

# 🖥️ 데스크톱 모드 (Windows 전용)
python run_desktop_app.py
```

---

## 실행 모드

| 모드 | 명령어 | 특징 |
|---|---|---|
| 웹 | `python run_web_server.py` | 브라우저 기반, 타 OS 재현 용이 |
| 데스크톱 | `python run_desktop_app.py` | Windows 네이티브, WebView2 필요 |

> **권장**: 새 환경에서는 웹 모드를 먼저 확인하세요.

---

## MCP 서버 연결

Settings → Servers에서 MCP 서버를 추가합니다.

- **stdio**: 로컬 Python 파일 실행 (`python your_server.py`)
- **SSE**: 원격 서버 URL (`http://host/sse`)

예시는 `user_data/servers/servers.example.json`을 참고하세요.

---

## 현재 상태

**Public Beta (v2.0)**

- ✅ 웹 모드: 정상 동작 확인
- ✅ 데스크톱 모드: Windows + WebView2 환경 정상 동작
- ✅ MCP stdio/SSE 연결
- ✅ 다중 AI 프로필
- 🔄 패키지 배포 (PyPI) — 예정

---

## 보안 원칙

- API Key는 **절대 코드에 직접 입력하지 마세요**. `.env` 파일을 사용하세요.
- `user_data/` 하위 폴더는 `.gitignore`로 버전 관리에서 제외됩니다.
- 실서버 정보, 대화 기록, 프로필이 저장소에 포함되지 않습니다.

---

## 라이선스

본 프로젝트는 **PolyForm Noncommercial License 1.0** 조건에 따라 배포됩니다.

- ✅ 개인 사용, 연구, 교육, 비상업적 목적 허용
- ❌ 상업적 이용 시 별도 상업 라이선스 필요

상업적 이용 문의: Lim Arsenal (lim-asdk) / rfcon0@gmail.com

---

## 로드맵

- [ ] PyPI 패키지 배포
- [ ] IQ-Pack 마켓플레이스
- [ ] 멀티 에이전트 오케스트레이션
- [ ] 클라우드 동기화

---

**Developer**: Lim Hwa Chan | **Provider**: Lim Arsenal
