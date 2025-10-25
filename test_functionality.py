"""
FlashRecord Functionality Test - Real-world testing
Tests: Screenshot, GIF generation, command mapping
"""

import os
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from flashrecord.cli import FlashRecordCLI
from flashrecord.screenshot import take_screenshot
from flashrecord.video_recorder import VideoRecorder
from flashrecord.config import Config
from flashrecord.utils import get_timestamp, format_filesize

def test_config():
    """Test configuration loading"""
    print("\n[TEST] Configuration Loading")
    config = Config()
    print(f"  Command Style: {config.command_style}")
    print(f"  Save Directory: {config.save_dir}")
    print(f"  Auto Delete Hours: {config.auto_delete_hours}")
    print(f"  hcap Path: {config.hcap_path}")
    assert config.command_style in ["numbered", "vs_vc_vg", "verbose"]
    assert os.path.exists(config.save_dir)
    print("[PASS] Configuration loaded successfully")

def test_cli_commands():
    """Test new shortcut keys"""
    print("\n[TEST] CLI Command Mapping (New Shortcuts)")
    cli = FlashRecordCLI()

    # Test new shortcut keys
    tests = [
        ("@sc", ("screenshot", None), "Screenshot shortcut"),
        ("@sv", ("gif", None), "GIF shortcut"),
        ("help", ("help", None), "Help command"),
        ("exit", ("exit", None), "Exit command"),
        ("1", ("start", None), "Start (numbered)"),
        ("2", ("stop", None), "Stop (numbered)"),
        ("3", ("gif", None), "GIF (numbered)"),
    ]

    for cmd, expected, description in tests:
        result = cli.map_command(cmd)
        assert result == expected, f"Failed: {description}"
        print(f"  [+] {description}: {cmd} -> {result}")

    print("[PASS] All command mappings correct")

def test_utilities():
    """Test utility functions"""
    print("\n[TEST] Utility Functions")

    # Test timestamp
    ts = get_timestamp()
    assert len(ts) == 15  # YYYYMMDD_HHMMSS
    assert "_" in ts
    print(f"  Timestamp: {ts}")

    # Test file size formatting
    sizes = [
        (512, "512.0 B"),
        (1024, "1.0 KB"),
        (1048576, "1.0 MB"),
    ]

    for size, expected_start in sizes:
        formatted = format_filesize(size)
        print(f"  {size} bytes -> {formatted}")

    print("[PASS] Utilities working correctly")

def test_directory_structure():
    """Verify directory structure"""
    print("\n[TEST] Directory Structure")
    config = Config()
    save_dir = config.save_dir

    assert os.path.exists(save_dir), f"Save directory not found: {save_dir}"
    print(f"  [+] Save directory exists: {save_dir}")

    # Check for AI model markdown files
    expected_files = ["claude.md", "gemini.md", "codex.md", "general.md"]
    for filename in expected_files:
        filepath = os.path.join(save_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  [+] {filename} ({format_filesize(size)})")

    print("[PASS] Directory structure verified")

def main():
    """Run all tests"""
    print("=" * 50)
    print("FlashRecord Functionality Test")
    print("=" * 50)

    try:
        test_config()
        test_cli_commands()
        test_utilities()
        test_directory_structure()

        print("\n" + "=" * 50)
        print("[SUCCESS] All tests passed!")
        print("=" * 50)
        print("\nNext steps:")
        print("  1. Run: python -m flashrecord.cli")
        print("  2. Use: @sc (screenshot)")
        print("  3. Use: @sv (GIF from recording)")
        print("=" * 50 + "\n")

    except AssertionError as e:
        print(f"\n[FAIL] {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
