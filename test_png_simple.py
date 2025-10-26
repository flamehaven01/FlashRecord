"""
Simple PNG compression test - FlashRecord v0.3.3
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from flashrecord.screenshot import take_screenshot

print("[*] Testing PNG compression...")
print()

# Test with 1-second delays
print("[1] Default screenshot...")
r1 = take_screenshot(output_dir="flashrecord-save", compress=False)
time.sleep(1.5)

print("[2] Balanced compression...")
r2 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='balanced')
time.sleep(1.5)

print("[3] High quality compression...")
r3 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='high')
time.sleep(1.5)

print("[4] Compact compression...")
r4 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='compact')

print()
print("[*] Results:")
if r1: print(f"    Default:  {r1} ({os.path.getsize(r1)/1024:.1f} KB)")
if r2: print(f"    Balanced: {r2} ({os.path.getsize(r2)/1024:.1f} KB)")
if r3: print(f"    High:     {r3} ({os.path.getsize(r3)/1024:.1f} KB)")
if r4: print(f"    Compact:  {r4} ({os.path.getsize(r4)/1024:.1f} KB)")
print()
print("[+] Test complete")
