"""
Diagnose color shift issue between original screenshot and GIF
Compare original PNG with GIF to identify palette generation problem
"""
from PIL import Image
import numpy as np

# Load original screenshot and GIF
original_path = "flashrecord-save/screenshot_20251025_210856.png"
gif_path = "flashrecord-save/screen_20251025_210704.gif"

original = Image.open(original_path)
gif = Image.open(gif_path)

print("=" * 70)
print("COLOR ACCURACY DIAGNOSTIC")
print("=" * 70)

# Resize original to match GIF size for fair comparison
original_resized = original.resize(gif.size, Image.Resampling.LANCZOS)

# Convert both to RGB
original_rgb = original_resized.convert('RGB')
gif_rgb = gif.convert('RGB')

# Get numpy arrays
orig_arr = np.array(original_rgb)
gif_arr = np.array(gif_rgb)

print("\n[1] OVERALL COLOR STATISTICS")
print("-" * 70)

print("\nOriginal Screenshot (PNG):")
print(f"  Red   mean: {orig_arr[:,:,0].mean():.1f}  std: {orig_arr[:,:,0].std():.1f}")
print(f"  Green mean: {orig_arr[:,:,1].mean():.1f}  std: {orig_arr[:,:,1].std():.1f}")
print(f"  Blue  mean: {orig_arr[:,:,2].mean():.1f}  std: {orig_arr[:,:,2].std():.1f}")

print("\nGIF Output:")
print(f"  Red   mean: {gif_arr[:,:,0].mean():.1f}  std: {gif_arr[:,:,0].std():.1f}")
print(f"  Green mean: {gif_arr[:,:,1].mean():.1f}  std: {gif_arr[:,:,1].std():.1f}")
print(f"  Blue  mean: {gif_arr[:,:,2].mean():.1f}  std: {gif_arr[:,:,2].std():.1f}")

print("\nColor Shift:")
r_shift = orig_arr[:,:,0].mean() - gif_arr[:,:,0].mean()
g_shift = orig_arr[:,:,1].mean() - gif_arr[:,:,1].mean()
b_shift = orig_arr[:,:,2].mean() - gif_arr[:,:,2].mean()

print(f"  Red   shift: {r_shift:+.1f}")
print(f"  Green shift: {g_shift:+.1f}")
print(f"  Blue  shift: {b_shift:+.1f}")

print("\n[2] SAMPLE PIXEL COMPARISON (Floor area - should be PURPLE)")
print("-" * 70)

# Sample floor area (bottom center)
h, w = gif.size[1], gif.size[0]
floor_samples = [
    (w//2, int(h*0.8)),
    (w//2 + 50, int(h*0.8)),
    (w//2 - 50, int(h*0.8)),
    (w//2, int(h*0.85)),
    (w//2, int(h*0.75))
]

for i, (x, y) in enumerate(floor_samples):
    orig_pixel = original_rgb.getpixel((x, y))
    gif_pixel = gif_rgb.getpixel((x, y))

    print(f"\nFloor pixel {i+1} at ({x}, {y}):")
    print(f"  Original: RGB{orig_pixel}")
    print(f"  GIF:      RGB{gif_pixel}")
    print(f"  Diff:     R{orig_pixel[0]-gif_pixel[0]:+4d} G{orig_pixel[1]-gif_pixel[1]:+4d} B{orig_pixel[2]-gif_pixel[2]:+4d}")

print("\n[3] PALETTE ANALYSIS")
print("-" * 70)

palette = gif.getpalette()
print(f"\nGIF palette (first 20 colors):")
for i in range(20):
    r, g, b = palette[i*3:i*3+3]
    print(f"  Color {i:2d}: RGB({r:3d}, {g:3d}, {b:3d})", end="")

    # Check if this looks like purple
    if b > r and b > g and r > 80:
        print(" [Possible purple]")
    elif b > 150 and r > 80 and g > 80:
        print(" [Light purple/violet]")
    else:
        print()

print("\n[4] PURPLE COLOR DETECTION")
print("-" * 70)

# Check if purple colors exist in palette
purple_count = 0
for i in range(128):
    r, g, b = palette[i*3:i*3+3]
    # Purple: high blue, moderate red, low-moderate green
    if b > 120 and r > 80 and r < 200 and g > 60 and g < 180:
        purple_count += 1

print(f"\nPurple-like colors in palette: {purple_count}/128")

if purple_count < 5:
    print("[!] WARNING: Very few purple colors in palette!")
    print("    This suggests palette generation is missing purple tones.")

print("\n[5] ROOT CAUSE ANALYSIS")
print("-" * 70)

# Check brightness shift
orig_brightness = (orig_arr[:,:,0].mean() + orig_arr[:,:,1].mean() + orig_arr[:,:,2].mean()) / 3
gif_brightness = (gif_arr[:,:,0].mean() + gif_arr[:,:,1].mean() + gif_arr[:,:,2].mean()) / 3

print(f"\nBrightness comparison:")
print(f"  Original: {orig_brightness:.1f}")
print(f"  GIF:      {gif_brightness:.1f}")
print(f"  Loss:     {orig_brightness - gif_brightness:.1f} ({(1 - gif_brightness/orig_brightness)*100:.1f}%)")

if gif_brightness < orig_brightness * 0.7:
    print("\n[!] CRITICAL: Significant brightness loss detected!")
    print("    Possible causes:")
    print("    1. Palette sampling bias towards darker pixels")
    print("    2. MEDIANCUT algorithm not preserving bright colors")
    print("    3. Floyd-Steinberg dithering darkening effect")

print("\n[6] RECOMMENDATION")
print("-" * 70)
print("\nPossible fixes:")
print("  1. Increase palette size from 128 to 256 colors")
print("  2. Add brightness preservation in palette generation")
print("  3. Use weighted sampling favoring bright/saturated colors")
print("  4. Try alternative quantization: MAXCOVERAGE or FASTOCTREE")
print("  5. Disable dithering to see if it's causing darkening")

# Save side-by-side comparison
comparison = Image.new('RGB', (w*2, h))
comparison.paste(original_rgb, (0, 0))
comparison.paste(gif_rgb, (w, 0))
comparison.save("flashrecord-save/color_comparison.png")

print("\n[+] Saved side-by-side comparison: flashrecord-save/color_comparison.png")
print("=" * 70)
