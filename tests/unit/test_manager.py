"""
Unit tests for flashrecord.manager module
"""

import os
import tempfile
import time
from pathlib import Path

import pytest

from flashrecord.manager import FileManager


class TestFileManager:
    """Tests for FileManager class"""

    def test_manager_initialization(self):
        """Test that FileManager can be initialized"""
        manager = FileManager()
        assert manager is not None

    def test_manager_with_custom_dir(self):
        """Test FileManager with custom directory"""
        manager = FileManager(save_dir="custom-dir")
        assert manager.save_dir == "custom-dir"

    def test_get_storage_usage_empty(self):
        """Test storage usage for non-existent directory"""
        manager = FileManager(save_dir="nonexistent-dir-xyz")
        usage = manager.get_storage_usage()
        assert usage == 0.0

    def test_get_file_count_empty(self):
        """Test file count for non-existent directory"""
        manager = FileManager(save_dir="nonexistent-dir-xyz")
        count = manager.get_file_count()
        assert count == 0

    def test_cleanup_old_files_safe(self):
        """Test cleanup doesn't crash on non-existent directory"""
        manager = FileManager(save_dir="nonexistent-dir-xyz")
        deleted = manager.cleanup_old_files(hours=1)
        assert deleted == 0
