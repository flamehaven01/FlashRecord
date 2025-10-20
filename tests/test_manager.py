"""
Minimal Manager Tests - Core cleanup functionality
"""

import os
import pytest
import tempfile
import shutil
import time


@pytest.fixture
def temp_dir():
    """Create temp directory for testing"""
    temp = tempfile.mkdtemp()
    yield temp
    if os.path.exists(temp):
        shutil.rmtree(temp)


def test_cleanup_old_files(temp_dir):
    """Test file cleanup"""
    from flashrecord.manager import FileManager

    # Create old and new files
    old_file = os.path.join(temp_dir, "old.txt")
    new_file = os.path.join(temp_dir, "new.txt")

    with open(old_file, "w") as f:
        f.write("old")
    with open(new_file, "w") as f:
        f.write("new")

    # Set old_file to 2 days ago
    old_time = time.time() - (48 * 3600)
    os.utime(old_file, (old_time, old_time))

    manager = FileManager(temp_dir)
    deleted = manager.cleanup_old_files(hours=24)

    assert deleted == 1
    assert not os.path.exists(old_file)
    assert os.path.exists(new_file)


def test_get_storage_usage(temp_dir):
    """Test storage calculation"""
    from flashrecord.manager import FileManager

    # Create a file with content
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("x" * 10240)  # 10KB to be sure

    manager = FileManager(temp_dir)
    usage = manager.get_storage_usage()

    # Should be measurable (at least 0.01 MB)
    assert usage >= 0.01


def test_get_file_count(temp_dir):
    """Test file counting"""
    from flashrecord.manager import FileManager

    # Create test files
    for i in range(3):
        with open(os.path.join(temp_dir, f"file{i}.txt"), "w") as f:
            f.write("test")

    manager = FileManager(temp_dir)
    count = manager.get_file_count()

    assert count == 3
