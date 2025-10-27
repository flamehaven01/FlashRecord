"""
Edge case tests for flashrecord.utils module
"""

import pytest

from flashrecord.utils import format_filesize, get_timestamp


class TestFormatFilesizeEdgeCases:
    """Edge case tests for format_filesize function"""

    def test_very_large_files(self):
        """Test formatting of very large files (TB range)"""
        # 5 TB
        result = format_filesize(5 * 1024 * 1024 * 1024 * 1024)
        assert "TB" in result
        assert "5.0" in result

    def test_exact_boundaries(self):
        """Test exact power-of-1024 boundaries"""
        # Exactly 1 GB
        assert format_filesize(1073741824) == "1.0 GB"
        # Just under 1 GB
        result = format_filesize(1073741823)
        assert "MB" in result

    def test_fractional_values(self):
        """Test fractional file sizes"""
        # 1.5 MB
        result = format_filesize(1.5 * 1024 * 1024)
        assert "1.5 MB" in result

    def test_very_small_values(self):
        """Test very small byte counts"""
        assert format_filesize(1) == "1.0 B"
        assert format_filesize(10) == "10.0 B"
        assert format_filesize(100) == "100.0 B"

    def test_negative_values_detailed(self):
        """Test negative values produce valid strings"""
        result = format_filesize(-1024)
        assert isinstance(result, str)
        # Negative values should still format, even if meaningless
        assert len(result) > 0


class TestGetTimestampEdgeCases:
    """Edge case tests for get_timestamp function"""

    def test_timestamp_consistency(self):
        """Test multiple timestamps have consistent format"""
        timestamps = [get_timestamp() for _ in range(5)]

        # All should be same length
        assert all(len(ts) == 15 for ts in timestamps)

        # All should have underscore at position 8
        assert all(ts[8] == "_" for ts in timestamps)

    def test_timestamp_year_format(self):
        """Test year is 4 digits starting with 20"""
        timestamp = get_timestamp()
        year = timestamp[:4]
        assert year.startswith("20"), "Year should start with 20"
        assert year.isdigit(), "Year should be numeric"

    def test_timestamp_components(self):
        """Test timestamp components are valid"""
        timestamp = get_timestamp()

        # Extract components
        year = int(timestamp[0:4])
        month = int(timestamp[4:6])
        day = int(timestamp[6:8])
        hour = int(timestamp[9:11])
        minute = int(timestamp[11:13])
        second = int(timestamp[13:15])

        # Validate ranges
        assert 2020 <= year <= 2099
        assert 1 <= month <= 12
        assert 1 <= day <= 31
        assert 0 <= hour <= 23
        assert 0 <= minute <= 59
        assert 0 <= second <= 59
