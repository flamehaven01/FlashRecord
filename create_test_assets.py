"""
Create test assets for FlashRecord demonstration
Generates sample screenshot and tests functionality
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flashrecord.config import Config
from flashrecord.utils import get_timestamp, format_filesize

def create_test_screenshot():
    """Create a test PNG image (minimal valid PNG)"""
    config = Config()
    save_dir = config.save_dir

    # Minimal valid PNG (1x1 transparent pixel)
    png_bytes = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk start
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,  # width=1, height=1
        0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,  # bit depth, color type, CRC
        0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,  # IDAT chunk start
        0x54, 0x08, 0x99, 0x01, 0x01, 0x00, 0x00, 0xFE,  # IDAT data
        0xFF, 0x00, 0x00, 0x00, 0x00, 0xA4, 0x00, 0x00,  # IDAT data
        0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44,  # IEND chunk
        0xAE, 0x42, 0x60, 0x82                            # IEND CRC
    ])

    timestamp = get_timestamp()
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "wb") as f:
        f.write(png_bytes)

    return filepath

def create_test_gif():
    """Create a test GIF image (minimal valid GIF)"""
    config = Config()
    save_dir = config.save_dir

    # Minimal valid GIF (1x1 black pixel)
    gif_bytes = bytes([
        0x47, 0x49, 0x46, 0x38, 0x39, 0x61,  # GIF89a signature
        0x01, 0x00, 0x01, 0x00, 0x00, 0x00,  # width=1, height=1, flags
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # color table
        0x2C, 0x00, 0x00, 0x00, 0x00, 0x01,  # image descriptor
        0x00, 0x01, 0x00, 0x00, 0x02, 0x02,  # image data start
        0x4D, 0x01, 0x00, 0x3B                # image data end + GIF trailer
    ])

    timestamp = get_timestamp()
    filename = f"recording_{timestamp}.gif"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "wb") as f:
        f.write(gif_bytes)

    return filepath

def main():
    """Create test assets and display results"""
    print("\n" + "="*60)
    print("FlashRecord Test Assets Generator")
    print("="*60)

    config = Config()
    print(f"\nSave Directory: {config.save_dir}")

    # Create test screenshot
    print("\n[1] Creating test screenshot...")
    png_path = create_test_screenshot()
    png_size = os.path.getsize(png_path)
    print(f"    [+] Created: {os.path.basename(png_path)}")
    print(f"    [+] Size: {format_filesize(png_size)}")

    # Create test GIF
    print("\n[2] Creating test GIF...")
    gif_path = create_test_gif()
    gif_size = os.path.getsize(gif_path)
    print(f"    [+] Created: {os.path.basename(gif_path)}")
    print(f"    [+] Size: {format_filesize(gif_size)}")

    # Verify files
    print("\n[3] Verifying files...")
    png_exists = os.path.exists(png_path)
    gif_exists = os.path.exists(gif_path)
    print(f"    PNG exists: {png_exists}")
    print(f"    GIF exists: {gif_exists}")

    # List all files in save directory
    print("\n[4] Files in save directory:")
    if os.path.exists(config.save_dir):
        files = os.listdir(config.save_dir)
        for filename in sorted(files):
            filepath = os.path.join(config.save_dir, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                print(f"    - {filename} ({format_filesize(size)})")

    print("\n" + "="*60)
    print("Test Assets Created Successfully!")
    print("="*60 + "\n")

    return png_path, gif_path

if __name__ == "__main__":
    main()
