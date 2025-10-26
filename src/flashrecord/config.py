"""
Pydantic-based Configuration - Type-safe, validated settings
"""

import os
import json
from typing import Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ConfigDict


class FlashRecordConfig(BaseModel):
    """Type-safe configuration with validation"""

    command_style: Literal["numbered", "vs_vc_vg", "verbose"] = Field(
        default="numbered",
        description="Command input style: numbered (1,2,3), abbreviation (vs,vc,vg), or full words"
    )
    auto_delete_hours: int = Field(
        default=24,
        ge=0,
        description="Auto-delete files older than N hours (0=disabled)"
    )
    hcap_path: str = Field(
        default="d:\\Sanctum\\hcap-1.5.0\\simple_capture.py",
        description="Path to hcap screenshot tool"
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
        if not Path(v).exists():
            print(f"[!] Warning: hcap path not found: {v}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "command_style": "numbered",
                "auto_delete_hours": 24,
                "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
            }
        }
    )


class Config:
    """Configuration manager with Pydantic validation"""

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        # Navigate from src/flashrecord to project root
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Setup single flat directory
        self.save_dir = os.path.join(self.parent_dir, "output")
        os.makedirs(self.save_dir, exist_ok=True)

        # Load and validate config
        self._config = self._load_config()
        self._apply_config()

    def _load_config(self) -> FlashRecordConfig:
        """Load and validate configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    return FlashRecordConfig(**data)
        except json.JSONDecodeError:
            print(f"[!] Invalid JSON in {self.config_file}, using defaults")
        except ValueError as e:
            print(f"[!] Config validation error: {e}, using defaults")

        return FlashRecordConfig()

    def _apply_config(self):
        """Apply loaded configuration"""
        self.command_style = self._config.command_style
        self.auto_delete_hours = self._config.auto_delete_hours
        self.hcap_path = self._config.hcap_path

    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(
                    json.loads(self._config.model_dump_json()),
                    f,
                    indent=2
                )
        except Exception as e:
            print(f"[-] Config save error: {str(e)}")

    def model_dump(self):
        """Export configuration as dict"""
        return self._config.model_dump()

    def schema_json(self):
        """Export JSON schema for documentation"""
        return self._config.model_json_schema()
