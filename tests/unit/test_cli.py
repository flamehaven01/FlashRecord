"""
Unit tests for flashrecord.cli module
"""

import pytest

from flashrecord.cli import FlashRecordCLI


class TestFlashRecordCLI:
    """Tests for FlashRecordCLI class"""

    def test_cli_initialization(self):
        """Test that CLI can be initialized"""
        cli = FlashRecordCLI()
        assert cli is not None

    def test_cli_has_config(self):
        """Test CLI has config attribute"""
        cli = FlashRecordCLI()
        assert hasattr(cli, "config")
        assert cli.config is not None

    def test_cli_has_ai_manager(self):
        """Test CLI has ai_manager attribute"""
        cli = FlashRecordCLI()
        assert hasattr(cli, "ai_manager")
        assert cli.ai_manager is not None

    def test_cli_has_methods(self):
        """Test CLI has expected methods"""
        cli = FlashRecordCLI()
        assert hasattr(cli, "show_help")
        assert hasattr(cli, "handle_screenshot")
        assert callable(cli.show_help)
        assert callable(cli.handle_screenshot)

    def test_show_help_no_crash(self, capsys):
        """Test show_help doesn't crash"""
        cli = FlashRecordCLI()
        # Should not raise exception
        cli.show_help()

        # Verify some output was produced
        captured = capsys.readouterr()
        assert len(captured.out) > 0
        assert "FlashRecord" in captured.out
