"""
FlashRecord Test Suite - Verification and validation tests
"""

import os
import sys
import json
from pathlib import Path


def test_module_imports():
    """Test: All modules can be imported"""
    try:
        from flashrecord import (
            FlashRecordCLI,
            take_screenshot,
            record_video,
            FileManager,
            AIPromptManager,
        )
        print("[+] test_module_imports: PASS")
        return True
    except Exception as e:
        print(f"[-] test_module_imports: FAIL - {str(e)}")
        return False


def test_config_loading():
    """Test: Configuration loads correctly"""
    try:
        from flashrecord.config import Config

        config = Config()
        assert config.auto_delete_hours == 24
        assert config.hcap_path == "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
        assert os.path.exists(config.save_dir)
        print("[+] test_config_loading: PASS")
        return True
    except Exception as e:
        print(f"[-] test_config_loading: FAIL - {str(e)}")
        return False


def test_directories_created():
    """Test: Required directories are created"""
    try:
        from flashrecord.config import Config

        config = Config()
        dirs = [config.save_dir, config.screenshot_dir, config.video_dir, config.gif_dir]
        for d in dirs:
            assert os.path.exists(d), f"Directory not found: {d}"
        print("[+] test_directories_created: PASS")
        return True
    except Exception as e:
        print(f"[-] test_directories_created: FAIL - {str(e)}")
        return False


def test_ai_prompt_manager():
    """Test: AIPromptManager initializes and creates files"""
    try:
        from flashrecord.ai_prompt import AIPromptManager

        manager = AIPromptManager()
        assert os.path.exists(manager.ai_files["claude"])
        assert os.path.exists(manager.ai_files["gemini"])
        assert os.path.exists(manager.ai_files["codex"])
        print("[+] test_ai_prompt_manager: PASS")
        return True
    except Exception as e:
        print(f"[-] test_ai_prompt_manager: FAIL - {str(e)}")
        return False


def test_file_manager():
    """Test: FileManager can calculate storage usage"""
    try:
        from flashrecord.manager import FileManager

        manager = FileManager()
        usage = manager.get_storage_usage()
        count = manager.get_file_count()
        summary = manager.get_storage_summary()

        assert isinstance(usage, float)
        assert isinstance(count, int)
        assert "total_size_mb" in summary
        assert "file_count" in summary
        print("[+] test_file_manager: PASS")
        return True
    except Exception as e:
        print(f"[-] test_file_manager: FAIL - {str(e)}")
        return False


def test_utils_functions():
    """Test: Utility functions work correctly"""
    try:
        from flashrecord.utils import get_timestamp, format_filesize, get_system_info

        timestamp = get_timestamp()
        assert isinstance(timestamp, str)
        assert len(timestamp) == 15  # YYYYMMDD_HHMMSS

        filesize = format_filesize(1024)
        assert "KB" in filesize

        sysinfo = get_system_info()
        assert "platform" in sysinfo
        assert "python_version" in sysinfo

        print("[+] test_utils_functions: PASS")
        return True
    except Exception as e:
        print(f"[-] test_utils_functions: FAIL - {str(e)}")
        return False


def test_cli_initialization():
    """Test: CLI can be initialized"""
    try:
        from flashrecord.cli import FlashRecordCLI

        cli = FlashRecordCLI()
        assert cli.config is not None
        assert cli.ai_manager is not None
        assert cli.video_recorder is not None
        assert cli.recording is False
        print("[+] test_cli_initialization: PASS")
        return True
    except Exception as e:
        print(f"[-] test_cli_initialization: FAIL - {str(e)}")
        return False


def test_config_json_exists():
    """Test: config.json file exists and is valid JSON"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        assert os.path.exists(config_path), "config.json not found"

        with open(config_path, "r") as f:
            config = json.load(f)

        assert "auto_delete_hours" in config
        assert "hcap_path" in config
        print("[+] test_config_json_exists: PASS")
        return True
    except Exception as e:
        print(f"[-] test_config_json_exists: FAIL - {str(e)}")
        return False


def test_start_script_exists():
    """Test: flashrecord_start.bat exists"""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "flashrecord_start.bat")
        assert os.path.exists(script_path), "flashrecord_start.bat not found"
        print("[+] test_start_script_exists: PASS")
        return True
    except Exception as e:
        print(f"[-] test_start_script_exists: FAIL - {str(e)}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 60)
    print("FlashRecord Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_module_imports,
        test_config_loading,
        test_directories_created,
        test_ai_prompt_manager,
        test_file_manager,
        test_utils_functions,
        test_cli_initialization,
        test_config_json_exists,
        test_start_script_exists,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[-] {test.__name__}: ERROR - {str(e)}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
