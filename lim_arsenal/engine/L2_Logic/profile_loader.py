# -*- coding: utf-8 -*-
# Project: lim_chat_v1_4
# Developer: LIMHWACHAN
# Version: 1.4

"""
[L2 Logic Layer - Profile Loader]
Role: Handles the discovery, loading, and validation of Persona Profiles.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any

from L1_Infrastructure.path_manager import PathManager

logger = logging.getLogger("LimChat.Logic.Profile")


class ProfileLoader:
    def __init__(self):
        self.profile_dir = PathManager.get_profile_dir()

    def list_profiles(self) -> List[str]:
        if not self.profile_dir.exists():
            return []

        profiles = []
        for file in self.profile_dir.glob("*.json"):
            if file.stem.startswith("p_"):
                continue
            profiles.append(file.stem)
        return sorted(profiles)

    def get_default_profile(self) -> Dict[str, Any]:
        return {
            "name": "Emergency Assistant",
            "description": "A versatile emergency fallback AI for when primary profiles or prompts are missing.",
            "prompt_file": "emergency_assistant.txt",
            "system_prompt": "You are a helpful, versatile AI assistant. Provide clear and accurate information to the user.",
            "allowed_tools": [],
            "id": "emergency_assistant",
            "persona_id": "emergency_assistant",
        }

    def _builtin_persona_dir(self) -> Path:
        return PathManager.SRC_ROOT / "L4_Prompt" / "personas"

    def _read_prompt_text(self, prompt_name: str) -> str:
        if not prompt_name:
            return ""

        raw_name = Path(prompt_name)
        candidate_names = [raw_name.name] if raw_name.suffix else [f"{raw_name.name}.txt", f"{raw_name.name}.md"]
        roots = [PathManager.get_prompt_dir(), self._builtin_persona_dir()]

        for root in roots:
            for candidate_name in candidate_names:
                path = root / candidate_name
                if not path.exists():
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
                    return text.strip()
                except Exception:
                    continue
        return ""

    def _load_builtin_persona_profile(self, persona_name: str) -> Dict[str, Any]:
        prompt_text = self._read_prompt_text(persona_name)
        if not prompt_text:
            prompt_text = self.get_default_profile()["system_prompt"]

        display_name = persona_name.replace("_", " ").title() if persona_name else "Emergency Assistant"
        return {
            "name": display_name,
            "description": f"Built-in persona profile for {persona_name or 'emergency_assistant'}.",
            "prompt_file": f"{persona_name}.txt" if persona_name else "emergency_assistant.txt",
            "system_prompt": prompt_text,
            "allowed_tools": [],
            "id": persona_name or "emergency_assistant",
            "persona_id": persona_name or "emergency_assistant",
        }

    def load_profile(self, profile_name: str) -> Dict[str, Any]:
        profile_path = self.profile_dir / f"{profile_name}.json"

        if not profile_path.exists():
            logger.warning(f"Profile not found: {profile_name}. Falling back to built-in persona.")
            return self._load_builtin_persona_profile(profile_name)

        try:
            with open(profile_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid profile JSON for {profile_name}: {e}. Falling back to built-in persona.")
            return self._load_builtin_persona_profile(profile_name)
        except Exception as e:
            logger.warning(f"Failed to load profile {profile_name}: {e}. Falling back to built-in persona.")
            return self._load_builtin_persona_profile(profile_name)

        data.setdefault("id", profile_name)
        data.setdefault("name", profile_name.replace("_", " ").title())
        data.setdefault("system_prompt", "")
        data.setdefault("allowed_tools", [])
        data.setdefault("persona_id", data.get("persona_id", profile_name))

        prompt_source = data.get("prompt_file") or data.get("persona_id") or profile_name
        prompt_text = self._read_prompt_text(prompt_source)
        if prompt_text:
            data["system_prompt"] = prompt_text
            data["prompt_file_path"] = str(self._resolve_prompt_path(prompt_source))

        return data

    def _resolve_prompt_path(self, prompt_name: str) -> Path:
        raw_name = Path(prompt_name)
        candidate_names = [raw_name.name] if raw_name.suffix else [f"{raw_name.name}.txt", f"{raw_name.name}.md"]
        for root in [PathManager.get_prompt_dir(), self._builtin_persona_dir()]:
            for candidate_name in candidate_names:
                path = root / candidate_name
                if path.exists():
                    return path
        return self._builtin_persona_dir() / candidate_names[0]
