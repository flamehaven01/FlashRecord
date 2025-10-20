"""
Minimal Utils Tests - Core utility functions
"""

import pytest
from flashrecord.utils import get_timestamp, format_filesize


def test_get_timestamp():
    """Test timestamp generation"""
    ts = get_timestamp()
    assert len(ts) == 15
    assert ts[8] == "_"
    assert ts[:8].isdigit()
    assert ts[9:].isdigit()


def test_get_timestamp_format():
    """Test timestamp is valid datetime format"""
    from datetime import datetime
    ts = get_timestamp()
    # Should be parseable
    dt = datetime.strptime(ts, "%Y%m%d_%H%M%S")
    assert dt is not None


def test_format_filesize_bytes():
    """Test filesize formatting for bytes"""
    assert "B" in format_filesize(512)


def test_format_filesize_kb():
    """Test filesize formatting for kilobytes"""
    assert "KB" in format_filesize(1024)


def test_format_filesize_mb():
    """Test filesize formatting for megabytes"""
    assert "MB" in format_filesize(1024 * 1024)


def test_format_filesize_returns_string():
    """Test format_filesize returns string"""
    result = format_filesize(1024)
    assert isinstance(result, str)
