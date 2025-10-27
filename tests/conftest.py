"""
Pytest configuration and fixtures for FlashRecord tests
"""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_data():
    """Provide sample configuration data"""
    return {
        "save_directory": "flashrecord-save",
        "default_compression": "balanced",
        "default_gif_fps": 10,
        "default_gif_duration": 5,
    }
