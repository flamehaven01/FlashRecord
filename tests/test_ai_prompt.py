"""
Minimal AI Prompt Tests
"""

import os
import pytest
import tempfile
import shutil


@pytest.fixture
def temp_save_dir():
    """Create temp save directory"""
    temp = tempfile.mkdtemp()
    yield temp
    if os.path.exists(temp):
        shutil.rmtree(temp)


def test_save_session(temp_save_dir):
    """Test session saving"""
    from flashrecord.ai_prompt import AIPromptManager

    manager = AIPromptManager(temp_save_dir)
    result = manager.save_session("claude")

    assert result is True
    assert os.path.exists(os.path.join(temp_save_dir, "claude.md"))


def test_save_session_all_models(temp_save_dir):
    """Test saving to all AI models"""
    from flashrecord.ai_prompt import AIPromptManager

    manager = AIPromptManager(temp_save_dir)

    for model in ["claude", "gemini", "codex", "general"]:
        result = manager.save_session(model)
        assert result is True
        assert os.path.exists(os.path.join(temp_save_dir, f"{model}.md"))


def test_init_creates_files(temp_save_dir):
    """Test initialization creates markdown files"""
    from flashrecord.ai_prompt import AIPromptManager

    manager = AIPromptManager(temp_save_dir)

    for model in ["claude", "gemini", "codex", "general"]:
        path = os.path.join(temp_save_dir, f"{model}.md")
        assert os.path.exists(path)
