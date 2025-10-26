"""Quick test script for @sv command - Auto mode only"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flashrecord.screen_recorder import record_screen_to_gif
    from flashrecord.config import Config

    print("[*] FlashRecord @sv - Screen Recording test (Auto mode)")
    print("[*] Recording for 5 seconds at 10 fps...")

    config = Config()
    result = record_screen_to_gif(
        duration=5,
        fps=10,
        output_dir=config.save_dir
    )

    if result:
        file_size = os.path.getsize(result) / (1024 * 1024)  # MB
        print(f"\n[+] SUCCESS: GIF saved to {result}")
        print(f"[+] File size: {file_size:.1f} MB")

        # Verify file exists
        if os.path.exists(result):
            print(f"[+] File verified at: {os.path.abspath(result)}")
    else:
        print("[-] FAILED: GIF recording failed")

except Exception as e:
    print(f"[-] ERROR: {e}")
    import traceback
    traceback.print_exc()
