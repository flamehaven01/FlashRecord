"""
Comprehensive test for REX Engine Fix 7.1 and 7.2
Uses 50-frame source for better drift distribution testing
"""
from PIL import Image
from flashrecord.compression import CWAMInspiredCompressor
import glob

# Load 50-frame test file
test_files = glob.glob("flashrecord-save/test_50frames_*.gif")
if not test_files:
    print("[!] No 50-frame test GIF found.")
    print("[*] Creating 50-frame test GIF from available source...")

    # Try to load any available GIF
    any_gifs = glob.glob("flashrecord-save/*.gif")
    if not any_gifs:
        print("[!] No GIF files found. Run @sv first.")
        exit(1)

    # Load and duplicate frames to get 50 frames
    gif = Image.open(any_gifs[0])
    frames = []
    for i in range(gif.n_frames):
        gif.seek(i)
        frames.append(gif.convert('RGB'))

    # Duplicate to reach 50 frames
    while len(frames) < 50:
        frames.extend([f.copy() for f in frames[:min(50-len(frames), len(frames))]])

    frames = frames[:50]
    print(f"[+] Created 50-frame test set")
else:
    print(f"[*] Loading: {test_files[0]}")
    gif = Image.open(test_files[0])
    frames = []
    for i in range(gif.n_frames):
        gif.seek(i)
        frames.append(gif.convert('RGB'))
    print(f"[+] Loaded {len(frames)} frames")

# Test 1: Moderate compression (15 frames target)
print("\n[>] Test 1: Moderate compression (targeting ~15 frames)...")
compressor1 = CWAMInspiredCompressor(quality='balanced')

# Manually control to get ~15 frames
compressor1.scale_factor = 0.5
frames_scaled = compressor1._scale_frames(frames)
frames_temporal = compressor1._reduce_frame_rate(frames_scaled, target_fps=8, input_fps=10)
S = compressor1._compute_cw_saliency_maps(frames_temporal)
keep = compressor1._keep_mask_from_saliency(S, thr=0.20)
frames_filtered = [f for i, f in enumerate(frames_temporal) if keep[i]]

print(f"[*] Filtered to {len(frames_filtered)} frames")

pal = compressor1._build_global_palette(frames_filtered, colors=256, seed=1234)
qframes = compressor1._apply_global_palette(frames_filtered, pal, dither=True)

# Generate timing with Fix 7.2
durations = compressor1._durations_for_preserve(50, 10, len(qframes))
data = compressor1._encode_gif_bytes(qframes, durations_ms=durations)

size_mb = len(data) / (1024 * 1024)

# Save
output_path = "flashrecord-save/rex_fix7_15frames.gif"
with open(output_path, "wb") as f:
    f.write(data)

print(f"\n[+] Test 1 Results:")
print(f"    Saved: {output_path}")
print(f"    Size: {size_mb:.3f} MB")
print(f"    Frames: {len(qframes)}")
print(f"    Total duration: {sum(durations)}ms (expected: 5000ms)")

# Analyze drift distribution
print(f"\n[*] Fix 7.2 Drift Distribution Analysis:")
print(f"    Frame durations (first 5): {durations[:5]}")
print(f"    Frame durations (last 3): {durations[-3:]}")

# Count unique durations
unique_durs = set(durations)
print(f"    Unique duration values: {len(unique_durs)}")
print(f"    Values: {sorted(unique_durs)}")

# Check if drift is distributed
first_3_range = max(durations[:3]) - min(durations[:3])
if first_3_range > 0:
    print(f"    [+] SUCCESS - Drift distributed across first frames (range: {first_3_range}ms)")
else:
    print(f"    [-] Drift not visible in first 3 frames")

# Test 2: Aggressive compression with multiple iterations
print(f"\n[>] Test 2: Aggressive compression (1.5MB target, multiple iterations)...")
compressor2 = CWAMInspiredCompressor(quality='balanced')

data2, meta2 = compressor2.compress_to_target(
    frames,
    target_mb=1.5,
    init_colors=256,
    preserve_timing=True,
    max_iterations=5,
    input_fps=10
)

size_mb2 = len(data2) / (1024 * 1024)

output_path2 = "flashrecord-save/rex_fix7_aggressive.gif"
with open(output_path2, "wb") as f:
    f.write(data2)

print(f"\n[+] Test 2 Results:")
print(f"    Saved: {output_path2}")
print(f"    Size: {size_mb2:.3f} MB")
print(f"    Frames: {meta2['frames_out']}")
print(f"    Iterations: {meta2['iteration']}")
print(f"    Final colors: {meta2['colors']}")
print(f"    Total duration: {meta2['total_ms']}ms")
print(f"    Timing preserved: {meta2.get('preserve_timing_ok', False)}")

durs2 = meta2['durations_ms']
print(f"\n[*] Timing analysis:")
print(f"    First 5 durations: {durs2[:5]}")
print(f"    Last 3 durations: {durs2[-3:]}")
print(f"    Unique values: {len(set(durs2))}")

print(f"\n[*] Key improvements from Fix 7.1 + 7.2:")
print(f"    1. Fix 7.1: No accumulated rescaling blur (sharper text/edges)")
print(f"    2. Fix 7.2: Smooth timing (no last-frame stutter)")
print(f"\n[*] Visual verification needed:")
print(f"    - Check {output_path} for text clarity")
print(f"    - Check both GIFs for smooth playback without stuttering")
