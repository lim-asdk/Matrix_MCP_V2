# -*- coding: utf-8 -*-
# Project: lim_chat_v1_3
# Developer: LIMHWACHAN
# Version: 1.3

import time
import logging
import threading
import sys
from pathlib import Path
from typing import Dict
import ctypes
from ctypes import wintypes

# 상위 계층 임포트 (L1, L2, L3)
from L1_Infrastructure.config_manager import ConfigManager
from L1_Infrastructure.mcp_handler import McpClientHandler
from L1_Infrastructure.path_manager import PathManager
from L2_Logic.history_manager import HistoryManager
from L2_Logic.profile_loader import ProfileLoader
from L3_Orchestration.ai_engine import LimChatAIEngine

logger = logging.getLogger("LimChat.Bridge")

class LimChatBridgeAPI:
    """
    [L3 Orchestration Layer]
    역할: 웹뷰(L5 Presentation)와 내부 로직을 잇는 통로입니다.
    사용자의 요청을 받아 적절한 모듈(L1, L2, L3)을 호출하고 결과를 반환합니다.
    """
    def __init__(self, use_schema=False, config_filename="config_standard.json", auto_init=True):
        self._window = None
        self.use_schema = use_schema
        
        # [CRITICAL] ConfigManager initialization
        self._config_manager = ConfigManager(config_filename=config_filename)
        self._history_manager = HistoryManager()
        
        # 서버 및 도구 관리
        self._clients: Dict[str, McpClientHandler] = {}
        self._tool_map: Dict[str, str] = {}
        
        # 캐시 설정
        self._history_cache = []
        self._history_dirty = 0
        self._history_flush_every = 5
        
        self._profile_loader = ProfileLoader()
        self._profile_loader.profile_dir = PathManager.get_profile_dir()
        
        self._active_persona = self._config_manager.config.get("last_persona") or "stock_analyst"

        # [Prompt Management]
        from L2_Logic.backup_manager import BackupManager
        self._PROMPTS_DIR = PathManager.get_prompt_dir()
        self._BACKUPS_DIR = self._PROMPTS_DIR / "backups"
        self._HISTORY_FILE = PathManager.PROJECT_ROOT / "data" / "prompt_history.json"
        
        self._backup_manager = BackupManager(
            prompts_dir=str(self._PROMPTS_DIR),
            backups_dir=str(self._BACKUPS_DIR),
            history_file=str(self._HISTORY_FILE)
        )
        
        if auto_init:
            self._init_servers()
        
        logger.info(f"BridgeAPI initialized (Config: {config_filename})")

    def get_prompt_files(self):
        try:
            files = []
            for f in self._PROMPTS_DIR.glob("*.md"):
                 layer = f.stem.split("_")[0] if "_" in f.stem else "Unknown"
                 files.append({"name": f.stem, "path": str(f), "layer": layer})
            files.sort(key=lambda x: x['name'])
            return files
        except Exception as e:
            logger.error(f"Failed to list prompt files: {e}")
            return []

    def get_prompt_file(self, layer):
        try:
            file_path = self._PROMPTS_DIR / f"{layer}.md"
            if not file_path.exists(): return {"error": "Prompt file not found"}
            return {"layer": layer, "content": file_path.read_text(encoding='utf-8')}
        except Exception as e:
            return {"error": str(e)}

    def update_prompt_file(self, layer, content, reason="Manual edit via UI"):
        try:
            file_path = self._PROMPTS_DIR / f"{layer}.md"
            if file_path.exists(): self._backup_manager.create_backup(layer, reason)
            file_path.write_text(content, encoding='utf-8')
            return {"status": "success", "message": f"Prompt '{layer}' updated."}
        except Exception as e:
            return {"error": str(e)}

    def get_backups(self, layer=None, limit=None):
        try:
            if limit is not None: limit = int(limit)
            return self._backup_manager.list_backups(layer_name=layer, limit=limit)
        except Exception as e:
            return {"error": str(e)}

    def restore_backup(self, backup_filename):
        try:
            self._backup_manager.restore_backup(backup_filename)
            return {"status": "success", "message": f"Restored from {backup_filename}"}
        except Exception as e:
            return {"error": str(e)}

    def get_prompt_diff(self, layer, backup_filename):
        try:
            diff = self._backup_manager.get_diff(layer, backup_filename)
            return {"diff": diff}
        except Exception as e:
            return {"error": str(e)}

    def get_prompt_history(self):
        try:
            if not self._HISTORY_FILE.exists(): return []
            import json
            with open(self._HISTORY_FILE, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}

    def create_backup_snapshot(self, reason="Manual Backup"):
         try:
             results = []
             for f in self._PROMPTS_DIR.glob("*.md"):
                 layer_name = f.stem
                 self._backup_manager.create_backup(layer_name, reason)
                 results.append(layer_name)
             return {"status": "success", "message": f"Created snapshots for: {', '.join(results)}"}
         except Exception as e:
             return {"error": str(e)}

    def generate_prompt_snapshot(self):
        try:
            from datetime import datetime
            snapshot_dir = PathManager.PROJECT_ROOT / "프롬프트_관리_시스템" / "snapshots"
            snapshot_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_file = snapshot_dir / f"prompt_snapshot_{timestamp}.md"
            prompt_files = sorted(self._PROMPTS_DIR.glob("*.md"))
            if not prompt_files: return {"error": "No prompt files found"}
            
            content = ["# 프롬프트 시스템 스냅샷\n", f"**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"]
            for file_path in prompt_files:
                layer_name = file_path.stem
                content.append(f"## {layer_name}\n\n```markdown\n{file_path.read_text(encoding='utf-8')}\n```\n\n---\n\n")
            snapshot_file.write_text(''.join(content), encoding='utf-8')
            return {"status": "success", "file_path": str(snapshot_file), "file_name": snapshot_file.name}
        except Exception as e:
            return {"error": str(e)}

    def _init_servers(self):
        project_root = PathManager.PROJECT_ROOT
        servers_conf = self._config_manager.config.get("mcpServers", {})
        for name, conf in servers_conf.items():
            try:
                client = McpClientHandler(name, conf, project_root)
                client.start()
                self._clients[name] = client
            except Exception as e:
                logger.error(f"Failed to initialize server '{name}': {e}")

    def _bind_tools_dynamic(self, persona_name):
        try:
            profile = self._profile_loader.load_profile(persona_name)
            keywords = profile.get("capability_keywords", [])
            if not keywords: return profile.get("allowed_tools", [])
            
            allowed_tools = []
            # [Thread Safety] Use list() to avoid RuntimeError
            for server_name, client in list(self._clients.items()):
                if client.status != "connected": continue
                disabled_list = self._config_manager.config.get("mcpServers", {}).get(server_name, {}).get("disabled_tools", [])
                for tool in client.tools:
                    if tool.name in disabled_list: continue
                    tool_text = f"{tool.name} {tool.description}".lower()
                    for keyword in keywords:
                        if keyword.lower() in tool_text:
                            allowed_tools.append(tool.name); break
            return allowed_tools
        except Exception as e:
            logger.error(f"Binding failed: {e}")
            return []

    def set_window(self, window):
        self._window = window

    def chat(self, message, use_ai_mode, use_server=False):
        try:
            active_id = self._config_manager.config.get("active_profile_id")
            meta = self._config_manager.get_profile_meta(active_id)
            if not meta: return {"response": "Please select a profile first."}
            
            api_key = self._config_manager.get_api_key(active_id)
            engine_config = self._config_manager.load_engine_config()
            engine = LimChatAIEngine(api_key, meta["model"], meta["base_url"], use_schema=self.use_schema, engine_config=engine_config)
            engine.profile_loader.profile_dir = self._profile_loader.profile_dir
            
            dynamic_whitelist = self._bind_tools_dynamic(self._active_persona)
            system_prompt = engine.set_persona(self._active_persona, allowed_tools_override=dynamic_whitelist)
            
            if not self._history_manager.current_session_file: self._history_manager.start_new_session()
            self._append_history({"role": "user", "content": message, "timestamp": self._ts()})
            
            recent_hist = self._history_manager.load_history(self._history_manager.current_session_file.name)[-10:]
            recent_hist = [{k: v for k, v in m.items() if k != "tool_calls"} for m in recent_hist]

            all_openai_tools = []
            self._refresh_tool_map()
            if use_server:
                # [Thread Safety] Use list() to avoid RuntimeError
                for name, c in list(self._clients.items()):
                    if c.status == "connected":
                        disabled_list = self._config_manager.config.get("mcpServers", {}).get(name, {}).get("disabled_tools", [])
                        for t in c.tools:
                            if t.name not in disabled_list:
                                all_openai_tools.append({"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.inputSchema}})

            res = engine.process_chat(message, recent_hist, all_openai_tools, use_server, self._tool_map, self._clients, system_prompt_override=system_prompt)
            self._append_history({"role": "assistant", "content": res.get("response", ""), "timestamp": self._ts()})
            
            self._config_manager.config["last_persona"] = self._active_persona
            self._config_manager.save()
            return res

        except Exception as e:
            logger.error(f"Chat failed: {e}")
            try:
                # Emergency Fallback logic simplified for stability
                return {"response": f"⚠️ **Emergency Fallback Active**: Original error: {str(e)}"}
            except:
                return {"response": f"❌ Error: {str(e)}"}

    def _refresh_tool_map(self):
        self._tool_map = {}
        # [Thread Safety] Use list() to avoid RuntimeError
        for s_name, client in list(self._clients.items()):
            if client.status == "connected":
                for t in client.tools:
                    self._tool_map[t.name] = s_name

    def _ts(self):
        return int(time.time() * 1000)

    def _append_history(self, msg_obj):
        if not self._history_cache:
            self._history_cache = self._history_manager.load_history(self._history_manager.current_session_file.name)
        self._history_cache.append(msg_obj)
        self._history_dirty += 1
        if self._history_dirty >= self._history_flush_every:
            self._history_manager.save_history(self._history_cache)
            self._history_dirty = 0

    def get_profiles(self): 
        return {"profiles": self._config_manager.config.get("profiles", []), "active_id": self._config_manager.config.get("active_profile_id")}
    
    def activate_profile(self, pid): 
        self._config_manager.config["active_profile_id"] = pid
        self._config_manager.save()
        return {"status": "ok"}
    
    def save_profile(self, profile_data):
        pid = profile_data.get("id") or f"p_{int(time.time()*1000)}"
        profile_data["id"] = pid
        profile_meta = profile_data.copy()
        new_key = profile_meta.pop("api_key", None)
        profiles = self._config_manager.config.get("profiles", [])
        found = False
        for i, p in enumerate(profiles):
            if p["id"] == pid:
                if new_key == "******": profile_meta["key_file"] = p.get("key_file")
                profiles[i] = profile_meta
                found = True; break
        if not found: profiles.append(profile_meta)
        self._config_manager.config["profiles"] = profiles
        if new_key and new_key != "******": self._config_manager.save_api_key(pid, new_key)
        self._config_manager.save()
        return {"status": "saved", "id": pid}

    def get_server_status(self):
        # [Thread Safety] Use list() to avoid RuntimeError
        return [{"name": n, "status": c.status, "tools": len(c.tools)} for n, c in list(self._clients.items())]
    
    def get_tools(self):
        all_tools = {}
        # [Thread Safety] Use list() to avoid RuntimeError
        for s_name, client in list(self._clients.items()):
            disabled_list = self._config_manager.config.get("mcpServers", {}).get(s_name, {}).get("disabled_tools", [])
            for t in client.tools:
                all_tools[t.name] = {"name": t.name, "description": t.description, "server": s_name, "enabled": t.name not in disabled_list}
        return {"tools": all_tools}

    def get_server_tools(self, name):
        if name not in self._clients: return {"ok": False, "message": "Server is not connected.", "tools": []}
        disabled_list = self._config_manager.config.get("mcpServers", {}).get(name, {}).get("disabled_tools", [])
        tools = []
        for t in self._clients[name].tools:
            tools.append({"name": t.name, "description": t.description, "parameters": t.inputSchema, "enabled": t.name not in disabled_list})
        return {"ok": True, "tools": tools, "status": self._clients[name].status}

    def get_server_config_list(self):
        """[UI] 설정된 서버 목록을 반환합니다."""
        return self._config_manager.config.get("mcpServers", {})

    def get_python_executable(self):
        """Return the actual system Python executable used for server commands."""
        try:
            # Try to resolve via 'py' launcher if available on Windows
            output = subprocess.check_output(
                ["py", "-3.14", "-c", "import sys; print(sys.executable)"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output:
                return output
        except Exception:
            pass
        return sys.executable

    def save_server_config(self, name, command, args_str, transport="stdio", url=None, headers_str=None, display_name=None):
        """[UI] 서버 설정을 저장하고 재시작합니다 (Transport 지원 추가)."""
        args = [a.strip() for a in args_str.split('\n') if a.strip()]
        
        # 헤더 파싱 (Key=Value 형태)
        headers = {}
        if headers_str:
            for line in headers_str.split('\n'):
                if '=' in line:
                    k, v = line.split('=', 1)
                    headers[k.strip()] = v.strip()

        # Preserve existing env from JSON if available
        existing_conf = self._config_manager.config.get("mcpServers", {}).get(name, {})
        env = existing_conf.get("env", {}).copy()
        
        # Enforce essential flags
        env["PYTHONUNBUFFERED"] = "1"
        env["GR_BOOT_SILENT"] = "1"

        server_data = {
            "name": display_name or name, 
            "transport": transport,  # stdio, sse, http
            "command": command,
            "args": args,
            "env": env,
            "url": url,
            "headers": headers
        }
        
        print(f"\n[BRIDGE] SAVE ATTEMPT: {name} (Transport: {transport})\n")
        success = self._config_manager.save_server(name, server_data)
        if not success:
            print(f"[BRIDGE] SAVE FAILED for {name}!")
            return {"status": "failed", "message": "File save failed"}
        print(f"[BRIDGE] SAVE SUCCESS for {name}.")

        # 서버 재시작
        if name in self._clients:
            try:
                self._clients[name].stop()
            except:
                pass
        
        project_root = PathManager.PROJECT_ROOT
        new_client = McpClientHandler(name, server_data, project_root)
        new_client.start()
        self._clients[name] = new_client
        
        return {"status": "saved"}

    def delete_server(self, name):
        """[UI] 서버 설정을 삭제하고 가동 중인 클라이언트를 중지합니다."""
        if name in self._clients:
            try:
                self._clients[name].stop()
                del self._clients[name]
            except:
                pass
        success = self._config_manager.delete_server(name)
        return {"status": "deleted" if success else "failed"}

    def toggle_tool(self, server_name, tool_name, enabled):
        """[UI] 특정 도구의 활성화 여부를 전환합니다."""
        server_conf = self._config_manager.config.get("mcpServers", {}).get(server_name)
        if not server_conf:
            return {"status": "error", "message": "Server configuration not found."}
        
        disabled_list = server_conf.get("disabled_tools", [])
        if enabled:
            if tool_name in disabled_list:
                disabled_list.remove(tool_name)
        else:
            if tool_name not in disabled_list:
                disabled_list.append(tool_name)
        
        server_conf["disabled_tools"] = disabled_list
        self._config_manager.save_server(server_name, server_conf)
        return {"status": "ok", "enabled": enabled}

    def toggle_server_tools(self, server_name, enabled):
        """[UI] 특정 서버의 모든 도구를 일괄 활성화/비활성화합니다."""
        server_conf = self._config_manager.config.get("mcpServers", {}).get(server_name)
        if not server_conf:
            return {"status": "error", "message": "Server configuration not found."}
        
        client = self._clients.get(server_name)
        if not client:
            return {"status": "error", "message": "Server is not connected."}
            
        all_tool_names = [t.name for t in client.tools]
        
        if enabled:
            server_conf["disabled_tools"] = []
        else:
            server_conf["disabled_tools"] = all_tool_names
            
        self._config_manager.save_server(server_name, server_conf)
        return {"status": "ok", "enabled": enabled}

    def test_connection(self, command, args_str, transport="stdio", url=None, headers_str=None, display_name=None):
        """[UI] 입력된 설정으로 서버 연결을 테스트합니다 (Transport 지원)."""
        args = [a.strip() for a in args_str.split('\n') if a.strip()]
        
        headers = {}
        if headers_str:
            for line in headers_str.split('\n'):
                if '=' in line:
                    k, v = line.split('=', 1)
                    headers[k.strip()] = v.strip()

        existing_conf = self._config_manager.config.get("mcpServers", {}).get(display_name or "Test Server", {})
        env = existing_conf.get("env", {}).copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["GR_BOOT_SILENT"] = "1"

        temp_config = {
            "name": display_name or "Test Server",
            "transport": transport,
            "command": command,
            "args": args,
            "env": env,
            "url": url,
            "headers": headers
        }
        
        temp_name = "test_temp"
        project_root = PathManager.PROJECT_ROOT
        client = McpClientHandler(temp_name, temp_config, project_root)
        last_error = None
        remote_transport = transport.lower() in ("sse", "http")
        
        try:
            client.start()
            for _ in range(20):
                time.sleep(0.5)
                if client.status == "connected":
                    tools = []
                    for t in client.tools:
                        tools.append({
                            "name": t.name,
                            "description": t.description,
                            "parameters": t.inputSchema
                        })
                    return {"ok": True, "status": "connected", "tools": tools}
                if client.status == "error":
                    if remote_transport:
                        last_error = client.error_msg or "Unknown Error"
                        continue
                    return {"ok": False, "message": client.error_msg or "Unknown Error"}
            
            if last_error:
                return {"ok": False, "message": f"Connection Timeout: Server did not respond in 10s ({last_error})"}
            return {"ok": False, "message": "Connection Timeout: Server did not respond in 10s"}
        except Exception as e:
            return {"ok": False, "message": str(e)}
        finally:
            try:
                client.stop()
            except:
                pass

    def test_profile(self, api_key, model, base_url, profile_id=None):
        try:
            from openai import OpenAI
            test_client = OpenAI(api_key=api_key, base_url=base_url)
            test_client.chat.completions.create(model=model, messages=[{"role": "user", "content": "hi"}], max_tokens=5)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def load_history_list(self): return self._history_manager.get_history_list()
    def load_history_session(self, fname): return self._history_manager.load_history(fname)
    def start_new_chat(self): return {"status": "ok", "filename": self._history_manager.start_new_session()}
    def get_engine_config(self): return self._config_manager.load_engine_config()
    def get_settings_template(self):
        p = PathManager.get_ui_path("settings.html")
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def get_personas(self):
        try:
            return {"personas": [{"id": n, "name": n.replace("_", " ").title()} for n in self._profile_loader.list_profiles()], "active_id": self._active_persona}
        except:
            return {"personas": [{"id": "default_assistant", "name": "Emergency Assistant"}], "active_id": self._active_persona}

    def switch_persona(self, persona_id):
        available = self._profile_loader.list_profiles()
        if persona_id not in available: persona_id = available[0] if available else "default_assistant"
        self._active_persona = persona_id
        self._config_manager.config["last_persona"] = persona_id
        self._config_manager.save()
        return {"status": "ok", "active_id": persona_id}
