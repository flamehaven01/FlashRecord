# FlashRecord - Fast, Simple, Easy Screen Recording & GIF Generator

> **Fast Screen Recording + Instant GIF Generation + AI Prompt Storage**

A lightweight, CLI-based screen recording tool that captures screenshots, records terminal sessions, converts to GIF, and saves session data for AI models (Claude, Gemini, Codex).

## Features

- [+] **Instant Screenshots** - Uses hcap for 24.8ms screen capture
- [+] **Terminal Recording** - Records CLI output with terminalizer
- [+] **GIF Generation** - Auto-converts recordings to animated GIFs
- [+] **AI Model Integration** - Saves sessions for Claude, Gemini, Codex
- [+] **Auto-Cleanup** - Time-based file deletion (configurable hours)
- [+] **Lightweight** - CLI-only, minimal dependencies
- [+] **Cross-Platform** - Works on Windows, macOS, Linux

## Quick Start

### Installation

```bash
# Clone or download FlashRecord
cd D:\Sanctum\flashrecord

# Windows: Run start script
.\flashrecord_start.bat

# Or use Python directly
python -m flashrecord.cli
```

### Prerequisites

```bash
# Install Python 3.8+
python --version

# Install terminalizer globally (for GIF recording)
npm install -g terminalizer

# Ensure hcap is available
# Default: d:\Sanctum\hcap-1.5.0\simple_capture.py
```

## Command Styles

FlashRecord supports **3 configurable command styles**. Choose during first-time setup or edit `config.json`:

```json
{
  "command_style": "numbered"
}
```

### 1. Numbered Style (Default)
**Best for:** Speed, keyboard shortcuts, minimal typing

```
> 1                    # Start recording
> 2                    # Stop recording
> 3                    # Convert to GIF
> 4                    # Save to claude.md
> 5                    # Save to gemini.md
> 6                    # Save to codex.md
> #sc                  # Screenshot (universal)
> help                 # Help menu (universal)
> exit                 # Exit (universal)
```

**Config value:** `"numbered"`

---

### 2. vs/vc/vg Style (Video Start/Video Capture/Video Gif)
**Best for:** Mnemonics, easy to remember abbreviations

```
> vs                   # Video Start - Start recording
> vc                   # Video Capture - Stop recording
> vg                   # Video Gif - Convert to GIF
> cs                   # Claude Save - Save to claude.md
> cg                   # Gemini Save - Save to gemini.md
> cz                   # Codex Save - Save to codex.md
> sc                   # Screenshot (universal)
> help                 # Help menu (universal)
> exit                 # Exit (universal)
```

**Config value:** `"vs_vc_vg"`

---

### 3. Verbose Style (Full Words)
**Best for:** Clarity, self-documenting, new users

```
> start                # Start recording
> stop                 # Stop recording
> gif                  # Convert to GIF
> claude               # Save to claude.md
> gemini               # Save to gemini.md
> codex                # Save to codex.md
> #sc                  # Screenshot (universal)
> help                 # Help menu (universal)
> exit                 # Exit (universal)
```

**Config value:** `"verbose"`

---

### Universal Commands (All Styles)

| Command | Action |
|---------|--------|
| `#sc` | Take screenshot instantly |
| `#sv` | Render most recent recording to GIF |
| `help` | Show help menu |
| `exit` / `quit` / `q` | Exit FlashRecord |

### Instruction Notes

FlashRecord reads per-model guidance from the markdown files created in `flashrecord-save/`.
Add instructions either between `<!-- instructions:start -->` and `<!-- instructions:end -->`
or under a `## Instructions` heading inside `claude.md`, `gemini.md`, `codex.md`, or `general.md`.
The CLI prints these snippets at startup so you always see the latest workflow notes.

## Directory Structure

```
D:\Sanctum\flashrecord/
├── flashrecord/              # Main package
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Main CLI interface
│   ├── screenshot.py         # Screenshot wrapper
│   ├── video_recorder.py     # Video recording
│   ├── config.py             # Configuration management
│   ├── ai_prompt.py          # AI prompt manager
│   ├── manager.py            # File lifecycle
│   └── utils.py              # Helper utilities
├── flashrecord-save/         # Auto-created flat save directory
│   ├── *.png                 # Screenshots (auto-named)
│   ├── *.gif                 # GIF conversions (auto-named)
│   ├── claude.md             # Claude session records
│   ├── gemini.md             # Gemini session records
│   ├── codex.md              # Codex session records
│   └── general.md            # General session records
├── flashrecord_start.bat     # Windows launch script
├── config.json               # Configuration file
├── setup.py                  # Package setup
└── README.md                 # This file
```

## Configuration

Edit `config.json` to customize:

```json
{
  "auto_delete_hours": 24,
  "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
}
```

### Options

- **auto_delete_hours**: Auto-delete files older than N hours (0 = disable)
- **hcap_path**: Path to hcap screenshot tool

## Usage Examples

### Example 1: Quick Screenshot

```
> #sc
[+] Screenshot saved: flashrecord-save/screenshots/screenshot_20240115_143022.png
```

### Example 2: Record Terminal Session

```
> #sv
[>] Recording started... (press '2' to stop)
> [Do your terminal work]
> 2
[+] Recording stopped: flashrecord-save/recordings/record_20240115_143030
> 3
[+] GIF created: flashrecord-save/recordings/recording_20240115_143045.gif
```

### Example 3: Save Session to AI

```
> claude
[+] Saved to claude.md
```

## Output Structure

All files save to **flat `flashrecord-save/` directory** (no subdirectories):

### Screenshots
- Format: `PNG`
- Path: `flashrecord-save/screenshot_YYYYMMDD_HHMMSS.png`
- Size: Depends on screen resolution

### Recordings
- Format: `terminalizer YAML`
- Path: `flashrecord-save/record_YYYYMMDD_HHMMSS`

### GIFs
- Format: `GIF`
- Path: `flashrecord-save/recording_YYYYMMDD_HHMMSS.gif`
- Speed: Configurable via terminalizer options

### Session Records
- Format: `Markdown`
- Path: `flashrecord-save/claude.md`, `gemini.md`, `codex.md`, `general.md`

## Troubleshooting

### hcap Not Found

```
[-] Screenshot failed
```

**Solution:** Verify hcap path in config.json:
```bash
cd d:\Sanctum\hcap-1.5.0\
python simple_capture.py test.png
```

### terminalizer Not Found

```
Warning: terminalizer not found
Install: npm install -g terminalizer
```

**Solution:** Install globally:
```bash
npm install -g terminalizer
terminalizer --version
```

### Recording Not Starting

**Solution:** Check if another instance is using terminalizer:
```bash
tasklist | findstr terminalizer
```

## Module Reference

### CLI Module (`cli.py`)

Main command processor and user interface.

```python
from flashrecord import FlashRecordCLI

cli = FlashRecordCLI()
cli.run()
```

### Screenshot Module (`screenshot.py`)

Captures screenshots using hcap.

```python
from flashrecord import take_screenshot

path = take_screenshot()
```

### Video Recorder Module (`video_recorder.py`)

Handles recording and GIF conversion.

```python
from flashrecord.video_recorder import VideoRecorder

recorder = VideoRecorder()
recorder.start_recording()
recorder.convert_to_gif("path/to/recording")
```

### Configuration Module (`config.py`)

Manages settings and directories.

```python
from flashrecord.config import Config

config = Config()
print(config.save_dir)
```

### AI Prompt Manager (`ai_prompt.py`)

Saves sessions to AI model files.

```python
from flashrecord.ai_prompt import AIPromptManager

manager = AIPromptManager()
manager.save_session("claude")
```

### File Manager (`manager.py`)

Handles file lifecycle and cleanup.

```python
from flashrecord.manager import FileManager

manager = FileManager()
manager.cleanup_old_files(hours=24)
print(manager.get_storage_summary())
```

## Performance

- Screenshot Capture: ~24.8ms (hcap)
- GIF Conversion: ~2-5s (terminalizer)
- Session Save: ~50ms (markdown append)
- File Cleanup: ~100ms (directory scan)

## License

MIT License - See LICENSE file for details

## Author

Flamehaven - AI Development Framework

## Support

For issues or questions, check the troubleshooting section or review logs in flashrecord-save/ directory.
