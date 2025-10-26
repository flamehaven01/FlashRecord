"""Test KAIROS-inspired compression on FlashRecord GIF"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flashrecord.screen_recorder import record_screen_to_gif
from flashrecord.config import Config

print("[*] FlashRecord Compression Test")
print("[*] Testing KAIROS-inspired compression")
print("[*] Recording 5 seconds with 'balanced' compression...")

config = Config()

# Record with compression
result = record_screen_to_gif(
    duration=5,
    fps=10,
    output_dir=config.save_dir,
    compression='balanced'  # Use KAIROS-inspired compression
)

if result:
    file_size = os.path.getsize(result) / (1024 * 1024)  # MB
    print(f"\n[+] SUCCESS: Compressed GIF saved")
    print(f"[+] File: {result}")
    print(f"[+] Size: {file_size:.1f} MB")

    # Compare with previous test
    print(f"\n[*] Comparison:")
    print(f"[*] Previous (no compression): 25.6 MB")
    print(f"[*] Current (balanced): {file_size:.1f} MB")

    if file_size < 25.6:
        reduction = ((25.6 - file_size) / 25.6) * 100
        print(f"[+] Compression success: {reduction:.1f}% reduction!")

    if os.path.exists(result):
        print(f"[+] File verified at: {os.path.abspath(result)}")
else:
    print("[-] FAILED: GIF recording with compression failed")
