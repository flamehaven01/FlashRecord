"""
Minimal Utilities - Timestamp and formatting
"""

from datetime import datetime


def get_timestamp():
    """Get YYYYMMDD_HHMMSS timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_filesize(size_bytes):
    """Convert bytes to human-readable"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
