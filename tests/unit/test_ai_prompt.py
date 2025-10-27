"""
Unit tests for flashrecord.ai_prompt module
"""

import pytest

from flashrecord.ai_prompt import AIPromptManager


class TestAIPromptManager:
    """Tests for AIPromptManager class"""

    def test_manager_initialization(self):
        """Test that AIPromptManager can be initialized"""
        manager = AIPromptManager()
        assert manager is not None

    def test_get_instruction_notes_returns_dict(self):
        """Test get_instruction_notes returns a dictionary"""
        manager = AIPromptManager()
        notes = manager.get_instruction_notes()
        assert isinstance(notes, dict)

    def test_get_instruction_notes_no_crash(self):
        """Test get_instruction_notes doesn't crash without files"""
        manager = AIPromptManager()
        # Should not raise exception even if files don't exist
        notes = manager.get_instruction_notes()
        assert notes is not None
