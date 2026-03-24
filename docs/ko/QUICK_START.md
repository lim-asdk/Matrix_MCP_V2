# 상세 빠른 시작 가이드 (한국어)

Matrix MCP v2.0에 오신 것을 환영합니다. 이 가이드는 3분 이내에 시스템을 설치하고 실행하는 방법을 안내합니다.

## 1. 준비 사항
- Python 3.10 이상
- Git

## 2. 설치 과정

### 저장소 복제
```bash
git clone https://github.com/lim-asdk/Matrix_MCP_V2.git
cd Matrix_MCP_V2
```

### 가상 환경 설정
```bash
python -m venv .venv
```

**활성화 방법:**
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

### 의존성 설치
```bash
pip install -r requirements.txt
```

## 3. 환경 설정

### 환경 변수 (.env)
1. 예시 파일 복사: `copy .env.example .env`
2. `.env` 파일을 열어 `OPENAI_API_KEY`를 입력합니다.
3. (선택 사항) Grok이나 DeepSeek 등 다른 API를 사용한다면 `OPENAI_BASE_URL`을 수정합니다.

### MCP 서버 설정
시스템은 `user_data/servers/servers.example.json`을 기본으로 포함하고 있습니다. UI에서 이 파일을 선택하면 즉시 공식 SSE 테스트 노드에 연결할 수 있습니다.

## 4. 워크스페이스 실행

### 웹 모드 (권장)
가장 안정적이며 브라우저에서 즉시 확인 가능합니다.
```bash
python run_web_server.py
```
실행 후 브라우저에서 `http://127.0.0.1:2027`로 접속하세요.

### 데스크톱 모드
Windows 전용 네이티브 경험을 제공합니다.
```bash
python run_desktop_app.py
```
*참고: Windows에 WebView2 런타임이 설치되어 있어야 합니다.*

## 5. UI 초기 설정
1. **Settings → AI Profiles**에서 API 키와 모델이 올바르게 설정되었는지 확인합니다.
2. **Settings → Servers**에서 리스트 중 `servers.example`을 선택한 후 **Save & Restart**를 클릭합니다.
3. 대화를 시작하세요! AI가 페르소나에 맞춰 MCP 도구를 자동으로 호출합니다.
