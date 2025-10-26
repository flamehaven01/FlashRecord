"""
Test suite for improved compression module
Validates all enhancements from 8.txt and 9.txt
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flashrecord'))

import numpy as np
from PIL import Image
from compression_improved import CWAMInspiredCompressor


def create_test_frames(n=10, size=(100, 100), color_variance=True):
    """Create synthetic test frames"""
    frames = []
    for i in range(n):
        if color_variance:
            # Varying colors for diversity
            arr = np.random.randint(0, 256, (size[1], size[0], 3), dtype=np.uint8)
        else:
            # Uniform color
            color = (128 + i * 10) % 256
            arr = np.full((size[1], size[0], 3), color, dtype=np.uint8)

        frames.append(Image.fromarray(arr, 'RGB'))

    return frames


def test_initialization():
    """Test 1: Compressor initialization"""
    print("[>] Test 1: Initialization")

    compressor = CWAMInspiredCompressor(target_size_mb=5, quality='balanced', max_memory_mb=512)

    assert compressor.target_size_mb == 5
    assert compressor.scale_factor == 0.50
    assert compressor.min_colors == 16
    assert compressor.adaptive_tile_enabled == True

    print("[+] PASS: Initialization")


def test_input_validation():
    """Test 2: Input validation and error handling"""
    print("\n[>] Test 2: Input Validation")

    compressor = CWAMInspiredCompressor()

    # Empty frames
    assert compressor._validate_frames([]) == False

    # Valid frames
    frames = create_test_frames(5)
    assert compressor._validate_frames(frames) == True

    # Memory limit check
    compressor_small = CWAMInspiredCompressor(max_memory_mb=1)
    large_frames = create_test_frames(100, size=(1000, 1000))
    assert compressor_small._validate_frames(large_frames) == False

    print("[+] PASS: Input Validation")


def test_safe_convert():
    """Test 3: Safe frame conversion"""
    print("\n[>] Test 3: Safe Convert")

    compressor = CWAMInspiredCompressor()

    # Valid conversion
    frame = Image.new('RGB', (50, 50), (255, 0, 0))
    gray = compressor._safe_convert(frame, 'L')
    assert gray.mode == 'L'

    # Corrupted frame simulation (should return placeholder)
    # In real scenario, this would catch PIL errors

    print("[+] PASS: Safe Convert")


def test_adaptive_tile_size():
    """Test 4: Adaptive tile sizing (9.txt #3)"""
    print("\n[>] Test 4: Adaptive Tile Size")

    compressor = CWAMInspiredCompressor()

    # Low complexity (uniform gray)
    low_complex = np.full((100, 100), 128, dtype=np.uint8)
    tile_size = compressor._adaptive_tile_size(low_complex)
    assert tile_size == 32  # Coarse tiles for simple content

    # High complexity (random noise)
    high_complex = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    tile_size = compressor._adaptive_tile_size(high_complex)
    assert tile_size in [8, 16]  # Fine tiles for complex content

    print("[+] PASS: Adaptive Tile Size")


def test_compression_pipeline():
    """Test 5: Full compression pipeline"""
    print("\n[>] Test 5: Compression Pipeline")

    compressor = CWAMInspiredCompressor(quality='balanced')

    # Create test frames
    frames = create_test_frames(20, size=(200, 200))

    # Compress
    compressed = compressor.compress_frames(frames)

    # Should reduce frame count
    assert len(compressed) < len(frames)
    assert len(compressed) > 0

    # Frames should be valid
    assert all(isinstance(f, Image.Image) for f in compressed)

    print(f"[*] Reduced {len(frames)} -> {len(compressed)} frames")
    print("[+] PASS: Compression Pipeline")


def test_saliency_computation():
    """Test 6: Saliency computation with error handling"""
    print("\n[>] Test 6: Saliency Computation")

    compressor = CWAMInspiredCompressor()

    frames = create_test_frames(5, size=(100, 100))

    # Compute saliency maps
    saliency_maps = compressor._compute_cw_saliency_maps(frames)

    # Should return map for each frame
    assert len(saliency_maps) == len(frames)

    # Maps should be normalized [0, 1]
    for S in saliency_maps:
        assert S.min() >= 0.0
        assert S.max() <= 1.0

    print("[+] PASS: Saliency Computation")


def test_palette_building():
    """Test 7: Global palette with reservoir sampling (8.txt #4)"""
    print("\n[>] Test 7: Palette Building")

    compressor = CWAMInspiredCompressor()

    frames = create_test_frames(10, size=(150, 150))

    # Build palette
    palette = compressor._build_global_palette(frames, colors=128, seed=42)

    # Should be 768 elements (256 * 3 RGB)
    assert len(palette) == 768

    # All values should be in valid range
    assert all(0 <= v <= 255 for v in palette)

    # Deterministic (same seed = same palette)
    palette2 = compressor._build_global_palette(frames, colors=128, seed=42)
    assert palette == palette2

    print("[+] PASS: Palette Building")


def test_compress_to_target():
    """Test 8: Target-driven compression with enhancements"""
    print("\n[>] Test 8: Compress to Target")

    compressor = CWAMInspiredCompressor()

    frames = create_test_frames(30, size=(200, 200))

    # Compress to 1MB target
    gif_bytes, metadata = compressor.compress_to_target(
        frames,
        target_mb=1.0,
        init_colors=128,
        preserve_timing=True,
        input_fps=10
    )

    # Should produce valid GIF
    assert len(gif_bytes) > 0

    # Should meet target (or be close)
    size_mb = len(gif_bytes) / (1024 * 1024)
    print(f"[*] Target: 1.0MB, Actual: {size_mb:.3f}MB")
    assert size_mb <= 1.1  # Allow 10% tolerance

    # Metadata validation
    assert 'frames_out' in metadata
    assert 'colors' in metadata
    assert 'size_mb' in metadata
    assert 'preserve_timing_ok' in metadata

    print(f"[*] Metadata: {metadata}")
    print("[+] PASS: Compress to Target")


def test_timing_preservation():
    """Test 9: Timing preservation (REX Fix 7.2)"""
    print("\n[>] Test 9: Timing Preservation")

    compressor = CWAMInspiredCompressor()

    # Original: 50 frames at 10fps = 5 seconds = 5000ms
    orig_frames = 50
    fps_in = 10
    out_frames = 30

    durations = compressor._durations_for_preserve(orig_frames, fps_in, out_frames)

    # Should have duration for each output frame
    assert len(durations) == out_frames

    # Total should match original (±10ms tolerance)
    total_ms = sum(durations)
    expected_ms = int((orig_frames / fps_in) * 1000)

    print(f"[*] Expected: {expected_ms}ms, Actual: {total_ms}ms, Diff: {abs(total_ms - expected_ms)}ms")
    assert abs(total_ms - expected_ms) <= 10

    # All durations should be 10ms increments
    assert all(d % 10 == 0 for d in durations)

    print("[+] PASS: Timing Preservation")


def test_error_recovery():
    """Test 10: Error recovery and graceful degradation"""
    print("\n[>] Test 10: Error Recovery")

    compressor = CWAMInspiredCompressor()

    # Test with edge cases

    # Single frame
    single_frame = create_test_frames(1, size=(50, 50))
    result = compressor.compress_frames(single_frame)
    assert len(result) >= 1  # Should handle gracefully

    # Very small frames
    tiny_frames = create_test_frames(5, size=(10, 10))
    result = compressor.compress_frames(tiny_frames)
    assert len(result) >= 1

    print("[+] PASS: Error Recovery")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("FlashRecord Compression - Enhanced Edition Test Suite")
    print("="*60)

    tests = [
        test_initialization,
        test_input_validation,
        test_safe_convert,
        test_adaptive_tile_size,
        test_compression_pipeline,
        test_saliency_computation,
        test_palette_building,
        test_compress_to_target,
        test_timing_preservation,
        test_error_recovery
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[-] FAIL: {test.__name__} - {e}")
            failed += 1
        except Exception as e:
            print(f"[-] ERROR: {test.__name__} - {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
