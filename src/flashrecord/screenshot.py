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

        result = subprocess.run(["screencapture", "-x", tmp_path], capture_output=True, timeout=5)

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


def _save_image(img, filepath, compress=False, quality="balanced"):
    """
    Save PIL Image to file with optional compression

    Args:
        img: PIL Image to save
        filepath: Output file path
        compress: Enable compression (scale down resolution)
        quality: Compression quality - 'high' (70%), 'balanced' (50%), 'compact' (30%)

    Returns:
        True if successful, False otherwise
    """
    try:
        if img is None:
            return False

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Apply compression if requested
        if compress:
            from PIL import Image

            scale_factors = {
                "high": 0.70,  # 70% - minimal quality loss
                "balanced": 0.50,  # 50% - good balance
                "compact": 0.30,  # 30% - maximum compression
            }
            scale = scale_factors.get(quality, 0.50)

            w, h = img.size
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if img.mode == "RGBA":
            rgb_img = img.convert("RGB")
            # Phase 1: Always use optimize=True and compress_level=9
            rgb_img.save(filepath, "PNG", optimize=True, compress_level=9)
        else:
            # Phase 1: Always use optimize=True and compress_level=9
            img.save(filepath, "PNG", optimize=True, compress_level=9)

        return os.path.exists(filepath)
    except Exception as e:
        print(f"[-] Failed to save image: {str(e)}")
        return False


def take_screenshot(output_dir=None, compress=False, quality="balanced"):
    """
    Take screenshot natively without external dependencies

    Supports:
    - Windows: PIL/Pillow (ImageGrab)
    - macOS: screencapture command
    - Linux: gnome-screenshot, scrot, or ImageMagick

    Compression (v0.3.3):
    - Phase 1: Always applies optimize=True (5-15% reduction, lossless)
    - Phase 2: Optional resolution scaling for 50-90% reduction

    Args:
        output_dir: Directory to save screenshot
        compress: Enable resolution scaling (default: False)
        quality: Compression quality when compress=True
                 - 'high': 70% scale (minimal quality loss, ~50% size reduction)
                 - 'balanced': 50% scale (good balance, ~75% size reduction)
                 - 'compact': 30% scale (maximum compression, ~90% size reduction)

    Returns:
        Path to saved screenshot file, or None on failure

    Examples:
        take_screenshot()                           # optimize only (2.1 MB)
        take_screenshot(compress=True)              # balanced (0.6 MB)
        take_screenshot(compress=True, quality='high')  # high quality (1.2 MB)
    """
    try:
        if output_dir is None:
            from .config import Config

            output_dir = Config().get_output_dir("screenshots")

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

        # Save image with compression
        if _save_image(img, filepath, compress=compress, quality=quality):
            return filepath
        else:
            print("[-] Failed to save screenshot")
            return None

    except Exception as e:
        print(f"[-] Screenshot error: {str(e)}")
        return None
