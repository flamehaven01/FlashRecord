"""
Fine-tune to get exactly 15 frames
"""
from PIL import Image
from flashrecord.compression import CWAMInspiredCompressor

# Load previous recording (reuse frames to save time)
import glob
test_files = glob.glob("flashrecord-save/test_*frames_*.gif")
if test_files:
    print(f"[*] Loading frames from: {test_files[0]}")
    gif = Image.open(test_files[0])

    # Extract all frames
    frames = []
    for i in range(gif.n_frames):
        gif.seek(i)
        frames.append(gif.convert('RGB'))

    print(f"[+] Loaded {len(frames)} frames")

    # Test different saliency thresholds to hit 15 frames
    compressor = CWAMInspiredCompressor(quality='balanced')

    thresholds_to_test = [0.20, 0.22, 0.23, 0.24, 0.26, 0.27, 0.28]

    print("\n[>] Searching for threshold that gives ~15 frames...")
    print("="*70)

    for thr in thresholds_to_test:
        test_frames = frames.copy()

        # Process
        S = compressor._compute_cw_saliency_maps(test_frames)
        keep = compressor._keep_mask_from_saliency(S, thr=thr)
        filtered = [f for i, f in enumerate(test_frames) if keep[i]]

        print(f"  Threshold {thr:.2f}: {len(filtered):2d} frames", end="")

        if 14 <= len(filtered) <= 16:
            print(" [+] TARGET HIT!")

            # Generate full GIF
            pal = compressor._build_global_palette(filtered, colors=256, seed=1234)
            qframes = compressor._apply_global_palette(filtered, pal, dither=True)
            durations_ms = compressor._durations_for_preserve(len(frames), 10, len(qframes))
            data = compressor._encode_gif_bytes(qframes, durations_ms=durations_ms)

            size_mb = len(data) / (1024 * 1024)
            filename = f"flashrecord-save/optimal_15frames.gif"

            with open(filename, "wb") as f:
                f.write(data)

            print(f"\n[+] Saved: {filename}")
            print(f"    Frames: {len(qframes)}")
            print(f"    Size: {size_mb:.3f} MB")
            print(f"    Duration: {sum(durations_ms)}ms")
            break
        else:
            print()

    print("="*70)
else:
    print("[!] No test files found. Run test_15frames.py first.")
