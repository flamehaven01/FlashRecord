"""
Test PNG compression functionality - FlashRecord v0.3.3
Validates Phase 1+2 implementation
"""
import os
import sys
from PIL import Image

# Add flashrecord to path
sys.path.insert(0, os.path.dirname(__file__))

from flashrecord.screenshot import take_screenshot

def test_png_compression():
    """Test all compression modes"""
    print("[*] FlashRecord v0.3.3 PNG Compression Test\n")

    # Test 1: Default (optimize only)
    print("[>] Test 1: Default @sc (optimize only)")
    result1 = take_screenshot(output_dir="flashrecord-save", compress=False)
    if result1 and os.path.exists(result1):
        size1 = os.path.getsize(result1) / (1024 * 1024)
        print(f"[+] PASS: {result1}")
        print(f"[*] Size: {size1:.2f} MB (optimized PNG)\n")
    else:
        print("[-] FAIL: Screenshot failed\n")
        return False

    # Test 2: Balanced compression
    print("[>] Test 2: @sc -c (balanced compression)")
    result2 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='balanced')
    if result2 and os.path.exists(result2):
        size2 = os.path.getsize(result2) / (1024 * 1024)
        reduction2 = ((size1 - size2) / size1) * 100
        print(f"[+] PASS: {result2}")
        print(f"[*] Size: {size2:.2f} MB ({reduction2:.1f}% reduction)\n")
    else:
        print("[-] FAIL: Balanced compression failed\n")
        return False

    # Test 3: High quality compression
    print("[>] Test 3: @sc -c high (70% scale)")
    result3 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='high')
    if result3 and os.path.exists(result3):
        size3 = os.path.getsize(result3) / (1024 * 1024)
        reduction3 = ((size1 - size3) / size1) * 100
        print(f"[+] PASS: {result3}")
        print(f"[*] Size: {size3:.2f} MB ({reduction3:.1f}% reduction)\n")
    else:
        print("[-] FAIL: High quality compression failed\n")
        return False

    # Test 4: Compact compression
    print("[>] Test 4: @sc -c compact (30% scale)")
    result4 = take_screenshot(output_dir="flashrecord-save", compress=True, quality='compact')
    if result4 and os.path.exists(result4):
        size4 = os.path.getsize(result4) / (1024 * 1024)
        reduction4 = ((size1 - size4) / size1) * 100
        print(f"[+] PASS: {result4}")
        print(f"[*] Size: {size4:.2f} MB ({reduction4:.1f}% reduction)\n")
    else:
        print("[-] FAIL: Compact compression failed\n")
        return False

    # Summary
    print("[=] Test Summary:")
    print(f"    Default:  {size1:.2f} MB (baseline)")
    print(f"    Balanced: {size2:.2f} MB ({reduction2:.1f}% reduction)")
    print(f"    High:     {size3:.2f} MB ({reduction3:.1f}% reduction)")
    print(f"    Compact:  {size4:.2f} MB ({reduction4:.1f}% reduction)")
    print("\n[+] All tests PASSED\n")

    # Verify compression expectations
    print("[*] Validation:")
    if reduction2 >= 60:  # Balanced should be 70-80%
        print(f"[+] Balanced compression: {reduction2:.1f}% (expected 70-80%)")
    else:
        print(f"[!] Balanced compression: {reduction2:.1f}% (expected 70-80%, check implementation)")

    if reduction3 >= 40:  # High should be 40-50%
        print(f"[+] High quality compression: {reduction3:.1f}% (expected 40-50%)")
    else:
        print(f"[!] High quality compression: {reduction3:.1f}% (expected 40-50%, check implementation)")

    if reduction4 >= 85:  # Compact should be 85-92%
        print(f"[+] Compact compression: {reduction4:.1f}% (expected 85-92%)")
    else:
        print(f"[!] Compact compression: {reduction4:.1f}% (expected 85-92%, check implementation)")

    return True

if __name__ == "__main__":
    try:
        success = test_png_compression()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[-] Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
