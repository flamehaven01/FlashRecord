"""
FlashRecord CLI Wrapper for Claude Code Integration
Allows direct execution of @sc and @sv commands from Claude
"""

import sys
import os

# Add src/ to path for flashrecord package
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

from flashrecord.screenshot import take_screenshot
from flashrecord.screen_recorder import record_screen_to_gif
from flashrecord.config import Config


def execute_screenshot():
    """Execute @sc command - Take screenshot"""
    print("[*] Executing @sc - Screenshot capture...")
    config = Config()
    screenshot_dir = config.get_output_dir("screenshots")
    result = take_screenshot(output_dir=screenshot_dir)

    if result:
        print(f"[+] Screenshot saved: {result}")
        file_size = os.path.getsize(result) / 1024  # KB
        print(f"[+] File size: {file_size:.1f} KB")
        return result
    else:
        print("[-] Screenshot failed")
        return None


def execute_screen_record(duration=5, fps=10):
    """Execute @sv command - Record screen to GIF"""
    print(f"[*] Executing @sv - Recording screen for {duration} seconds...")
    config = Config()
    gif_dir = config.get_output_dir("gifs")

    result = record_screen_to_gif(duration=duration, fps=fps, output_dir=gif_dir)

    return result


def main():
    """Main entry point for CLI wrapper"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python flashrecord_cli_wrapper.py @sc")
        print("  python flashrecord_cli_wrapper.py @sv [duration] [fps]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "@sc":
        execute_screenshot()

    elif command == "@sv":
        # Parse optional duration and fps
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        fps = int(sys.argv[3]) if len(sys.argv) > 3 else 10

        # Validate
        if duration < 1 or duration > 60:
            print("[-] Duration must be between 1-60 seconds. Using default: 5")
            duration = 5

        if fps < 1 or fps > 30:
            print("[-] FPS must be between 1-30. Using default: 10")
            fps = 10

        execute_screen_record(duration=duration, fps=fps)

    else:
        print(f"[-] Unknown command: {command}")
        print("[*] Available commands: @sc, @sv")
        sys.exit(1)


if __name__ == "__main__":
    main()
