import asyncio
import threading
import logging
import os
import json
import subprocess
from urllib.parse import urlparse
from typing import Optional, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.types import Tool

logger = logging.getLogger("LimChat.MCP")


class McpClientHandler:
    """
    [L1 Infrastructure Layer]
    Manage one MCP server process/session over stdio or SSE/HTTP.
    """

    def __init__(self, name, server_config, project_root):
        self.name = name
        self.server_config = server_config or {}
        self.project_root = project_root
        self.session: Optional[ClientSession] = None
        self.tools: List[Tool] = []
        self._loop = None
        self._thread = None
        self._proc = None
        self._stop_event = asyncio.Event()
        self.status = "stopped"
        self.connected = False
        self.error_msg = ""

        retry_cfg = self.server_config.get("retry", {}) if isinstance(self.server_config, dict) else {}
        self._max_retries = int(retry_cfg.get("max_retries", 0))
        self._base_delay = float(retry_cfg.get("base_delay", 2.0))
        self._max_delay = float(retry_cfg.get("max_delay", 30.0))
        self._list_tools_retries = int(retry_cfg.get("list_tools_retries", 2))
        self._list_tools_delay = float(retry_cfg.get("list_tools_delay", 2.0))
        self._init_timeout = float(retry_cfg.get("init_timeout", 90.0))
        self._tools_timeout = float(retry_cfg.get("tools_timeout", 90.0))

    def start(self):
        self.status = "connecting"
        self.connected = False
        self.error_msg = ""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the MCP session and terminate any launched helper process."""
        self.status = "stopped"
        self.connected = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._stop_event.set)

        if getattr(self, "_proc", None):
            try:
                if self._proc.poll() is None:
                    self._proc.terminate()
                    try:
                        self._proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self._proc.kill()
            except Exception:
                pass
            finally:
                self._proc = None

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())

    async def _connect(self):
        transport_type = self.server_config.get("transport", "stdio").lower()
        attempt = 0
        delay = self._base_delay

        while not self._stop_event.is_set():
            try:
                self.status = "connecting"
                self.connected = False
                self.error_msg = ""

                if transport_type == "stdio":
                    await self._connect_stdio()
                elif transport_type in ("sse", "http"):
                    self._launch_local_sse_server_if_needed()
                    await self._connect_sse()
                else:
                    raise ValueError(f"Unknown transport type: {transport_type}")

                if self._stop_event.is_set():
                    break

                self.status = "error"
                self.error_msg = "Disconnected (session ended)"
                logger.warning(f"[{self.name}] Session ended, will retry.")
            except Exception as exc:
                self.status = "error"
                self.connected = False
                self.error_msg = str(exc)
                logger.error(f"[{self.name}] Connection failed: {exc}")

            attempt += 1
            if self._max_retries > 0 and attempt > self._max_retries:
                logger.error(f"[{self.name}] Max retries reached, giving up.")
                break

            await asyncio.sleep(delay)
            delay = min(self._max_delay, delay * 2)

    def _resolve_launch_spec(self):
        import sys
        cmd = self.server_config.get("command", sys.executable)
        if cmd.lower() in ["python", "python3", "python.exe"]:
            cmd = sys.executable
        args = self.server_config.get("args", [])
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env.update(self.server_config.get("env", {}))

        configured_cwd = self.server_config.get("cwd")
        cwd = None
        if configured_cwd:
            cwd = os.path.abspath(os.path.join(self.project_root, configured_cwd)) if not os.path.isabs(configured_cwd) else configured_cwd

        resolved_args = []
        for arg in args:
            if arg.endswith(".py") and not os.path.isabs(arg):
                candidate_paths = []
                if cwd:
                    candidate_paths.append(os.path.join(cwd, arg))
                candidate_paths.append(os.path.join(self.project_root, arg))
                candidate = next((path for path in candidate_paths if os.path.exists(path)), candidate_paths[-1])
                resolved_args.append(candidate)
            else:
                resolved_args.append(arg)

        if not cwd:
            for arg in resolved_args:
                if arg.endswith(".py") and os.path.exists(arg):
                    cwd = os.path.dirname(arg)
                    break

        if cwd:
            env["PYTHONPATH"] = cwd + os.pathsep + env.get("PYTHONPATH", "")

        return cmd, resolved_args, env, cwd

    async def _connect_stdio(self):
        cmd, resolved_args, env, cwd = self._resolve_launch_spec()
        server_params = StdioServerParameters(command=cmd, args=resolved_args, env=env, cwd=cwd)

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await self._manage_session(session)

    async def _connect_sse(self):
        url = self.server_config.get("url")
        headers = self.server_config.get("headers", {})

        if not url:
            raise ValueError("URL is required for SSE transport")

        async with sse_client(url=url, headers=headers) as (read, write):
            async with ClientSession(read, write) as session:
                await self._manage_session(session)

    def _launch_local_sse_server_if_needed(self):
        transport_type = self.server_config.get("transport", "stdio").lower()
        if transport_type not in ("sse", "http"):
            return

        url = self.server_config.get("url", "")
        if not url:
            return

        parsed = urlparse(url)
        if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            return

        if getattr(self, "_proc", None) and self._proc.poll() is None:
            return

        command = self.server_config.get("command")
        args = self.server_config.get("args", [])
        if not command or not args:
            return

        cmd, resolved_args, env, cwd = self._resolve_launch_spec()
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0

        self._proc = subprocess.Popen(
            [cmd, *resolved_args],
            cwd=cwd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
        logger.info(f"[{self.name}] Launched local SSE server for {url}")

    async def _manage_session(self, session):
        self.session = session
        try:
            await asyncio.wait_for(session.initialize(), timeout=self._init_timeout)

            last_error = None
            for i in range(self._list_tools_retries + 1):
                try:
                    result = await asyncio.wait_for(session.list_tools(), timeout=self._tools_timeout)
                    self.tools = result.tools
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    if i < self._list_tools_retries:
                        await asyncio.sleep(self._list_tools_delay)
            if last_error:
                raise last_error

            self.status = "connected"
            self.connected = True
            self.error_msg = ""
            logger.info(f"[{self.name}] Connect success. Tools: {len(self.tools)}")
        except asyncio.TimeoutError:
            self.status = "error"
            self.connected = False
            self.error_msg = "Connection timeout (check server output for stray prints)"
            logger.error(f"[{self.name}] {self.error_msg}")
            return
        except Exception as exc:
            self.status = "error"
            self.connected = False
            self.error_msg = str(exc)
            logger.error(f"[{self.name}] Session init failed: {exc}")
            return

        await self._stop_event.wait()

    def call_tool_sync(self, name: str, arguments: dict):
        if not self.session or not self._loop:
            raise Exception("Session not connected")

        future = asyncio.run_coroutine_threadsafe(self.session.call_tool(name, arguments), self._loop)
        try:
            result = future.result(timeout=60)
            texts = [c.text for c in result.content if c.type == "text"]
            full_text = "\n".join(texts)
            try:
                return json.loads(full_text)
            except Exception:
                return {"raw_text": full_text}
        except Exception as exc:
            raise exc
