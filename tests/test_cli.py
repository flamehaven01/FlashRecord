"""
Minimal CLI Tests - Core functionality only
"""

import pytest
from flashrecord.cli import FlashRecordCLI


@pytest.fixture
def cli():
    """Create CLI instance for testing"""
    return FlashRecordCLI()


def test_map_command_universal(cli):
    """Test universal commands"""
    assert cli.map_command("exit") == ("exit", None)
    assert cli.map_command("quit") == ("exit", None)
    assert cli.map_command("help") == ("help", None)
    assert cli.map_command("@sc") == ("screenshot", None)
    assert cli.map_command("@sv") == ("gif", None)


def test_map_command_numbered(cli):
    """Test numbered style (default)"""
    assert cli.map_command("1") == ("start", None)
    assert cli.map_command("2") == ("stop", None)
    assert cli.map_command("3") == ("gif", None)
    assert cli.map_command("4") == ("save", "claude")


def test_map_command_unknown(cli):
    """Test unknown command"""
    # New implementation returns unknown command as param for debugging
    action, param = cli.map_command("random")
    assert action == "unknown"
    assert param is not None  # Command is passed for debugging
