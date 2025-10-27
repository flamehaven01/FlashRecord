"""
Unit tests for flashrecord.screenshot module
"""

import pytest


class TestScreenshotModule:
    """Tests for screenshot module"""

    def test_import_take_screenshot(self):
        """Test that take_screenshot function can be imported"""
        from flashrecord.screenshot import take_screenshot

        assert take_screenshot is not None
        assert callable(take_screenshot)

    def test_function_signature(self):
        """Test take_screenshot has expected parameters"""
        from flashrecord.screenshot import take_screenshot
        import inspect

        sig = inspect.signature(take_screenshot)
        params = list(sig.parameters.keys())

        # Should have output_dir, compress, quality parameters
        assert "output_dir" in params
        assert "compress" in params
        assert "quality" in params


class TestScreenshotHelpers:
    """Tests for screenshot helper functions"""

    def test_platform_specific_imports(self):
        """Test that platform-specific capture functions exist"""
        from flashrecord import screenshot

        # Check that helper functions exist
        assert hasattr(screenshot, "_capture_windows")
        assert hasattr(screenshot, "_capture_macos")
        assert hasattr(screenshot, "_capture_linux")
        assert hasattr(screenshot, "_save_image")
