"""
Test REX Engine Fix 7.1 and 7.2 improvements

Fix 7.1: Accumulated Rescaling Artifacts
- Store original frames
- Always rescale from original, not from previous scaled version
- Expected: Better text/edge sharpness during aggressive compression

Fix 7.2: Drift Distribution
- Distribute timing drift across first N frames
- Expected: Smoother playback without last-frame stutter
"""
from PIL import Image
from flashrecord.compression import CWAMInspiredCompressor
import glob

# Load previous test recording (50 frames)
test_files = glob.glob("flashrecord-save/test_*frames_*.gif")
if not test_files:
    print("[!] No test GIF found. Run @sv first.")
    exit(1)

print(f"[*] Loading: {test_files[0]}")
gif = Image.open(test_files[0])

# Extract all frames
frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frames.append(gif.convert('RGB'))

print(f"[+] Loaded {len(frames)} frames")

# Test aggressive compression scenario (target 1MB)
print("\n[>] Testing REX Fix 7.1 + 7.2 with aggressive 1MB target...")
compressor = CWAMInspiredCompressor(quality='balanced')

data, meta = compressor.compress_to_target(
    frames,
    target_mb=1.0,
    init_colors=256,
    preserve_timing=True,
    max_iterations=5,
    input_fps=10
)

size_mb = len(data) / (1024 * 1024)

# Save output
output_path = "flashrecord-save/rex_fix7_1mb.gif"
with open(output_path, "wb") as f:
    f.write(data)

print(f"\n[+] SUCCESS!")
print(f"    Saved: {output_path}")
print(f"    Size: {size_mb:.3f} MB")
print(f"    Frames: {meta['frames_out']}")
print(f"    Iterations: {meta['iteration']}")
print(f"    Colors: {meta['colors']}")
print(f"    Total duration: {meta['total_ms']}ms")
print(f"    Timing preserved: {meta.get('preserve_timing_ok', False)}")

# Analyze timing distribution (Fix 7.2 verification)
print(f"\n[>] Fix 7.2 Drift Distribution Analysis:")
durs = meta['durations_ms']
print(f"    Frame durations (ms): {durs[:5]}... {durs[-3:]}")
print(f"    Average: {sum(durs) / len(durs):.1f}ms")
print(f"    Std dev: {(sum((d - sum(durs)/len(durs))**2 for d in durs) / len(durs))**0.5:.1f}ms")

# Check if drift is distributed (not just on last frame)
first_5_deviation = sum(abs(d - durs[0]) for d in durs[:5])
last_frame_deviation = abs(durs[-1] - durs[0])

if first_5_deviation > 0:
    print(f"    [+] Drift distributed across first frames: {first_5_deviation}ms total")
else:
    print(f"    [-] Drift NOT distributed, concentrated on last frame: {last_frame_deviation}ms")

print(f"\n[*] Expected improvements:")
print(f"    - Text/edges sharper (Fix 7.1: no accumulated rescaling)")
print(f"    - Smoother playback (Fix 7.2: distributed timing)")
print(f"\n[*] Visual verification required:")
print(f"    Compare {output_path} with previous aggressive compressions")
