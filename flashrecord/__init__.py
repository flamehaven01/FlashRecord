"""
FlashRecord v0.3.0 - Screen Capture & Animated GIF Recording
Simple, fast, standalone screen recording tool
"""

__version__ = "0.3.0"
__author__ = "Flamehaven"

from .cli import FlashRecordCLI
from .screenshot import take_screenshot
from .screen_recorder import ScreenRecorder, record_screen_to_gif
from .manager import FileManager
from .ai_prompt import AIPromptManager
from .install import InstallWizard, run_setup_if_needed

__all__ = [
    'FlashRecordCLI',
    'take_screenshot',
    'ScreenRecorder',
    'record_screen_to_gif',
    'FileManager',
    'AIPromptManager',
    'InstallWizard',
    'run_setup_if_needed',
]
