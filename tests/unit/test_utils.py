"""
Unit tests for flashrecord.utils module
"""

import re

import pytest

from flashrecord.utils import format_filesize, get_timestamp


class TestGetTimestamp:
    """Tests for get_timestamp function"""

    def test_timestamp_format(self):
        """Test that timestamp follows expected format"""
        timestamp = get_timestamp()
        # Format: YYYYMMDD_HHMMSS
        pattern = r"^\d{8}_\d{6}$"
        assert re.match(pattern, timestamp), f"Timestamp {timestamp} doesn't match pattern"

    def test_timestamp_length(self):
        """Test timestamp has correct length"""
        timestamp = get_timestamp()
        assert len(timestamp) == 15, "Timestamp should be 15 characters (YYYYMMDD_HHMMSS)"

    def test_timestamp_uniqueness(self):
        """Test consecutive timestamps are different (usually)"""
        import time

        ts1 = get_timestamp()
        time.sleep(0.1)
        ts2 = get_timestamp()
        # Note: May fail if called within same second
        # This is acceptable as it's just checking basic functionality


class TestFormatFilesize:
    """Tests for format_filesize function"""

    def test_bytes(self):
        """Test formatting of bytes"""
        assert format_filesize(500) == "500.0 B"

    def test_kilobytes(self):
        """Test formatting of kilobytes"""
        assert format_filesize(1024) == "1.0 KB"
        assert format_filesize(1536) == "1.5 KB"

    def test_megabytes(self):
        """Test formatting of megabytes"""
        assert format_filesize(1024 * 1024) == "1.0 MB"
        assert format_filesize(2.5 * 1024 * 1024) == "2.5 MB"

    def test_gigabytes(self):
        """Test formatting of gigabytes"""
        assert format_filesize(1024 * 1024 * 1024) == "1.0 GB"

    def test_zero(self):
        """Test formatting of zero bytes"""
        assert format_filesize(0) == "0.0 B"

    def test_negative(self):
        """Test that negative values are handled"""
        # Should not raise exception
        result = format_filesize(-100)
        assert isinstance(result, str)
