"""
Minimal AI Prompt Manager - Save sessions to markdown
"""

import os
from datetime import datetime
from typing import Dict, List


class AIPromptManager:
    """Minimal session saving"""

    def __init__(self, save_dir="flashrecord-save"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.ai_files = {
            "claude": f"{save_dir}/claude.md",
            "gemini": f"{save_dir}/gemini.md",
            "codex": f"{save_dir}/codex.md",
            "general": f"{save_dir}/general.md",
        }
        self._init_files()

    def _init_files(self):
        """Initialize markdown files"""
        for model, path in self.ai_files.items():
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"# {model.capitalize()} Sessions\n\n")

    def save_session(self, ai_model):
        """Save session entry"""
        try:
            if ai_model not in self.ai_files:
                return False
            with open(self.ai_files[ai_model], "a", encoding="utf-8") as f:
                f.write(f"- {datetime.now().isoformat()}\n")
            return True
        except Exception:
            return False

    def get_instruction_notes(self) -> Dict[str, str]:
        """
        Load reusable instruction snippets from the AI markdown files.

        Instructions can be defined either inside the block delimited by
        `<!-- instructions:start -->` / `<!-- instructions:end -->` or under a
        `## Instructions` heading.
        """
        notes: Dict[str, str] = {}
        for model, path in self.ai_files.items():
            section = self._read_instruction_section(path)
            if section:
                notes[model] = section
        return notes

    def _read_instruction_section(self, path: str) -> str:
        """Return instruction text from a markdown file if available."""
        if not path or not os.path.exists(path):
            return ""

        try:
            with open(path, encoding="utf-8") as handle:
                lines = [line.rstrip("\n") for line in handle]
        except Exception:
            return ""

        start_marker = "<!-- instructions:start -->"
        end_marker = "<!-- instructions:end -->"
        instructions: List[str] = []

        # Prefer explicit HTML comment markers
        capturing = False
        for line in lines:
            stripped = line.strip()
            if stripped == start_marker:
                capturing = True
                continue
            if stripped == end_marker and capturing:
                break
            if capturing:
                instructions.append(line)

        if instructions:
            return "\n".join(instructions).strip()

        # Fallback to `## Instructions` section
        instructions = []
        capture_section = False
        for line in lines:
            stripped = line.strip()
            if stripped.lower() == "## instructions":
                capture_section = True
                continue
            if capture_section and stripped.startswith("## "):
                break
            if capture_section:
                instructions.append(line)

        return "\n".join(instructions).strip()
