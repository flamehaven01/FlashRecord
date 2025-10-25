#!/usr/bin/env python3
"""
FlashRecord Screenshot Demo
Creates a test screenshot with embedded CLI output
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def create_demo_screenshot():
    """Create a demo screenshot showing FlashRecord CLI"""

    # Create image
    width, height = 800, 600
    background_color = (20, 20, 30)  # Dark background
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Try to use a default font
    try:
        font_large = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 14)
        font_small = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Colors
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (100, 150, 255)
    yellow = (255, 255, 0)

    # Draw title
    title = "FlashRecord v0.1.1 - CLI Demo"
    draw.text((20, 20), title, fill=blue, font=font_large)

    # Draw CLI output
    y_pos = 70
    lines = [
        ("======================================", green),
        ("FlashRecord - Fast Screen Recording  ", green),
        ("======================================", green),
        ("", white),
        ("[*] Commands: [1]start [2]stop [3]gif [4-6]save", yellow),
        ("[*] Universal: @sc=screenshot @sv=gif help exit", yellow),
        ("[*] Mode: numbered | Dir: flashrecord-save", white),
        ("", white),
        ("> @sc", blue),
        ("[+] Screenshot: flashrecord-save/screenshot_20251025_143022.png", green),
        ("", white),
        ("> 1", blue),
        ("[>] Recording started... (use '2' to stop)", yellow),
        ("[Do your work...]", white),
        ("> 2", blue),
        ("[+] Recording stopped", green),
        ("", white),
        ("> @sv", blue),
        ("[+] GIF: flashrecord-save/recording_20251025_143045.gif", green),
        ("", white),
        ("> 4", blue),
        ("[+] Saved to claude.md", green),
        ("", white),
        ("> help", blue),
        ("[*] Commands: [1]start [2]stop [3]gif [4-6]save", yellow),
        ("[*] Universal: @sc=screenshot @sv=gif help exit", yellow),
        ("", white),
        ("> exit", blue),
        ("[*] Goodbye", white),
    ]

    for text, color in lines:
        if y_pos > height - 40:
            break
        draw.text((20, y_pos), text, fill=color, font=font_small)
        y_pos += 18

    # Draw footer
    footer = f"Screenshot captured: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    draw.text((20, height - 30), footer, fill=white, font=font_small)

    # Save image
    output_dir = r"D:\Sanctum\flashrecord\flashrecord-save"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "flashrecord_demo.png")
    img.save(output_path)

    return output_path

if __name__ == "__main__":
    try:
        path = create_demo_screenshot()
        print(f"[+] Demo screenshot created: {path}")
        print(f"[+] File size: {os.path.getsize(path) / 1024:.1f} KB")
    except ImportError:
        print("[-] PIL/Pillow not installed")
        print("[*] Install with: pip install pillow")
    except Exception as e:
        print(f"[-] Error: {e}")
