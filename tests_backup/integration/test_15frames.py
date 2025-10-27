"""
Test with 15 frames output for smoother playback
Compare quality and file size
"""
import time
from datetime import datetime
from PIL import ImageGrab
from flashrecord.compression import CWAMInspiredCompressor

# Configuration
duration = 5
fps = 10

print("[>] FlashRecord - 15 Frame Test")
print(f"[*] Recording {duration}s at {fps}fps...")
time.sleep(1)

# Capture frames
frames = []
start = time.time()
print("[>] Recording...")

for i in range(duration * fps):
    screenshot = ImageGrab.grab()
    frames.append(screenshot)
    progress = (i + 1) / (duration * fps) * 100
    print(f"\r[{'=' * int(progress / 5)}{' ' * (20 - int(progress / 5))}] {progress:.0f}%", end='')
    time.sleep(1.0 / fps)

print()
elapsed = time.time() - start
print(f"[+] Captured {len(frames)} frames in {elapsed:.2f}s")

# Test different frame counts
compressor = CWAMInspiredCompressor(quality='balanced')

test_configs = [
    {"name": "Standard (10 frames)", "target_fps": 8, "saliency_thr": 0.25},
    {"name": "Smooth (15 frames)", "target_fps": 10, "saliency_thr": 0.15},
    {"name": "Ultra-smooth (20 frames)", "target_fps": 12, "saliency_thr": 0.05},
]

results = []

for config in test_configs:
    print(f"\n[>] Testing: {config['name']}")
    print(f"    Target FPS: {config['target_fps']}, Saliency threshold: {config['saliency_thr']}")

    # Modify compressor temporarily
    test_frames = frames.copy()

    # Manual processing for custom frame count
    print("[*] Resolution scaling...")
    test_frames = compressor._scale_frames(test_frames)

    print("[*] Temporal subsampling...")
    test_frames = compressor._reduce_frame_rate(test_frames, target_fps=config['target_fps'], input_fps=fps)

    print("[*] Computing saliency...")
    S = compressor._compute_cw_saliency_maps(test_frames)

    print("[*] Applying saliency filter...")
    keep = compressor._keep_mask_from_saliency(S, thr=config['saliency_thr'])
    test_frames = [f for i, f in enumerate(test_frames) if keep[i]]

    print(f"[*] Frames after filtering: {len(test_frames)}")

    # Build palette and compress
    print("[*] Building palette...")
    pal = compressor._build_global_palette(test_frames, colors=256, seed=1234)

    print("[*] Applying palette...")
    qframes = compressor._apply_global_palette(test_frames, pal, dither=True)

    print("[*] Preserving timing...")
    durations_ms = compressor._durations_for_preserve(len(frames), fps, len(qframes))

    print("[*] Encoding GIF...")
    data = compressor._encode_gif_bytes(qframes, durations_ms=durations_ms)

    size_mb = len(data) / (1024 * 1024)

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"flashrecord-save/test_{len(qframes)}frames_{timestamp}.gif"
    with open(filename, "wb") as f:
        f.write(data)

    results.append({
        "name": config['name'],
        "frames": len(qframes),
        "size_mb": size_mb,
        "duration_ms": sum(durations_ms),
        "filename": filename
    })

    print(f"[+] Saved: {filename}")
    print(f"    Size: {size_mb:.3f} MB")
    print(f"    Frames: {len(frames)} -> {len(qframes)}")
    print(f"    Duration: {sum(durations_ms)}ms")

# Summary comparison
print("\n" + "="*70)
print("COMPARISON SUMMARY")
print("="*70)

for r in results:
    print(f"\n{r['name']}:")
    print(f"  Frames: {r['frames']}")
    print(f"  Size: {r['size_mb']:.3f} MB")
    print(f"  Duration: {r['duration_ms']}ms")
    print(f"  File: {r['filename']}")

print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)

# Find best balance
best_quality = max(results, key=lambda x: x['frames'])
best_size = min(results, key=lambda x: x['size_mb'])

print(f"\nBest quality (most frames): {best_quality['name']} ({best_quality['frames']} frames)")
print(f"Best compression (smallest): {best_size['name']} ({best_size['size_mb']:.3f} MB)")

# Suggest 15 frame target
target_15 = [r for r in results if 14 <= r['frames'] <= 16]
if target_15:
    print(f"\n[+] 15-frame target achieved: {target_15[0]['name']}")
    print(f"    Perfect balance of smoothness and size!")
else:
    print(f"\n[*] To hit exactly 15 frames, adjust saliency_thr between 0.05 and 0.25")

print("="*70)
