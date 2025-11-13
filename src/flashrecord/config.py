"""
Pydantic-based Configuration - Type-safe, validated settings
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FlashRecordConfig(BaseModel):
    """Type-safe configuration with validation"""

    command_style: Literal["numbered", "vs_vc_vg", "verbose"] = Field(
        default="numbered",
        description="Command input style: numbered (1,2,3), abbreviation (vs,vc,vg), or full words",
    )
    auto_delete_hours: int = Field(
        default=24, ge=0, description="Auto-delete files older than N hours (0=disabled)"
    )
    hcap_path: str = Field(
        default="d:\\Sanctum\\hcap-1.5.0\\simple_capture.py",
        description="Path to optional legacy hcap screenshot tool",
    )

    @field_validator("command_style")
    @classmethod
    def validate_command_style(cls, v):
        """Validate command style is supported"""
        if v not in ["numbered", "vs_vc_vg", "verbose"]:
            raise ValueError(f"Invalid command_style: {v}")
        return v

    @field_validator("hcap_path")
    @classmethod
    def validate_hcap_path(cls, v):
        """Warn if hcap path doesn't exist"""
        if v and not Path(v).exists():
            print(f"[!] Warning: hcap path not found: {v}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "command_style": "numbered",
                "auto_delete_hours": 24,
                "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py",
            }
        }
    )


class Config:
    """Configuration manager with Pydantic validation"""

    ENV_PREFIX = "FLASHRECORD_"

    def __init__(self, config_file: str = "config.json"):
        # Navigate from src/flashrecord to project root
        self.parent_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.config_file = self._resolve_config_path(config_file)
        self.output_root = os.getenv(f"{self.ENV_PREFIX}OUTPUT_ROOT") or os.path.join(
            self.parent_dir, "output"
        )
        os.makedirs(self.output_root, exist_ok=True)

        # Load and validate config
        self._config = self._load_config()
        self._apply_config()

        # Expose structured directories
        self.save_dir = self.get_output_dir("gifs")
        self.gif_dir = self.save_dir
        self.screenshot_dir = self.get_output_dir("screenshots")
        self.session_dir = self.get_output_dir("sessions")
        self.video_dir = self.get_output_dir("captures")

    def _resolve_config_path(self, config_file: str) -> str:
        if os.path.isabs(config_file):
            return config_file
        return os.path.join(self.parent_dir, config_file)

    def _get_env(self, key: str) -> Optional[str]:
        return os.getenv(f"{self.ENV_PREFIX}{key}")

    def _load_env_overrides(self) -> dict:
        overrides = {}
        if (value := self._get_env("COMMAND_STYLE")):
            overrides["command_style"] = value
        if (value := self._get_env("AUTO_DELETE_HOURS")):
            try:
                overrides["auto_delete_hours"] = int(value)
            except ValueError:
                print(f"[!] Invalid FLASHRECORD_AUTO_DELETE_HOURS '{value}', using default")
        if (value := self._get_env("HCAP_PATH")):
            overrides["hcap_path"] = value
        return overrides

    def _load_config(self) -> FlashRecordConfig:
        """Load and validate configuration"""
        data = {}
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file) as f:
                    data = json.load(f)
        except json.JSONDecodeError:
            print(f"[!] Invalid JSON in {self.config_file}, using defaults")
        except ValueError as e:
            print(f"[!] Config validation error: {e}, using defaults")

        env_overrides = self._load_env_overrides()
        data.update({k: v for k, v in env_overrides.items() if v is not None})

        return FlashRecordConfig(**data)

    def _apply_config(self):
        """Apply loaded configuration"""
        self.command_style = self._config.command_style
        self.auto_delete_hours = self._config.auto_delete_hours
        self.hcap_path = self._config.hcap_path

    def get_output_dir(self, category: str, date: Optional[str] = None) -> str:
        """Return a dated output directory for a given category (screenshots/gifs/sessions)."""
        safe_category = category or "misc"
        date_segment = date or datetime.now().strftime("%Y%m%d")
        path = os.path.join(self.output_root, date_segment, safe_category)
        os.makedirs(path, exist_ok=True)
        return path

    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(json.loads(self._config.model_dump_json()), f, indent=2)
        except Exception as e:
            print(f"[-] Config save error: {str(e)}")

    def model_dump(self):
        """Export configuration as dict"""
        return self._config.model_dump()

    def schema_json(self):
        """Export JSON schema for documentation"""
        return self._config.model_json_schema()
