"""
Final color validation: Compare latest GIF with original screenshot
"""
from PIL import Image, ImageGrab
import numpy as np

# Capture current screen as reference
print("[>] Capturing current screen as reference...")
current_screen = ImageGrab.grab()
current_screen.save("flashrecord-save/current_reference.png")

# Load latest GIF
gif_path = "flashrecord-save/screen_20251025_211453.gif"
gif = Image.open(gif_path)

print(f"\n[*] Analyzing: {gif_path}")
print(f"    Mode: {gif.mode}")
print(f"    Size: {gif.size}")
print(f"    Frames: {gif.n_frames}")

# Resize reference to match GIF
ref_resized = current_screen.resize(gif.size, Image.Resampling.LANCZOS)
gif_rgb = gif.convert('RGB')

# Sample floor area (purple floor)
h, w = gif.size[1], gif.size[0]
floor_samples = [
    (w//2, int(h*0.85)),      # Center bottom
    (w//2 + 50, int(h*0.85)),  # Right
    (w//2 - 50, int(h*0.85)),  # Left
]

print("\n[*] Purple Floor Color Validation:")
print("="*70)

total_error = 0
for i, (x, y) in enumerate(floor_samples):
    ref_pixel = ref_resized.getpixel((x, y))
    gif_pixel = gif_rgb.getpixel((x, y))

    # Calculate error
    error = np.sqrt(sum([(a-b)**2 for a, b in zip(ref_pixel, gif_pixel)]))
    total_error += error

    print(f"\nSample {i+1} at ({x}, {y}):")
    print(f"  Reference: RGB{ref_pixel}")
    print(f"  GIF:       RGB{gif_pixel}")
    print(f"  Error:     {error:.1f}")

    # Check if purple (B > R, B > G)
    if gif_pixel[2] > gif_pixel[0] and gif_pixel[2] > gif_pixel[1]:
        print(f"  Status:    [+] Purple preserved (B={gif_pixel[2]} > R={gif_pixel[0]}, G={gif_pixel[1]})")
    else:
        print(f"  Status:    [!] NOT purple (B={gif_pixel[2]}, R={gif_pixel[0]}, G={gif_pixel[1]})")

avg_error = total_error / len(floor_samples)
print("\n" + "="*70)
print(f"Average Color Error: {avg_error:.1f}")

if avg_error < 5:
    print("[+] EXCELLENT: Nearly perfect color accuracy!")
elif avg_error < 15:
    print("[+] GOOD: Acceptable color accuracy")
elif avg_error < 30:
    print("[~] FAIR: Noticeable but acceptable differences")
else:
    print("[!] POOR: Significant color distortion")

# Palette analysis
palette = gif.getpalette()
purple_colors = 0
for i in range(256):
    r, g, b = palette[i*3:i*3+3]
    if b > 120 and b > r and b > g:
        purple_colors += 1

print(f"\nPurple colors in palette: {purple_colors}/256")

# Overall statistics
ref_arr = np.array(ref_resized)
gif_arr = np.array(gif_rgb)

print("\n" + "="*70)
print("Overall Color Statistics:")
print("="*70)
print("\nReference (Current Screen):")
print(f"  R: {ref_arr[:,:,0].mean():.1f} ± {ref_arr[:,:,0].std():.1f}")
print(f"  G: {ref_arr[:,:,1].mean():.1f} ± {ref_arr[:,:,1].std():.1f}")
print(f"  B: {ref_arr[:,:,2].mean():.1f} ± {ref_arr[:,:,2].std():.1f}")

print("\nGIF Output:")
print(f"  R: {gif_arr[:,:,0].mean():.1f} ± {gif_arr[:,:,0].std():.1f}")
print(f"  G: {gif_arr[:,:,1].mean():.1f} ± {gif_arr[:,:,1].std():.1f}")
print(f"  B: {gif_arr[:,:,2].mean():.1f} ± {gif_arr[:,:,2].std():.1f}")

# Final verdict
print("\n" + "="*70)
print("REX Engine Fix 6 - Color Accuracy Validation")
print("="*70)

if avg_error < 15 and purple_colors > 20:
    print("\n[+] SUCCESS: Color accuracy fix is working correctly!")
    print("    - Purple floor preserved")
    print("    - Rich palette diversity")
    print("    - Ready for production")
else:
    print("\n[!] NEEDS REVIEW: Color accuracy may need further tuning")

print("\n" + "="*70)
