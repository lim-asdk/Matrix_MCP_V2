# -*- coding: utf-8 -*-
# Project: lim_chat_v1_3en
# Developer: LIMHWACHAN
# Version: 1.3

"""
[L4 Prompt Layer - Dynamic Loader]
AI prompts are loaded from external prompt files when available.
This loader now falls back to the built-in persona directory so legacy
setups without a packs/ directory still resolve their AI identity.
"""

import re
from pathlib import Path

from L1_Infrastructure.path_manager import PathManager


class PromptLoader:
    """
    Dynamically loads AI prompts from external text/markdown files.
    """

    def __init__(self, prompts_dir=None):
        if prompts_dir is None:
            self.prompts_dir = PathManager.get_prompt_dir()
        else:
            self.prompts_dir = Path(prompts_dir)

    def _candidate_roots(self):
        roots = [self.prompts_dir]
        builtin_root = PathManager.SRC_ROOT / "L4_Prompt" / "personas"
        if builtin_root not in roots:
            roots.append(builtin_root)
        return roots

    def _candidate_names(self, layer_name):
        raw_name = Path(layer_name)
        if raw_name.suffix:
            return [raw_name.name]
        return [f"{raw_name.name}.md", f"{raw_name.name}.txt"]

    def load(self, layer_name):
        """
        Load prompt text from a specific layer file.
        """
        for root in self._candidate_roots():
            for candidate_name in self._candidate_names(layer_name):
                file_path = root / candidate_name
                if not file_path.exists():
                    continue
                try:
                    raw_content = file_path.read_text(encoding="utf-8").strip()
                    return self._sanitize_content(raw_content)
                except Exception:
                    continue
        return ""

    def _sanitize_content(self, content):
        """
        Strip HTML comments so metadata does not leak into the system prompt.
        """
        sanitized = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        return sanitized.strip()

    def load_all(self, persona_id=None, l2_file=None, l3_file=None):
        l4_file = persona_id if persona_id else "L4_stock_analyst"
        l2_target = l2_file if l2_file else "L2_data_processing"
        l3_target = l3_file if l3_file else "L3_orchestration"

        return {
            "L2": self.load(l2_target),
            "L3": self.load(l3_target),
            "L4": self.load(l4_file),
        }

    def reload(self):
        return self.load_all()
