"""Check GIF color palette and compare with original screenshot"""
from PIL import Image, ImageGrab
import numpy as np

# Check generated GIF
gif_path = "flashrecord-save/screen_20251025_205959.gif"
gif = Image.open(gif_path)

print(f"[*] GIF Analysis: {gif_path}")
print(f"    Mode: {gif.mode}")
print(f"    Size: {gif.size}")
print(f"    Frames: {gif.n_frames}")

# Get palette
palette = gif.getpalette()
if palette:
    print(f"    Palette length: {len(palette)}")
    print(f"    First 10 RGB colors:")
    for i in range(10):
        r, g, b = palette[i*3:i*3+3]
        print(f"      Color {i}: RGB({r:3d}, {g:3d}, {b:3d})")

# Capture current screen for comparison
print("\n[*] Capturing current screen for comparison...")
current_screen = ImageGrab.grab()
current_screen = current_screen.resize(gif.size)  # Match GIF size

# Convert both to RGB for comparison
gif_rgb = gif.convert('RGB')
current_rgb = current_screen.convert('RGB')

# Sample some pixel colors
print("\n[*] Sample pixel comparison (center of image):")
h, w = gif.size[1], gif.size[0]
for i in range(5):
    x = w // 2 + i * 50
    y = h // 2

    gif_pixel = gif_rgb.getpixel((x, y))
    screen_pixel = current_rgb.getpixel((x, y))

    print(f"    Pixel ({x}, {y}):")
    print(f"      GIF:    RGB{gif_pixel}")
    print(f"      Screen: RGB{screen_pixel}")

# Analyze overall color distribution
print("\n[*] Color distribution analysis:")
gif_arr = np.array(gif_rgb)
print(f"    GIF RGB means: R={gif_arr[:,:,0].mean():.1f}, G={gif_arr[:,:,1].mean():.1f}, B={gif_arr[:,:,2].mean():.1f}")

# Check if there's excessive red/orange bias
r_mean = gif_arr[:,:,0].mean()
g_mean = gif_arr[:,:,1].mean()
b_mean = gif_arr[:,:,2].mean()

if r_mean > g_mean * 1.2 and r_mean > b_mean * 1.2:
    print("[!] WARNING: Excessive red channel bias detected!")
    print(f"    Red is {r_mean/g_mean:.2f}x green and {r_mean/b_mean:.2f}x blue")
else:
    print("[+] Color balance looks normal")

# Save first frame as PNG for comparison
gif.save("flashrecord-save/gif_frame0.png")
print("\n[+] Saved first frame as gif_frame0.png for inspection")
