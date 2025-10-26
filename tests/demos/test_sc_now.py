"""Quick test script for @sc command"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flashrecord.screenshot import take_screenshot
    from flashrecord.config import Config

    print("[*] FlashRecord @sc - Screenshot test")
    print("[*] Taking screenshot...")

    config = Config()
    result = take_screenshot(output_dir=config.save_dir)

    if result:
        file_size = os.path.getsize(result) / 1024  # KB
        print(f"[+] SUCCESS: Screenshot saved to {result}")
        print(f"[+] File size: {file_size:.1f} KB")

        # Verify file exists
        if os.path.exists(result):
            print(f"[+] File verified at: {os.path.abspath(result)}")
    else:
        print("[-] FAILED: Screenshot capture failed")

except Exception as e:
    print(f"[-] ERROR: {e}")
    import traceback
    traceback.print_exc()
