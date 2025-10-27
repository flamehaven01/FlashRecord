"""
Pytest configuration and shared fixtures for FlashRecord tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
from PIL import Image
import numpy as np

# Add flashrecord to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    tmp_dir = tempfile.mkdtemp(prefix="flashrecord_test_")
    yield tmp_dir
    # Cleanup
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)


@pytest.fixture
def sample_image():
    """Create a simple test image"""
    img = Image.new('RGB', (1920, 1080), color=(100, 150, 200))
    return img


@pytest.fixture
def complex_image():
    """Create a complex test image with random noise"""
    noise = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
    return Image.fromarray(noise)


@pytest.fixture
def gradient_image():
    """Create a gradient test image"""
    gradient = Image.new('RGB', (1920, 1080))
    pixels = gradient.load()
    for i in range(1920):
        color = int(255 * i / 1920)
        for j in range(1080):
            pixels[i, j] = (color, color, color)
    return gradient


@pytest.fixture
def test_frames():
    """Create a list of test frames for GIF testing"""
    frames = []
    for i in range(10):
        # Create frame with changing color
        color = int(255 * i / 10)
        img = Image.new('RGB', (640, 480), color=(color, 100, 200))
        frames.append(img)
    return frames


@pytest.fixture
def mock_config(temp_dir):
    """Mock configuration with temporary directory"""
    class MockConfig:
        def __init__(self):
            self.save_dir = temp_dir
            self.default_quality = 'balanced'
            self.default_fps = 10

    return MockConfig()


@pytest.fixture(autouse=True)
def reset_test_state():
    """Reset any global state before each test"""
    yield
    # Cleanup any global state here if needed


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir
