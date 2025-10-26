"""
Create exactly 15-frame GIF by evenly sampling from 50 frames
"""
from PIL import Image
from flashrecord.compression import CWAMInspiredCompressor
import numpy as np

# Load 50-frame GIF
gif_path = "flashrecord-save/test_50frames_20251025_211918.gif"
gif = Image.open(gif_path)

print(f"[*] Loading: {gif_path}")
print(f"    Total frames: {gif.n_frames}")

# Extract all frames
frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frames.append(gif.convert('RGB'))

print(f"[+] Loaded {len(frames)} frames")

# Select exactly 15 frames evenly distributed
target_frames = 15
indices = np.linspace(0, len(frames)-1, target_frames, dtype=int)
selected_frames = [frames[i] for i in indices]

print(f"\n[*] Selected {len(selected_frames)} frames:")
print(f"    Indices: {list(indices)}")

# Compress with 256-color palette
compressor = CWAMInspiredCompressor(quality='balanced')

print("\n[>] Generating 15-frame GIF...")
print("[*] Building palette...")
pal = compressor._build_global_palette(selected_frames, colors=256, seed=1234)

print("[*] Applying palette...")
qframes = compressor._apply_global_palette(selected_frames, pal, dither=True)

print("[*] Preserving timing (5000ms total)...")
durations_ms = compressor._durations_for_preserve(50, 10, len(qframes))

print("[*] Encoding...")
data = compressor._encode_gif_bytes(qframes, durations_ms=durations_ms)

size_mb = len(data) / (1024 * 1024)

# Save
output_path = "flashrecord-save/smooth_15frames.gif"
with open(output_path, "wb") as f:
    f.write(data)

print(f"\n[+] SUCCESS!")
print(f"    Saved: {output_path}")
print(f"    Frames: {len(qframes)}")
print(f"    Size: {size_mb:.3f} MB")
print(f"    Duration: {sum(durations_ms)}ms")
print(f"    Per-frame: {sum(durations_ms)/len(qframes):.0f}ms avg")

# Compare with 10-frame version
print("\n[>] Comparison with 10-frame version:")
print(f"    10 frames: ~1.0 MB")
print(f"    15 frames: {size_mb:.3f} MB ({size_mb/1.0:.1f}x size)")
print(f"    Smoothness gain: {(15/10-1)*100:.0f}% more frames")
