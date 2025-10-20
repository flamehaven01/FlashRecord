"""
FlashRecord - Fast, Simple, Easy Screen Recording & GIF Generator
Standalone version for cross-project use
"""

__version__ = "0.1.0"
__author__ = "Flamehaven"

from .cli import FlashRecordCLI
from .screenshot import take_screenshot
from .video_recorder import record_video
from .manager import FileManager
from .ai_prompt import AIPromptManager
from .install import InstallWizard, run_setup_if_needed

__all__ = [
    'FlashRecordCLI',
    'take_screenshot',
    'record_video',
    'FileManager',
    'AIPromptManager',
    'InstallWizard',
    'run_setup_if_needed',
]
