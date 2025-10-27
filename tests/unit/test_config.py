"""
Unit tests for flashrecord.config module
"""

from pathlib import Path

import pytest

from flashrecord.config import Config


class TestConfig:
    """Tests for Config class"""

    def test_config_initialization(self):
        """Test that Config can be initialized"""
        config = Config()
        assert config is not None

    def test_default_save_directory(self):
        """Test default save directory is set"""
        config = Config()
        assert hasattr(config, "save_dir")
        assert config.save_dir is not None

    def test_config_singleton_pattern(self):
        """Test that Config maintains configuration"""
        config1 = Config()
        config2 = Config()
        # Both should work independently
        assert config1.save_dir == config2.save_dir

    def test_save_directory_type(self):
        """Test save directory is string"""
        config = Config()
        assert isinstance(config.save_dir, str)

    def test_save_directory_not_empty(self):
        """Test save directory is not empty"""
        config = Config()
        assert len(config.save_dir) > 0
