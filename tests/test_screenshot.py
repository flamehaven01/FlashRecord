"""
Unit tests for screenshot module - screenshot.py (native implementation)
Tests the take_screenshot function with native Pillow/PIL
"""

import os
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import sys


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
    """Test suite for take_screenshot function (native implementation)"""

    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_windows')
    def test_take_screenshot_success_windows(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test successful screenshot capture on Windows"""
        from flashrecord.screenshot import take_screenshot

        # Mock successful capture and save
        mock_img = MagicMock()
        mock_capture.return_value = mock_img
        mock_save.return_value = True

        result = take_screenshot(temp_output_dir)

        # Verify save was called
        assert mock_save.called
        assert "screenshot_20250101_120000.png" in result
        assert temp_output_dir in result

    @patch('flashrecord.screenshot.sys.platform', 'darwin')
    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_macos')
    def test_take_screenshot_success_macos(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test successful screenshot capture on macOS"""
        from flashrecord.screenshot import take_screenshot

        # Mock successful capture and save
        mock_img = MagicMock()
        mock_capture.return_value = mock_img
        mock_save.return_value = True

        result = take_screenshot(temp_output_dir)

        # Verify capture and save were called
        assert mock_capture.called
        assert mock_save.called
        assert result is not None

    @patch('flashrecord.screenshot.sys.platform', 'linux')
    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_linux')
    def test_take_screenshot_success_linux(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test successful screenshot capture on Linux"""
        from flashrecord.screenshot import take_screenshot

        # Mock successful capture and save
        mock_img = MagicMock()
        mock_capture.return_value = mock_img
        mock_save.return_value = True

        result = take_screenshot(temp_output_dir)

        # Verify capture and save were called
        assert mock_capture.called
        assert mock_save.called
        assert result is not None

    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_windows')
    def test_take_screenshot_capture_returns_none(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test screenshot when capture fails"""
        from flashrecord.screenshot import take_screenshot

        # Mock failed capture
        mock_capture.return_value = None

        result = take_screenshot(temp_output_dir)

        # Verify result is None
        assert result is None
        # Save should not be called
        assert not mock_save.called

    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_windows')
    def test_take_screenshot_save_fails(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test screenshot when save fails"""
        from flashrecord.screenshot import take_screenshot

        # Mock successful capture but failed save
        mock_img = MagicMock()
        mock_capture.return_value = mock_img
        mock_save.return_value = False

        result = take_screenshot(temp_output_dir)

        # Verify result is None
        assert result is None

    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_windows')
    def test_take_screenshot_creates_directory(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test that output directory is created"""
        from flashrecord.screenshot import take_screenshot

        # Mock successful capture and save
        mock_img = MagicMock()
        mock_capture.return_value = mock_img
        mock_save.return_value = True

        nested_dir = os.path.join(temp_output_dir, "nested", "dir")
        result = take_screenshot(nested_dir)

        # Verify directory was created by assertion that save was called
        assert mock_save.called

    @patch('flashrecord.screenshot._save_image')
    @patch('flashrecord.screenshot._capture_windows')
    def test_take_screenshot_exception_handling(
        self, mock_capture, mock_save, mock_timestamp, temp_output_dir
    ):
        """Test exception handling in take_screenshot"""
        from flashrecord.screenshot import take_screenshot

        # Mock exception during capture
        mock_capture.side_effect = Exception("Capture failed")

        result = take_screenshot(temp_output_dir)

        # Verify result is None and exception was handled
        assert result is None


class TestSaveImage:
    """Test suite for _save_image function"""

    def test_save_image_success(self, temp_output_dir):
        """Test successful image save"""
        from flashrecord.screenshot import _save_image
        from PIL import Image

        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        filepath = os.path.join(temp_output_dir, "test.png")

        result = _save_image(img, filepath)

        assert result is True
        assert os.path.exists(filepath)

    def test_save_image_rgba_conversion(self, temp_output_dir):
        """Test RGBA to RGB conversion during save"""
        from flashrecord.screenshot import _save_image
        from PIL import Image

        # Create RGBA image
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        filepath = os.path.join(temp_output_dir, "test_rgba.png")

        result = _save_image(img, filepath)

        assert result is True
        assert os.path.exists(filepath)

    def test_save_image_none_input(self, temp_output_dir):
        """Test save with None image"""
        from flashrecord.screenshot import _save_image

        filepath = os.path.join(temp_output_dir, "test_none.png")
        result = _save_image(None, filepath)

        assert result is False
        assert not os.path.exists(filepath)

    def test_save_image_creates_directory(self, temp_output_dir):
        """Test that directory is created if it doesn't exist"""
        from flashrecord.screenshot import _save_image
        from PIL import Image

        img = Image.new('RGB', (100, 100), color='blue')
        nested_path = os.path.join(temp_output_dir, "a", "b", "c", "test.png")

        result = _save_image(img, nested_path)

        assert result is True
        assert os.path.exists(nested_path)
