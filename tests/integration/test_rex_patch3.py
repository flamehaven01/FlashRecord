"""Test REX Engine Patch 3: Global Palette + Target Size Feedback Loop"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flashrecord.screen_recorder import record_screen_to_gif
from flashrecord.compression import CWAMInspiredCompressor
from flashrecord.config import Config
from PIL import Image

print("[*] REX Engine Patch 3 Test")
print("[*] Testing Global Palette + Target Size Feedback Loop")
print("[*] Recording 5 seconds...")

config = Config()

# Record frames (without built-in compression)
import time
import threading
import numpy as np
from PIL import ImageGrab

frames = []
duration = 5
fps = 10

def capture_frames():
    global frames
    for i in range(duration * fps):
        screenshot = ImageGrab.grab()
        frames.append(screenshot)
        time.sleep(1.0 / fps)

print("[>] Capturing frames...")
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()
capture_thread.join()

print(f"[+] Captured {len(frames)} frames")

# Test compress_to_target with different target sizes
compressor = CWAMInspiredCompressor(quality='balanced')

targets = [5, 3, 1]  # Test 5MB, 3MB, 1MB targets

for target_mb in targets:
    print(f"\n[*] Testing target: {target_mb} MB")
    data, meta = compressor.compress_to_target(frames, target_mb=target_mb)

    # Save to file
    output_path = os.path.join(config.save_dir, f"rex_patch3_{target_mb}mb.gif")
    with open(output_path, "wb") as f:
        f.write(data)

    print(f"[+] Result: {meta}")
    print(f"[+] Saved: {output_path}")
    print(f"[+] Actual size: {meta['size_mb']} MB")

    # Check if target was met
    if meta['size_mb'] <= target_mb:
        print(f"[+] TARGET MET! ({meta['size_mb']} MB <= {target_mb} MB)")
    else:
        print(f"[-] Target missed ({meta['size_mb']} MB > {target_mb} MB)")
