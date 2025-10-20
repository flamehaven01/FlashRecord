"""
Screenshot module - Wrapper for hcap screenshot tool
"""

import subprocess
import os
import sys
from datetime import datetime
from .utils import get_timestamp


def take_screenshot(output_dir="flashrecord-save"):
    """Take screenshot using hcap tool"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename with timestamp
        timestamp = get_timestamp()
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        # Call hcap tool
        hcap_path = "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
        cmd = [sys.executable, hcap_path, filepath]

        result = subprocess.run(cmd, capture_output=True, timeout=5)

        if result.returncode == 0 and os.path.exists(filepath):
            return filepath
        else:
            print(f"[-] hcap failed: {result.stderr.decode()}")
            return None

    except subprocess.TimeoutExpired:
        print("[-] Screenshot timeout (>5s)")
        return None
    except Exception as e:
        print(f"[-] Screenshot error: {str(e)}")
        return None
