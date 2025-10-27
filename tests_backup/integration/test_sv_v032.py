"""
Test @sv command with v0.3.2 timing preservation
Records 5 second GIF with enhanced compression
"""

import time
from datetime import datetime
from PIL import ImageGrab
from flashrecord.compression import CWAMInspiredCompressor

# Configuration
duration = 5  # seconds
fps = 10      # frames per second

print("[>] FlashRecord @sv - Screen Recording to GIF (v0.3.2)")
print(f"[*] Recording screen for {duration} seconds at {fps}fps...")
print("[*] Press any key to start...")

# Small delay for user to prepare
time.sleep(2)

# Capture frames
frames = []
start_time = time.time()

print("[>] Recording...")
for i in range(duration * fps):
    screenshot = ImageGrab.grab()
    frames.append(screenshot)
    elapsed = time.time() - start_time
    progress = (i + 1) / (duration * fps) * 100
    print(f"\r[{'=' * int(progress / 5)}{' ' * (20 - int(progress / 5))}] {progress:.0f}% ({elapsed:.1f}s)", end='')
    time.sleep(1.0 / fps)

print()
total_time = time.time() - start_time
print(f"[+] Captured {len(frames)} frames in {total_time:.2f}s")

# Compress with v0.3.2 timing preservation
print("[>] Encoding GIF with v0.3.2 timing preservation...")
compressor = CWAMInspiredCompressor(quality='balanced')

data, meta = compressor.compress_to_target(
    frames,
    target_mb=10,
    preserve_timing=True,
    max_iterations=5,
    input_fps=fps
)

# Generate filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"flashrecord-save/screen_{timestamp}.gif"

# Save GIF
with open(filename, "wb") as f:
    f.write(data)

# Display results
print(f"\n[+] GIF saved: {filename}")
print(f"[*] File size: {meta['size_mb']:.3f} MB")
print(f"[*] Frames: {meta['orig_frames']} -> {meta['frames_out']}")
print(f"[*] Timing preserved: {'YES' if meta.get('preserve_timing_ok') else 'NO'}")
print(f"[*] Duration: {meta['total_ms']}ms (original: {len(frames) / fps * 1000:.0f}ms)")
print(f"[*] Compression: {(1 - meta['size_mb'] / (len(frames) * 0.5)) * 100:.1f}%")
