"""
Screen recording to animated GIF
ScreenToGif-like functionality for FlashRecord v0.3.0
With KAIROS-inspired compression
"""

import os
import threading
import time

import imageio
from PIL import ImageGrab

from .compression import GIFCompressor
from .utils import get_timestamp


class ScreenRecorder:
    """Record screen to animated GIF"""

    def __init__(self, fps=10, quality=85, compression="balanced"):
        """
        Initialize screen recorder

        Args:
            fps: Frames per second (default: 10)
            quality: GIF quality 1-100 (default: 85)
            compression: 'high', 'balanced', 'compact', or 'none' (default: 'balanced')
        """
        self.fps = fps
        self.quality = quality
        self.compression_mode = compression
        self.frames = []
        self.is_recording = False
        self._capture_thread = None
        self._start_time = None

    def start_recording(self, duration=None):
        """
        Start capturing frames

        Args:
            duration: Optional duration in seconds (None = manual stop)
        """
        if self.is_recording:
            print("[-] Already recording")
            return False

        self.is_recording = True
        self.frames = []
        self._start_time = time.time()

        # Start capture thread
        self._capture_thread = threading.Thread(
            target=self._capture_frames, args=(duration,), daemon=True
        )
        self._capture_thread.start()
        return True

    def stop_recording(self):
        """Stop capturing frames"""
        if not self.is_recording:
            return False

        self.is_recording = False

        if self._capture_thread:
            self._capture_thread.join(timeout=2.0)

        return True

    def _capture_frames(self, duration=None):
        """
        Capture frames at specified FPS

        Args:
            duration: Optional auto-stop duration in seconds
        """
        interval = 1.0 / self.fps
        frame_count = 0

        while self.is_recording:
            loop_start = time.time()

            # Check duration limit
            if duration and (loop_start - self._start_time) >= duration:
                self.is_recording = False
                break

            try:
                # Capture screen
                screenshot = ImageGrab.grab()

                # Optional: Resize for smaller GIF (50% scale)
                # screenshot = screenshot.resize(
                #     (screenshot.width // 2, screenshot.height // 2)
                # )

                self.frames.append(screenshot)
                frame_count += 1

            except Exception as e:
                print(f"[-] Frame capture error: {e}")

            # Maintain FPS
            elapsed = time.time() - loop_start
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)

    def save_gif(self, output_path):
        """
        Save captured frames as GIF with KAIROS-inspired compression

        Args:
            output_path: Path to save GIF file

        Returns:
            True if successful, False otherwise
        """
        if not self.frames:
            print("[-] No frames to save")
            return False

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Apply compression if enabled
            frames_to_save = self.frames
            if self.compression_mode and self.compression_mode != "none":
                compressor = GIFCompressor(target_size_mb=10, quality=self.compression_mode)
                frames_to_save = compressor.compress_frames(self.frames)

                # Show compression stats
                stats = compressor.estimate_compression_ratio(self.frames, frames_to_save)
                if stats:
                    print(
                        f"[*] Compression: {stats['original_frames']} -> {stats['compressed_frames']} frames"
                    )
                    print(f"[*] Frame reduction: {stats['frame_reduction']}")

            # Save as GIF with imageio
            imageio.mimsave(
                output_path,
                frames_to_save,
                duration=1000 / self.fps,  # Duration per frame in ms
                loop=0,  # Infinite loop
            )

            return os.path.exists(output_path)

        except Exception as e:
            print(f"[-] GIF save error: {e}")
            return False

    def get_stats(self):
        """
        Get recording statistics

        Returns:
            dict with frame_count, duration, fps
        """
        frame_count = len(self.frames)
        duration = frame_count / self.fps if frame_count > 0 else 0

        return {
            "frame_count": frame_count,
            "duration": duration,
            "fps": self.fps,
            "recording": self.is_recording,
        }


def record_screen_to_gif(duration=5, fps=10, output_dir=None, compression="balanced"):
    """
    Convenience function: Record screen for duration and save as GIF

    Args:
        duration: Recording duration in seconds (default: 5)
        fps: Frames per second (default: 10)
        output_dir: Output directory (default: flashrecord-save)
        compression: 'high', 'balanced', 'compact', or 'none' (default: 'balanced')

    Returns:
        Path to saved GIF file, or None on failure
    """
    recorder = ScreenRecorder(fps=fps, compression=compression)

    print(f"[>] Recording screen for {duration} seconds...")

    # Start recording
    recorder.start_recording(duration=duration)

    # Wait for completion with progress
    start_time = time.time()
    while recorder.is_recording:
        elapsed = time.time() - start_time
        progress = min(100, int((elapsed / duration) * 100))
        bar = "■" * (progress // 10) + "□" * (10 - progress // 10)
        print(f"\r[{bar}] {progress}% ({elapsed:.1f}s)", end="", flush=True)
        time.sleep(0.1)

    print()  # New line after progress bar

    # Generate filename
    timestamp = get_timestamp()
    filename = f"screen_{timestamp}.gif"
    if output_dir is None:
        from .config import Config

        output_dir = Config().get_output_dir("gifs")

    filepath = os.path.join(output_dir, filename)

    # Save GIF
    print("[+] Encoding GIF...")
    if recorder.save_gif(filepath):
        stats = recorder.get_stats()
        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB

        print(f"[+] GIF saved: {filepath}")
        print(
            f"[+] Size: {file_size:.1f} MB, {stats['frame_count']} frames, {stats['duration']:.1f}s"
        )
        return filepath
    else:
        print("[-] Failed to save GIF")
        return None
