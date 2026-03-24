# Architecture Overview

Matrix MCP v2.0 follows a strictly layered architecture (L1 to L5) to ensure modularity, scalability, and security.

## 📐 Layered Structure

### L1: Infrastructure (Foundation)
- **PathManager**: Global path resolution relative to project root.
- **ConfigManager**: Secure loading of JSON configurations and API keys.
- **MCP Handler**: Low-level protocol management for stdio and SSE.

### L2: Logic (Brain)
- **ProfileLoader**: Loads AI profiles and behavior definitions.
- **HistoryManager**: Manages conversation persistence and session memory.
- **BackupManager**: Automated snapshot system for prompts and personas.

### L3: Orchestration (Bridge)
- **Bridge API**: The central communication hub between UI and logic.
- **AI Engine**: Core LLM processing, tool-calling loop, and schema management.
- **Orchestrator**: Coordinates multiple MCP servers and AI agents.

### L4: Prompt (Interface Contract)
- **Persona System**: Role-based AI behavior definitions.
- **Prompt Templates**: Structured interaction patterns for different tasks.

### L5: Presentation (Visual)
- **Web UI**: Modern, glassmorphic HTML/JS interface.
- **Desktop Shell**: Lightweight wrapper for Windows execution.

## 🔒 Security & Data
- All user data is stored in `user_data/`, which is strictly excluded from version control.
- API keys are managed via `.env` and encrypted-style JSON placeholders.
- Public distributions contain only `.example` templates for configuration.
