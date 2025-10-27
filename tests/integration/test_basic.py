"""
Basic integration tests for FlashRecord v0.3.0
"""

import pytest


class TestImports:
    """Test that all main modules can be imported"""

    def test_import_config(self):
        """Test config module import"""
        from flashrecord.config import Config

        assert Config is not None

    def test_import_utils(self):
        """Test utils module import"""
        from flashrecord.utils import format_filesize, get_timestamp

        assert format_filesize is not None
        assert get_timestamp is not None

    def test_import_manager(self):
        """Test manager module import"""
        from flashrecord.manager import FileManager

        assert FileManager is not None

    def test_import_screenshot(self):
        """Test screenshot module import"""
        from flashrecord.screenshot import take_screenshot

        assert take_screenshot is not None

    def test_import_screen_recorder(self):
        """Test screen_recorder module import"""
        from flashrecord.screen_recorder import ScreenRecorder, record_screen_to_gif

        assert ScreenRecorder is not None
        assert record_screen_to_gif is not None

    def test_import_compression(self):
        """Test compression module import"""
        from flashrecord.compression import CWAMInspiredCompressor

        assert CWAMInspiredCompressor is not None

    def test_import_cli(self):
        """Test CLI module import"""
        from flashrecord.cli import FlashRecordCLI

        assert FlashRecordCLI is not None

    def test_import_ai_prompt(self):
        """Test AI prompt module import"""
        from flashrecord.ai_prompt import AIPromptManager

        assert AIPromptManager is not None


class TestBasicFunctionality:
    """Test basic functionality without file operations"""

    def test_config_creation(self):
        """Test Config can be created"""
        from flashrecord.config import Config

        config = Config()
        assert config.save_dir is not None

    def test_manager_creation(self):
        """Test FileManager can be created"""
        from flashrecord.manager import FileManager

        manager = FileManager()
        assert manager.save_dir is not None

    def test_cli_creation(self):
        """Test CLI can be created"""
        from flashrecord.cli import FlashRecordCLI

        cli = FlashRecordCLI()
        assert cli is not None

    def test_compressor_creation(self):
        """Test compressor can be created"""
        from flashrecord.compression import CWAMInspiredCompressor

        compressor = CWAMInspiredCompressor()
        assert compressor is not None

    def test_ai_prompt_manager_creation(self):
        """Test AI prompt manager can be created"""
        from flashrecord.ai_prompt import AIPromptManager

        manager = AIPromptManager()
        assert manager is not None
