"""
Unit tests for flashrecord.screen_recorder module
"""

import inspect

import pytest

from flashrecord.screen_recorder import ScreenRecorder, record_screen_to_gif


class TestScreenRecorder:
    """Tests for ScreenRecorder class"""

    def test_screen_recorder_initialization(self):
        """Test that ScreenRecorder can be initialized"""
        recorder = ScreenRecorder()
        assert recorder is not None

    def test_screen_recorder_has_frames_list(self):
        """Test ScreenRecorder has frames attribute"""
        recorder = ScreenRecorder()
        assert hasattr(recorder, "frames")
        assert isinstance(recorder.frames, list)

    def test_screen_recorder_initial_state(self):
        """Test ScreenRecorder initial state"""
        recorder = ScreenRecorder()
        assert recorder.frames == []


class TestRecordFunction:
    """Tests for record_screen_to_gif function"""

    def test_function_exists(self):
        """Test that record_screen_to_gif function exists"""
        assert record_screen_to_gif is not None
        assert callable(record_screen_to_gif)

    def test_function_signature(self):
        """Test function has expected parameters"""
        sig = inspect.signature(record_screen_to_gif)
        params = list(sig.parameters.keys())

        # Check for expected parameters
        assert "duration" in params
        assert "fps" in params
        assert "output_dir" in params
        assert "compression" in params

    def test_function_defaults(self):
        """Test function has reasonable defaults"""
        sig = inspect.signature(record_screen_to_gif)

        # Check default values
        assert sig.parameters["duration"].default == 5
        assert sig.parameters["fps"].default == 10
        assert sig.parameters["compression"].default == "balanced"
