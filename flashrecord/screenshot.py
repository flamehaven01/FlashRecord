"""
Screenshot module - Native screen capture without external dependencies
Supports Windows, macOS, and Linux platforms
"""

import os
import sys
from .utils import get_timestamp


def _capture_windows():
    """Capture screenshot on Windows using native PIL/Pillow"""
    try:
        from PIL import ImageGrab
        return ImageGrab.grab()
    except ImportError:
        return None
    except Exception as e:
        print(f"[-] PIL capture failed: {str(e)}")
        return None


def _capture_macos():
    """Capture screenshot on macOS using screencapture"""
    import subprocess
    import tempfile
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        result = subprocess.run(
            ["screencapture", "-x", tmp_path],
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0 and os.path.exists(tmp_path):
            from PIL import Image
            img = Image.open(tmp_path)
            os.unlink(tmp_path)
            return img
        return None
    except Exception as e:
        print(f"[-] macOS capture failed: {str(e)}")
        return None


def _capture_linux():
    """Capture screenshot on Linux using available tools"""
    import subprocess
    import tempfile

    # Try multiple tools in order
    tools = [
        (["gnome-screenshot", "-f"], "gnome-screenshot"),
        (["scrot"], "scrot"),
        (["import", "-window", "root"], "ImageMagick"),
    ]

    for cmd_prefix, tool_name in tools:
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name

            # Adjust command for tool
            if tool_name == "gnome-screenshot":
                cmd = cmd_prefix + [tmp_path]
            elif tool_name == "scrot":
                cmd = cmd_prefix + [tmp_path]
            else:  # ImageMagick
                cmd = cmd_prefix + [tmp_path]

            result = subprocess.run(cmd, capture_output=True, timeout=5)

            if result.returncode == 0 and os.path.exists(tmp_path):
                from PIL import Image
                img = Image.open(tmp_path)
                os.unlink(tmp_path)
                return img
        except Exception:
            continue

    return None


def _save_image(img, filepath):
    """Save PIL Image to file"""
    try:
        if img is None:
            return False

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if img.mode == "RGBA":
            rgb_img = img.convert("RGB")
            rgb_img.save(filepath, "PNG")
        else:
            img.save(filepath, "PNG")

        return os.path.exists(filepath)
    except Exception as e:
        print(f"[-] Failed to save image: {str(e)}")
        return False


def take_screenshot(output_dir="flashrecord-save"):
    """
    Take screenshot natively without external dependencies

    Supports:
    - Windows: PIL/Pillow (ImageGrab)
    - macOS: screencapture command
    - Linux: gnome-screenshot, scrot, or ImageMagick

    Args:
        output_dir: Directory to save screenshot

    Returns:
        Path to saved screenshot file, or None on failure
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename with timestamp
        timestamp = get_timestamp()
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        # Capture based on platform
        if sys.platform == "win32":
            img = _capture_windows()
        elif sys.platform == "darwin":
            img = _capture_macos()
        elif sys.platform.startswith("linux"):
            img = _capture_linux()
        else:
            print(f"[-] Unsupported platform: {sys.platform}")
            return None

        # Save image
        if _save_image(img, filepath):
            return filepath
        else:
            print("[-] Failed to save screenshot")
            return None

    except Exception as e:
        print(f"[-] Screenshot error: {str(e)}")
        return None
