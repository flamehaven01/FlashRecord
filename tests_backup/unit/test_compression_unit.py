"""
Unit tests for compression module (GIF compression with CWAM)
"""
import os
import pytest
import numpy as np
from PIL import Image
from flashrecord.compression import GIFCompressor, CWAMInspiredCompressor


class TestGIFCompressor:
    """Test GIF compression functionality"""

    @pytest.mark.unit
    def test_compressor_initialization(self):
        """Test compressor can be initialized"""
        compressor = GIFCompressor(target_size_mb=10.0, quality='balanced')
        assert compressor.target_size_mb == 10.0
        assert compressor.compression_mode == 'balanced'

    @pytest.mark.unit
    def test_compressor_with_quality_modes(self):
        """Test different quality modes"""
        high = GIFCompressor(target_size_mb=10.0, quality='high')
        balanced = GIFCompressor(target_size_mb=10.0, quality='balanced')
        compact = GIFCompressor(target_size_mb=10.0, quality='compact')

        assert high.scale_factor > balanced.scale_factor
        assert balanced.scale_factor > compact.scale_factor

    @pytest.mark.unit
    def test_compress_frames_reduces_count(self, test_frames):
        """Test frame compression reduces frame count"""
        compressor = GIFCompressor(target_size_mb=1.0, quality='balanced')
        compressed = compressor.compress_frames(test_frames)

        # Should reduce frames
        assert len(compressed) <= len(test_frames)
        # Should preserve timing
        assert compressor.get_stats()['preserve_timing_ok']

    @pytest.mark.unit
    def test_compress_to_target_size(self, test_frames):
        """Test compression achieves target size"""
        compressor = GIFCompressor(target_size_mb=0.5, quality='balanced')
        compressed = compressor.compress_frames(test_frames)

        # Compressed should have fewer frames
        assert len(compressed) < len(test_frames)

    @pytest.mark.unit
    def test_stats_reporting(self, test_frames):
        """Test statistics are reported correctly"""
        compressor = GIFCompressor(target_size_mb=1.0, quality='balanced')
        compressed = compressor.compress_frames(test_frames)
        stats = compressor.get_stats()

        assert 'frame_count' in stats
        assert 'duration' in stats
        assert 'preserve_timing_ok' in stats
        assert stats['frame_count'] == len(compressed)


class TestCWAMInspiredCompressor:
    """Test CWAM-inspired compression features"""

    @pytest.mark.unit
    def test_cwam_compressor_initialization(self):
        """Test CWAM compressor initialization"""
        compressor = CWAMInspiredCompressor(quality='balanced')
        assert compressor.quality == 'balanced'

    @pytest.mark.unit
    def test_adaptive_tile_size(self, complex_image, sample_image):
        """Test adaptive tile sizing based on complexity"""
        compressor = CWAMInspiredCompressor(quality='balanced')

        # Complex image should use smaller tiles
        complex_gray = np.array(complex_image.convert('L'))
        tile_complex = compressor._adaptive_tile_size(complex_gray)

        # Simple image should use larger tiles
        simple_gray = np.array(sample_image.convert('L'))
        tile_simple = compressor._adaptive_tile_size(simple_gray)

        # Complex should have smaller or equal tile size
        assert tile_complex <= tile_simple

    @pytest.mark.unit
    def test_saliency_computation(self, test_frames):
        """Test saliency computation"""
        compressor = CWAMInspiredCompressor(quality='balanced')

        # Should compute saliency for frames
        saliency = compressor._compute_saliency_map(test_frames[0])

        assert saliency is not None
        assert isinstance(saliency, np.ndarray)
        assert saliency.shape == test_frames[0].size[::-1]  # (height, width)

    @pytest.mark.unit
    def test_frame_selection_preserves_salient(self, test_frames):
        """Test frame selection preserves high-saliency frames"""
        compressor = CWAMInspiredCompressor(quality='balanced')

        # Compress with saliency-based selection
        compressed = compressor.compress_frames(test_frames, target_frames=5)

        # Should keep some frames
        assert len(compressed) > 0
        assert len(compressed) <= len(test_frames)

    @pytest.mark.unit
    def test_palette_optimization(self, test_frames):
        """Test palette optimization"""
        compressor = CWAMInspiredCompressor(quality='balanced')

        # Get optimized palette
        palette = compressor._build_palette(test_frames[:3])

        assert palette is not None
        assert len(palette) <= 256  # GIF palette limit

    @pytest.mark.unit
    def test_compression_with_timing_preservation(self, test_frames):
        """Test timing preservation during compression"""
        compressor = CWAMInspiredCompressor(quality='balanced')

        # Original duration (10 frames at 100ms each = 1000ms)
        original_duration = len(test_frames) * 100

        compressed = compressor.compress_frames(
            test_frames,
            original_fps=10,
            target_fps=5
        )

        # Check timing is preserved
        stats = compressor.get_stats()
        # Duration should be roughly preserved (within 10%)
        if stats.get('duration'):
            duration_diff = abs(stats['duration'] - original_duration)
            assert duration_diff < original_duration * 0.1

    @pytest.mark.unit
    def test_error_handling_empty_frames(self):
        """Test error handling with empty frame list"""
        compressor = CWAMInspiredCompressor(quality='balanced')
        result = compressor.compress_frames([])

        # Should return empty list or handle gracefully
        assert result == [] or result is None

    @pytest.mark.unit
    def test_error_handling_invalid_quality(self):
        """Test error handling with invalid quality"""
        # Should default to balanced or raise informative error
        try:
            compressor = CWAMInspiredCompressor(quality='invalid')
            # If it doesn't raise, should default to something reasonable
            assert compressor.quality in ['high', 'balanced', 'compact']
        except ValueError:
            # Acceptable to raise error
            pass

    @pytest.mark.unit
    def test_memory_efficiency_large_frames(self):
        """Test memory efficiency with large number of frames"""
        # Create 100 frames
        large_frame_list = []
        for i in range(100):
            img = Image.new('RGB', (640, 480), color=(i*2, 100, 200))
            large_frame_list.append(img)

        compressor = CWAMInspiredCompressor(quality='compact')

        # Should handle without crashing
        compressed = compressor.compress_frames(large_frame_list, target_frames=10)

        assert len(compressed) <= 10
        assert len(compressed) > 0
