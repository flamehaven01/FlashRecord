"""
Test color-corrected palette using the original purple floor screenshot
Direct comparison with known ground truth
"""
from PIL import Image
import numpy as np
from flashrecord.compression import CWAMInspiredCompressor

# Load the original purple floor screenshot
original_path = "flashrecord-save/screenshot_20251025_210856.png"
original = Image.open(original_path)

print("[>] Color Accuracy Test - Purple Floor Scene")
print(f"[*] Using original screenshot: {original_path}")
print(f"    Size: {original.size}")

# Create 10 duplicate frames (simulating 1 second of video at 10fps)
frames = [original.convert('RGB')] * 10

print(f"[*] Created {len(frames)} frames for testing")

# Test with CORRECTED palette (256 colors, saturation-weighted)
print("\n[>] Testing CORRECTED palette (256 colors, saturation-weighted)...")
compressor = CWAMInspiredCompressor(quality='balanced')

data, meta = compressor.compress_to_target(
    frames,
    target_mb=10,
    preserve_timing=True,
    max_iterations=5,
    input_fps=10
)

# Save corrected GIF
output_path = "flashrecord-save/test_color_FIXED.gif"
with open(output_path, "wb") as f:
    f.write(data)

print(f"\n[+] Saved: {output_path}")
print(f"    Size: {meta['size_mb']:.3f} MB")
print(f"    Colors: {meta['colors']}")
print(f"    Frames: {meta['frames_out']}")

# Now compare colors
print("\n[>] Analyzing color accuracy...")
gif_fixed = Image.open(output_path)
gif_fixed_rgb = gif_fixed.convert('RGB')

# Sample purple floor area
h, w = gif_fixed.size[1], gif_fixed.size[0]
floor_x, floor_y = w // 2, int(h * 0.8)

original_resized = original.resize(gif_fixed.size, Image.Resampling.LANCZOS)
orig_pixel = original_resized.getpixel((floor_x, floor_y))
fixed_pixel = gif_fixed_rgb.getpixel((floor_x, floor_y))

print(f"\nFloor color comparison (at {floor_x}, {floor_y}):")
print(f"  Original: RGB{orig_pixel}")
print(f"  Fixed GIF: RGB{fixed_pixel}")
print(f"  Difference: R{orig_pixel[0]-fixed_pixel[0]:+4d} G{orig_pixel[1]-fixed_pixel[1]:+4d} B{orig_pixel[2]-fixed_pixel[2]:+4d}")

# Check if purple is preserved (B > R, B > G)
if fixed_pixel[2] > fixed_pixel[0] and fixed_pixel[2] > fixed_pixel[1]:
    print("\n[+] SUCCESS! Purple color preserved (Blue > Red, Blue > Green)")
else:
    print("\n[!] FAILED! Color still distorted")

# Detailed palette analysis
palette = gif_fixed.getpalette()
purple_count = 0
for i in range(256):
    r, g, b = palette[i*3:i*3+3]
    # Purple: high blue, moderate red, low-moderate green
    if b > 120 and r > 80 and r < 200 and g > 60 and g < 180:
        purple_count += 1

print(f"\nPurple colors in palette: {purple_count}/256")
if purple_count > 15:
    print("[+] Good palette diversity for purple tones")
elif purple_count > 5:
    print("[~] Acceptable purple representation")
else:
    print("[!] Still insufficient purple colors")

# Compare with OLD broken version
print("\n[>] Loading OLD broken GIF for comparison...")
old_gif_path = "flashrecord-save/screen_20251025_210704.gif"
try:
    old_gif = Image.open(old_gif_path)
    old_gif_rgb = old_gif.convert('RGB')
    old_pixel = old_gif_rgb.getpixel((floor_x, floor_y))

    print(f"\nThree-way color comparison:")
    print(f"  Original:  RGB{orig_pixel}")
    print(f"  OLD (128c): RGB{old_pixel}")
    print(f"  NEW (256c): RGB{fixed_pixel}")

    # Calculate color distance (simple Euclidean)
    old_dist = np.sqrt(sum([(a-b)**2 for a, b in zip(orig_pixel, old_pixel)]))
    new_dist = np.sqrt(sum([(a-b)**2 for a, b in zip(orig_pixel, fixed_pixel)]))

    print(f"\nColor distance from original:")
    print(f"  OLD palette: {old_dist:.1f}")
    print(f"  NEW palette: {new_dist:.1f}")
    print(f"  Improvement: {((old_dist - new_dist) / old_dist * 100):.1f}%")

except Exception as e:
    print(f"[!] Could not load old GIF: {e}")

print("\n" + "="*70)
print("Color Fix Validation Complete")
print("="*70)
