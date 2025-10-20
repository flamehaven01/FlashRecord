# FlashRecord Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-01-15

### Added
- [+] Initial release of FlashRecord standalone version
- [+] Screenshot capture using hcap tool (24.8ms performance)
- [+] Terminal recording with terminalizer integration
- [+] Automatic GIF conversion from terminal recordings
- [+] AI model detection (Claude, Gemini, Codex)
- [+] Session management with markdown files per AI model
- [+] File lifecycle management with auto-cleanup
- [+] Configuration system (config.json)
- [+] Comprehensive test suite (9 tests, 100% pass)
- [+] Windows batch launcher script
- [+] Full documentation with examples
- [+] Package setup for pip installation

### Features
- **CLI Interface**: Simple numbered commands (1-3) and hashtag commands (#sc, #sv)
- **Screenshot Module**: Thin wrapper around hcap for instant captures
- **Video Recorder Module**: Thin wrapper around terminalizer for recording
- **Config Module**: JSON-based configuration with default paths
- **AI Prompt Manager**: Session tracking for multiple AI models
- **File Manager**: Storage usage calculation and auto-cleanup
- **Utils Module**: Timestamp formatting and system info detection

### Architecture
- **Lightweight**: 790 lines of core code, minimal dependencies
- **Standalone**: Zero external API calls, 100% local operation
- **Modular**: 8 independent modules with clear responsibilities
- **Testable**: 9 comprehensive validation tests
- **Documented**: README with examples and troubleshooting

### Testing
- [+] Module imports (all 5 modules)
- [+] Configuration loading and validation
- [+] Directory creation and management
- [+] AI prompt manager initialization
- [+] File manager storage calculations
- [+] Utility function operations
- [+] CLI initialization and state management
- [+] Configuration file presence and validation
- [+] Start script presence and validity

### File Structure
```
D:\Sanctum\flashrecord/
├── flashrecord/                  (Python package)
│   ├── __init__.py
│   ├── cli.py                    (Main CLI interface)
│   ├── screenshot.py             (hcap wrapper)
│   ├── video_recorder.py         (terminalizer wrapper)
│   ├── config.py                 (Configuration management)
│   ├── ai_prompt.py              (AI session tracking)
│   ├── manager.py                (File lifecycle)
│   └── utils.py                  (Helper functions)
├── flashrecord-save/             (Auto-created save directory)
│   ├── screenshots/              (Captured screenshots)
│   ├── recordings/               (Terminal recordings)
│   └── gifs/                     (Generated GIFs)
├── flashrecord_start.bat         (Windows launcher)
├── config.json                   (Default configuration)
├── setup.py                      (Package configuration)
├── test_flashrecord.py           (Test suite)
├── README.md                     (Documentation)
├── CHANGELOG.md                  (This file)
└── .gitignore                    (Git exclusions)
```

### Requirements
- Python 3.8+
- terminalizer (npm install -g terminalizer)
- hcap tool (d:\Sanctum\hcap-1.5.0\simple_capture.py)

### Known Limitations
- Requires terminalizer for GIF recording (optional for screenshots)
- Windows batch launcher is Windows-specific
- hcap path is hardcoded in default config

### Next Steps
- Create GitHub repository
- Add PyPI package support
- Implement cross-platform launcher scripts (shell, zsh)
- Add video player for GIF preview
- Create GUI version using Gradio
- Add WebP video format support
- Implement cloud sync (optional)
