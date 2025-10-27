"""
Unit tests for screenshot module
"""
import os
import pytest
from PIL import Image
from flashrecord.screenshot import take_screenshot, _save_image


class TestScreenshotModule:
    """Test screenshot functionality"""

    @pytest.mark.unit
    def test_save_image_default(self, temp_dir, sample_image):
        """Test saving image with default settings"""
        filepath = os.path.join(temp_dir, "test.png")
        result = _save_image(sample_image, filepath, compress=False)

        assert result is True
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0

    @pytest.mark.unit
    def test_save_image_balanced_compression(self, temp_dir, sample_image):
        """Test saving image with balanced compression"""
        filepath = os.path.join(temp_dir, "test_balanced.png")
        result = _save_image(sample_image, filepath, compress=True, quality='balanced')

        assert result is True
        assert os.path.exists(filepath)

        # Check resolution is reduced (50% scale)
        saved_img = Image.open(filepath)
        assert saved_img.width == int(sample_image.width * 0.5)
        assert saved_img.height == int(sample_image.height * 0.5)

    @pytest.mark.unit
    def test_save_image_high_quality_compression(self, temp_dir, sample_image):
        """Test saving image with high quality compression"""
        filepath = os.path.join(temp_dir, "test_high.png")
        result = _save_image(sample_image, filepath, compress=True, quality='high')

        assert result is True
        saved_img = Image.open(filepath)
        assert saved_img.width == int(sample_image.width * 0.7)
        assert saved_img.height == int(sample_image.height * 0.7)

    @pytest.mark.unit
    def test_save_image_compact_compression(self, temp_dir, sample_image):
        """Test saving image with compact compression"""
        filepath = os.path.join(temp_dir, "test_compact.png")
        result = _save_image(sample_image, filepath, compress=True, quality='compact')

        assert result is True
        saved_img = Image.open(filepath)
        assert saved_img.width == int(sample_image.width * 0.3)
        assert saved_img.height == int(sample_image.height * 0.3)

    @pytest.mark.unit
    def test_save_image_creates_directory(self, temp_dir, sample_image):
        """Test that _save_image creates output directory if needed"""
        nested_dir = os.path.join(temp_dir, "nested", "path")
        filepath = os.path.join(nested_dir, "test.png")

        result = _save_image(sample_image, filepath, compress=False)

        assert result is True
        assert os.path.exists(filepath)

    @pytest.mark.unit
    def test_save_image_rgba_conversion(self, temp_dir):
        """Test RGBA to RGB conversion"""
        rgba_img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        filepath = os.path.join(temp_dir, "test_rgba.png")

        result = _save_image(rgba_img, filepath, compress=False)

        assert result is True
        saved_img = Image.open(filepath)
        # PNG should handle RGBA or convert to RGB
        assert saved_img.mode in ['RGB', 'RGBA']

    @pytest.mark.unit
    def test_save_image_invalid_input(self, temp_dir):
        """Test saving with None image"""
        filepath = os.path.join(temp_dir, "test.png")
        result = _save_image(None, filepath, compress=False)

        assert result is False
        assert not os.path.exists(filepath)

    @pytest.mark.unit
    def test_compression_reduces_file_size(self, temp_dir, complex_image):
        """Test that compression actually reduces file size"""
        filepath_default = os.path.join(temp_dir, "default.png")
        filepath_compressed = os.path.join(temp_dir, "compressed.png")

        _save_image(complex_image, filepath_default, compress=False)
        _save_image(complex_image, filepath_compressed, compress=True, quality='compact')

        size_default = os.path.getsize(filepath_default)
        size_compressed = os.path.getsize(filepath_compressed)

        assert size_compressed < size_default
        reduction = ((size_default - size_compressed) / size_default) * 100
        # Compact should achieve significant reduction
        assert reduction > 30  # At least 30% reduction

    @pytest.mark.integration
    @pytest.mark.slow
    def test_take_screenshot_default(self, temp_dir):
        """Test taking screenshot with default settings"""
        result = take_screenshot(output_dir=temp_dir, compress=False)

        if result:  # May fail on headless systems
            assert os.path.exists(result)
            assert result.endswith('.png')
            assert os.path.getsize(result) > 0
        else:
            pytest.skip("Screenshot capture not available on this system")

    @pytest.mark.integration
    @pytest.mark.slow
    def test_take_screenshot_compressed(self, temp_dir):
        """Test taking screenshot with compression"""
        result = take_screenshot(output_dir=temp_dir, compress=True, quality='balanced')

        if result:
            assert os.path.exists(result)
            assert result.endswith('.png')
        else:
            pytest.skip("Screenshot capture not available on this system")
