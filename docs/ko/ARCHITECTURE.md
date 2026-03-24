# 시스템 아키텍처 개요

Matrix MCP v2.0은 모듈성, 확장성 및 보안을 보장하기 위해 엄격한 계층 구조(L1~L5)를 따릅니다.

## 📐 계층형 구조

### L1: Infrastructure (기반 계층)
- **PathManager**: 프로젝트 루트 기준의 전역 경로 해결.
- **ConfigManager**: JSON 설정 및 API 키의 안전한 로드.
- **MCP Handler**: stdio 및 SSE 프로토콜의 하위 레벨 관리.

### L2: Logic (로직 계층)
- **ProfileLoader**: AI 프로필 및 행동 정의 로드.
- **HistoryManager**: 대화 기록 유지 및 세션 메모리 관리.
- **BackupManager**: 프롬프트 및 페르소나 자동 스냅샷 시스템.

### L3: Orchestration (조정 계층)
- **Bridge API**: UI와 로직 사이의 중앙 통신 허브.
- **AI Engine**: LLM 처리, 도구 호출 루프 및 스키마 관리.
- **Orchestrator**: 다중 MCP 서버 및 AI 에이전트 조정.

### L4: Prompt (인터페이스 계층)
- **Persona System**: 역할 기반 AI 행동 정의.
- **Prompt Templates**: 작업별 구조화된 상호작용 패턴.

### L5: Presentation (표현 계층)
- **Web UI**: 현대적인 글래스모피즘(Glassmorphism) 스타일의 HTML/JS 인터페이스.
- **Desktop Shell**: Windows 실행을 위한 가벼운 래퍼(Wrapper).

## 🔒 보안 및 데이터 관리
- 모든 사용자 데이터는 `user_data/` 폴더에 저장되며, Git 버전 관리에서 엄격히 제외됩니다.
- API 키는 `.env` 및 개별 암호화 스타일 JSON 파일을 통해 관리됩니다.
- 공개 배포판에는 설정용 `.example` 템플릿만 포함됩니다.
