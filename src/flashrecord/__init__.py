"""
FlashRecord v0.3.5 - Screen Capture & Animated GIF Recording
Simple, fast, standalone screen recording tool
v0.3.5: Production quality with comprehensive test coverage
"""

__version__ = "0.3.5"
__author__ = "Flamehaven"

from .ai_prompt import AIPromptManager
from .cli import FlashRecordCLI
from .install import InstallWizard, run_setup_if_needed
from .manager import FileManager
from .screen_recorder import ScreenRecorder, record_screen_to_gif
from .screenshot import take_screenshot

__all__ = [
    "FlashRecordCLI",
    "take_screenshot",
    "ScreenRecorder",
    "record_screen_to_gif",
    "FileManager",
    "AIPromptManager",
    "InstallWizard",
    "run_setup_if_needed",
]
