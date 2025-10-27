#!/usr/bin/env python3
"""
FlashRecord Native Screenshot Test
@sc command execution
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from flashrecord.screenshot import take_screenshot

def main():
    """Run native screenshot"""
    print("\n" + "="*60)
    print("FlashRecord v0.2.0 - Native Screenshot Test")
    print("="*60)

    # Create output directory
    save_dir = "flashrecord-save"
    os.makedirs(save_dir, exist_ok=True)
    print(f"\n[*] Output directory: {save_dir}")

    # Take screenshot
    print("\n[>] Capturing screenshot with native implementation...")
    print(f"    Platform: {sys.platform}")

    try:
        result = take_screenshot(save_dir)

        if result:
            # Get file info
            size = os.path.getsize(result) / 1024
            filename = os.path.basename(result)
            abspath = os.path.abspath(result)

            print(f"\n[+] SUCCESS - Screenshot captured!")
            print(f"    File: {filename}")
            print(f"    Size: {size:.1f} KB")
            print(f"    Path: {abspath}")

            # List all screenshots
            print(f"\n[*] All screenshots in {save_dir}:")
            screenshots = [f for f in os.listdir(save_dir) if f.startswith("screenshot_")]
            if screenshots:
                for ss in sorted(screenshots):
                    filepath = os.path.join(save_dir, ss)
                    ss_size = os.path.getsize(filepath) / 1024
                    print(f"    - {ss} ({ss_size:.1f} KB)")
            else:
                print("    (none)")

            print("\n" + "="*60)
            print("✓ Native screenshot implementation working!")
            print("="*60 + "\n")
            return 0
        else:
            print("\n[-] FAILED - Screenshot capture returned None")
            return 1

    except Exception as e:
        print(f"\n[-] ERROR - {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
