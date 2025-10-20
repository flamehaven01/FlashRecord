"""
Minimal File Manager - Auto-cleanup old files
"""

import os
import time


class FileManager:
    """Minimal file lifecycle management"""

    def __init__(self, save_dir="flashrecord-save"):
        self.save_dir = save_dir

    def cleanup_old_files(self, hours=24):
        """Delete files older than N hours"""
        try:
            cutoff_time = time.time() - (hours * 3600)
            deleted = 0
            for root, _, files in os.walk(self.save_dir):
                for f in files:
                    path = os.path.join(root, f)
                    if os.path.getmtime(path) < cutoff_time:
                        os.remove(path)
                        deleted += 1
            return deleted
        except:
            return 0

    def get_storage_usage(self):
        """Get total storage in MB"""
        try:
            total = 0
            for root, _, files in os.walk(self.save_dir):
                for f in files:
                    total += os.path.getsize(os.path.join(root, f))
            return round(total / (1024 * 1024), 2)
        except:
            return 0.0

    def get_file_count(self):
        """Count all files"""
        try:
            count = 0
            for root, _, files in os.walk(self.save_dir):
                count += len(files)
            return count
        except:
            return 0
