"""
Unit tests for video_recorder module - video_recorder.py
Tests the VideoRecorder class with mocked subprocess and file operations
"""

import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import tempfile
import shutil


@pytest.fixture
def video_recorder():
    """Create a VideoRecorder instance for testing"""
    from flashrecord.video_recorder import VideoRecorder

    # Use temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    recorder = VideoRecorder(output_dir=temp_dir)
    yield recorder
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def mock_timestamp(monkeypatch):
    """Mock the get_timestamp function"""
    from flashrecord import utils
    monkeypatch.setattr(utils, 'get_timestamp', lambda: '20250101_120000')
    return '20250101_120000'


class TestVideoRecorderInit:
    """Test VideoRecorder initialization"""

    def test_init_default_directory(self):
        """Test VideoRecorder initialization with default directory"""
        from flashrecord.video_recorder import VideoRecorder

        with patch('flashrecord.video_recorder.os.makedirs'):
            recorder = VideoRecorder()

        assert recorder.output_dir == "flashrecord-save/recordings"
        assert recorder.current_recording is None

    def test_init_custom_directory(self):
        """Test VideoRecorder initialization with custom directory"""
        from flashrecord.video_recorder import VideoRecorder

        with patch('flashrecord.video_recorder.os.makedirs'):
            recorder = VideoRecorder(output_dir="custom/path")

        assert recorder.output_dir == "custom/path"

    def test_init_creates_directory(self):
        """Test that initialization creates output directory"""
        from flashrecord.video_recorder import VideoRecorder

        with patch('flashrecord.video_recorder.os.makedirs') as mock_makedirs:
            recorder = VideoRecorder("test_dir")

        mock_makedirs.assert_called_once_with("test_dir", exist_ok=True)


class TestVideoRecorderStartRecording:
    """Test video recording start functionality"""

    @patch('flashrecord.video_recorder.subprocess.Popen')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_start_recording_success(
        self, mock_makedirs, mock_popen, mock_timestamp
    ):
        """Test successful recording start"""
        from flashrecord.video_recorder import VideoRecorder

        mock_popen.return_value = MagicMock()

        recorder = VideoRecorder()
        result = recorder.start_recording()

        # Verify Popen was called with correct terminalizer command
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert args[0] == "terminalizer"
        assert args[1] == "record"

        # Verify return value contains expected format
        assert result is not None
        assert "record_" in result

        # Verify current_recording is set
        assert recorder.current_recording is not None

    @patch('flashrecord.video_recorder.subprocess.Popen')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_start_recording_exception_handling(
        self, mock_makedirs, mock_popen, mock_timestamp
    ):
        """Test recording start with exception"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock Popen to raise an exception
        mock_popen.side_effect = FileNotFoundError("terminalizer not found")

        recorder = VideoRecorder()

        with patch('builtins.print') as mock_print:
            result = recorder.start_recording()

        # Should return None on error
        assert result is None

        # Verify error message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Recording start error" in str(call) for call in print_calls)

    @patch('flashrecord.video_recorder.subprocess.Popen')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_start_recording_stores_path(
        self, mock_makedirs, mock_popen, mock_timestamp
    ):
        """Test that start_recording stores the recording path"""
        from flashrecord.video_recorder import VideoRecorder

        mock_popen.return_value = MagicMock()

        recorder = VideoRecorder()
        result = recorder.start_recording()

        # Verify path is stored in current_recording
        assert recorder.current_recording == result


class TestVideoRecorderStopRecording:
    """Test video recording stop functionality"""

    @patch('flashrecord.video_recorder.os.makedirs')
    def test_stop_recording_returns_current_recording(self, mock_makedirs):
        """Test that stop_recording returns current recording path"""
        from flashrecord.video_recorder import VideoRecorder

        recorder = VideoRecorder()
        recorder.current_recording = "/path/to/recording"

        result = recorder.stop_recording()

        # Should return the current recording path
        assert result == "/path/to/recording"

    @patch('flashrecord.video_recorder.os.makedirs')
    def test_stop_recording_exception_handling(self, mock_makedirs):
        """Test stop_recording exception handling"""
        from flashrecord.video_recorder import VideoRecorder

        recorder = VideoRecorder()
        # Don't set current_recording to trigger error scenario
        recorder.current_recording = "/path/to/recording"

        # Mock an exception
        with patch.object(recorder, 'current_recording', None):
            with patch('builtins.print'):
                # This shouldn't actually raise, but handles edge cases
                result = recorder.stop_recording()

        # Behavior with None current_recording
        assert result is None


class TestVideoRecorderConvertToGif:
    """Test GIF conversion functionality"""

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_success(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test successful GIF conversion"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock file existence
        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        recorder = VideoRecorder()
        result = recorder.convert_to_gif("/path/to/recording")

        # Verify subprocess was called with terminalizer render command
        mock_subprocess.assert_called_once()
        args, kwargs = mock_subprocess.call_args
        assert args[0][0] == "terminalizer"
        assert args[0][1] == "render"

        # Verify return value
        assert result is not None
        assert ".gif" in result

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_file_not_found(
        self, mock_makedirs, mock_exists, mock_subprocess
    ):
        """Test GIF conversion with missing recording file"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock file doesn't exist
        mock_exists.return_value = False

        recorder = VideoRecorder()

        with patch('builtins.print') as mock_print:
            result = recorder.convert_to_gif("/nonexistent/path")

        # Should return None
        assert result is None

        # Verify error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("not found" in str(call).lower() for call in print_calls)

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_subprocess_failure(
        self, mock_makedirs, mock_exists, mock_subprocess
    ):
        """Test GIF conversion when subprocess fails"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock file exists but conversion fails
        mock_exists.side_effect = [True, False]  # First exists check True, second False
        mock_subprocess.return_value = MagicMock(
            returncode=1,
            stderr=b"conversion error"
        )

        recorder = VideoRecorder()

        with patch('builtins.print') as mock_print:
            result = recorder.convert_to_gif("/path/to/recording")

        # Should return None
        assert result is None

        # Verify error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("failed" in str(call).lower() for call in print_calls)

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_timeout(
        self, mock_makedirs, mock_exists, mock_subprocess
    ):
        """Test GIF conversion timeout"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock file exists
        mock_exists.return_value = True
        mock_subprocess.side_effect = subprocess.TimeoutExpired('cmd', 30)

        recorder = VideoRecorder()

        with patch('builtins.print') as mock_print:
            result = recorder.convert_to_gif("/path/to/recording")

        # Should return None
        assert result is None

        # Verify timeout message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("timeout" in str(call).lower() for call in print_calls)

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_general_exception(
        self, mock_makedirs, mock_exists, mock_subprocess
    ):
        """Test GIF conversion with general exception"""
        from flashrecord.video_recorder import VideoRecorder

        # Mock general exception
        mock_exists.return_value = True
        mock_subprocess.side_effect = OSError("Disk full")

        recorder = VideoRecorder()

        with patch('builtins.print') as mock_print:
            result = recorder.convert_to_gif("/path/to/recording")

        # Should return None
        assert result is None

        # Verify error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("error" in str(call).lower() for call in print_calls)

    @patch('flashrecord.video_recorder.subprocess.run')
    @patch('flashrecord.video_recorder.os.path.exists')
    @patch('flashrecord.video_recorder.os.makedirs')
    def test_convert_to_gif_generates_correct_output_path(
        self, mock_makedirs, mock_exists, mock_subprocess, mock_timestamp
    ):
        """Test that GIF path is generated correctly"""
        from flashrecord.video_recorder import VideoRecorder

        mock_exists.return_value = True
        mock_subprocess.return_value = MagicMock(returncode=0)

        recorder = VideoRecorder("test_dir")
        result = recorder.convert_to_gif("/path/to/recording")

        # Verify GIF path format
        assert "recording_" in result
        assert result.endswith(".gif")
        assert "test_dir" in result


class TestVideoRecorderConvenienceFunction:
    """Test the record_video convenience function"""

    @patch('flashrecord.video_recorder.os.makedirs')
    def test_record_video_function(self, mock_makedirs):
        """Test record_video convenience function"""
        from flashrecord.video_recorder import record_video

        recorder = record_video()

        # Should return a VideoRecorder instance
        from flashrecord.video_recorder import VideoRecorder
        assert isinstance(recorder, VideoRecorder)
