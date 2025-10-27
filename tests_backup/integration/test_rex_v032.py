"""
Test REX Engine v0.3.2: Timing Preservation Enhancement

Validates:
1. preserve_timing=True maintains original total playback duration
2. max_iterations extended to 5 for aggressive targets
3. Enhanced metadata with timing verification
4. durations_ms list sums to total_ms within ±10ms tolerance
"""

import time
from PIL import ImageGrab
from flashrecord.compression import CWAMInspiredCompressor

# Test configuration
duration = 5  # seconds
fps = 10      # frames per second
target_sizes = [5, 3, 1]  # MB

print("[>] REX Engine v0.3.2 Timing Preservation Test")
print(f"[*] Recording {duration}s at {fps}fps...")

# Capture frames
frames = []
start = time.time()
for i in range(duration * fps):
    screenshot = ImageGrab.grab()
    frames.append(screenshot)
    time.sleep(1.0 / fps)
elapsed = time.time() - start

print(f"[+] Captured {len(frames)} frames in {elapsed:.2f}s")
print(f"[*] Original total time: {len(frames) / fps * 1000:.0f}ms")

# Initialize compressor
compressor = CWAMInspiredCompressor(quality='balanced')

# Test different target sizes with timing preservation
for target_mb in target_sizes:
    print(f"\n[>] Testing target: {target_mb}MB with preserve_timing=True")

    data, meta = compressor.compress_to_target(
        frames,
        target_mb=target_mb,
        preserve_timing=True,
        max_iterations=5,
        input_fps=fps
    )

    # Validation
    orig_total_ms = int((len(frames) / fps) * 1000)
    timing_ok = meta.get('preserve_timing_ok', False)

    print(f"\n[+] Results for {target_mb}MB target:")
    print(f"    Iterations: {meta['iteration']}/{meta.get('max_iterations', 5)}")
    print(f"    Size: {meta['size_mb']:.4f}MB")
    print(f"    Frames: {meta['orig_frames']} -> {meta['frames_out']}")
    print(f"    Colors: {meta['colors']}")
    print(f"    Original total: {orig_total_ms}ms")
    print(f"    Output total: {meta['total_ms']}ms")
    print(f"    Timing preserved: {'YES' if timing_ok else 'NO'}")
    print(f"    Drift: {abs(orig_total_ms - meta['total_ms'])}ms")

    # Write GIF
    output_path = f"flashrecord-save/rex_v032_{target_mb}mb.gif"
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"[+] Saved: {output_path}")

    # Assertions from REX Engine 6.txt
    assert timing_ok, f"Timing preservation failed! Drift: {abs(orig_total_ms - meta['total_ms'])}ms"
    assert sum(meta['durations_ms']) == meta['total_ms'], "Durations sum mismatch"
    assert abs(orig_total_ms - meta['total_ms']) <= 10, "Total time drift > 10ms"

print("\n[+] All v0.3.2 validation checks passed!")
print("[*] Visual test: Compare playback speed with original recording")
