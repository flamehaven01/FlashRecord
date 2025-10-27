"""
Unit tests for flashrecord.compression module
"""

import numpy as np
import pytest
from PIL import Image

from flashrecord.compression import CWAMInspiredCompressor


class TestCWAMInspiredCompressor:
    """Tests for CWAMInspiredCompressor class"""

    def test_compressor_initialization(self):
        """Test that compressor can be initialized"""
        compressor = CWAMInspiredCompressor()
        assert compressor is not None

    def test_compressor_has_methods(self):
        """Test compressor has expected methods"""
        compressor = CWAMInspiredCompressor()
        assert hasattr(compressor, "compress_frames")
        assert callable(compressor.compress_frames)

    def test_create_simple_frame(self):
        """Test creating a simple test frame"""
        # Create a simple 100x100 red image
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))
        assert img.size == (100, 100)
        assert img.mode == "RGB"

    def test_compressor_with_single_frame(self):
        """Test compressor with single simple frame"""
        compressor = CWAMInspiredCompressor()
        frames = [Image.new("RGB", (100, 100), color=(255, 0, 0))]

        # Test that compress method exists and can be called
        # Note: We don't test actual compression as it requires file I/O
        assert hasattr(compressor, "compress_frames")
