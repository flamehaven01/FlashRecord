"""
Unit tests for screenshot module - screenshot.py
Tests the take_screenshot function with mocked subprocess and file operations
"""

import os
import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test output"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def mock_timestamp(monkeypatch):
    """Mock the get_timestamp function to return a consistent value"""
    from flashrecord import utils
    monkeypatch.setattr(utils, 'get_timestamp', lambda: '20250101_120000')
    return '20250101_120000'


class TestTakeScreenshot:
    """Test suite for take_screenshot function"""

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_success(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test successful screenshot capture"""
        from flashrecord.screenshot import take_screenshot

        # Mock file existence check to return True for the output file
        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        result = take_screenshot("test_output")

        # Verify directory was created
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)

        # Verify subprocess was called with correct arguments
        assert mock_subprocess.called
        args, kwargs = mock_subprocess.call_args
        # Check that hcap path is in the command
        assert 'd:\\Sanctum\\hcap-1.5.0\\simple_capture.py' in args[0][1]
        # Check that filename contains screenshot and .png
        assert "screenshot_" in args[0][2]
        assert ".png" in args[0][2]

        # Verify result contains the filepath
        assert result is not None
        assert "screenshot_" in result
        assert ".png" in result

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_subprocess_failure(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot when subprocess returns error"""
        from flashrecord.screenshot import take_screenshot

        # Mock subprocess failure
        mock_exists.return_value = False
        mock_subprocess.return_value = MagicMock(
            returncode=1,
            stderr=b"hcap error message"
        )

        with patch('builtins.print') as mock_print:
            result = take_screenshot("test_output")

        # Should return None on failure
        assert result is None

        # Verify error message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("hcap failed" in str(call) for call in print_calls)

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_file_not_created(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot when file is not created despite success returncode"""
        from flashrecord.screenshot import take_screenshot

        # Mock subprocess returns success but file doesn't exist
        mock_subprocess.return_value = MagicMock(returncode=0)
        mock_exists.return_value = False

        with patch('builtins.print'):
            result = take_screenshot("test_output")

        # Should return None if file wasn't created
        assert result is None

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_timeout(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot timeout handling"""
        from flashrecord.screenshot import take_screenshot
        import subprocess

        # Mock subprocess timeout
        mock_subprocess.side_effect = subprocess.TimeoutExpired('cmd', 5)

        with patch('builtins.print') as mock_print:
            result = take_screenshot("test_output")

        # Should return None on timeout
        assert result is None

        # Verify timeout message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("timeout" in str(call).lower() for call in print_calls)

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_general_exception(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot with general exception"""
        from flashrecord.screenshot import take_screenshot

        # Mock general exception
        mock_makedirs.side_effect = OSError("Permission denied")

        with patch('builtins.print') as mock_print:
            result = take_screenshot("test_output")

        # Should return None on error
        assert result is None

        # Verify error message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("error" in str(call).lower() for call in print_calls)

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_default_output_dir(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot with default output directory"""
        from flashrecord.screenshot import take_screenshot

        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        result = take_screenshot()

        # Should use default directory
        mock_makedirs.assert_called_once_with(
            "flashrecord-save/screenshots", exist_ok=True
        )
        assert result is not None

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_custom_output_dir(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test screenshot with custom output directory"""
        from flashrecord.screenshot import take_screenshot

        custom_dir = "custom/screenshots/path"
        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        result = take_screenshot(custom_dir)

        # Should use provided directory
        mock_makedirs.assert_called_once_with(custom_dir, exist_ok=True)
        assert result is not None
        assert custom_dir in result

    @patch('flashrecord.screenshot.subprocess.run')
    @patch('flashrecord.screenshot.os.path.exists')
    @patch('flashrecord.screenshot.os.makedirs')
    def test_take_screenshot_hcap_path_configuration(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test that hcap path is correctly configured"""
        from flashrecord.screenshot import take_screenshot

        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        take_screenshot()

        # Verify hcap path is correctly set
        args, _ = mock_subprocess.call_args
        assert 'd:\\Sanctum\\hcap-1.5.0\\simple_capture.py' in args[0][1]
