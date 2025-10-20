"""
Video Recorder module - Wrapper for terminalizer CLI recording
"""

import subprocess
import os
from datetime import datetime
from .utils import get_timestamp


class VideoRecorder:
    """Handles video recording and GIF conversion"""

    def __init__(self, output_dir="flashrecord-save"):
        self.output_dir = output_dir
        self.current_recording = None
        os.makedirs(output_dir, exist_ok=True)

    def start_recording(self):
        """Start recording terminal using terminalizer"""
        try:
            timestamp = get_timestamp()
            recording_name = f"record_{timestamp}"
            recording_path = os.path.join(self.output_dir, recording_name)

            # Start terminalizer recording
            cmd = ["terminalizer", "record", recording_path]
            subprocess.Popen(cmd)

            self.current_recording = recording_path
            return recording_path

        except Exception as e:
            print(f"[-] Recording start error: {str(e)}")
            return None

    def stop_recording(self):
        """Stop recording (terminalizer uses Ctrl+C)"""
        try:
            # Terminalizer records until Ctrl+C
            # User will press Ctrl+C to stop
            return self.current_recording
        except Exception as e:
            print(f"[-] Recording stop error: {str(e)}")
            return None

    def convert_to_gif(self, recording_path):
        """Convert recording to GIF"""
        try:
            # Ensure recording path exists
            if not os.path.exists(recording_path):
                print(f"[-] Recording not found: {recording_path}")
                return None

            # Generate GIF filename
            timestamp = get_timestamp()
            gif_path = os.path.join(
                self.output_dir, f"recording_{timestamp}.gif"
            )

            # Render to GIF
            cmd = ["terminalizer", "render", recording_path, "-o", gif_path]
            result = subprocess.run(cmd, capture_output=True, timeout=30)

            if result.returncode == 0 and os.path.exists(gif_path):
                return gif_path
            else:
                print(f"[-] GIF conversion failed: {result.stderr.decode()}")
                return None

        except subprocess.TimeoutExpired:
            print("[-] GIF conversion timeout (>30s)")
            return None
        except Exception as e:
            print(f"[-] GIF conversion error: {str(e)}")
            return None


def record_video():
    """Convenience function for standalone recording"""
    recorder = VideoRecorder()
    return recorder
