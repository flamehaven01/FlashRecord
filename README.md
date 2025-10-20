# FlashRecord - Fast Screen Recording & GIF Generator

> **One-command screen capture + GIF generation + AI session storage**

A lightweight CLI tool for recording screens, capturing screenshots, and saving sessions to AI models (Claude, Gemini, Codex).

## Features

- **Screenshot** - Instant screen capture (24.8ms with hcap)
- **Terminal Recording** - Record CLI sessions with terminalizer
- **GIF Export** - Auto-convert recordings to animated GIFs
- **AI Integration** - Save sessions for Claude, Gemini, Codex
- **Auto-Cleanup** - Delete files older than N hours
- **Cross-Platform** - Windows, macOS, Linux

## Quick Start

### Installation

```bash
# Clone repository
cd D:\Sanctum\flashrecord

# Windows: Run start script
.\flashrecord_start.bat

# Or use Python directly
python -m flashrecord.cli
```

### Prerequisites

```bash
# Python 3.8+
python --version

# Install terminalizer (for GIF recording)
npm install -g terminalizer

# Ensure hcap is available
# Default: d:\Sanctum\hcap-1.5.0\simple_capture.py
```

## Commands

### Three Command Styles Available

Choose your preferred style during setup or edit `config.json`:

#### 1. Numbered (Default) - Fast
```
> 1              # Start recording
> 2              # Stop recording
> 3              # Convert to GIF
> 4              # Save to claude.md
> 5              # Save to gemini.md
> 6              # Save to codex.md
```

#### 2. Abbreviation (vs/vc/vg) - Mnemonics
```
> vs             # Video Start
> vc             # Video Capture (stop)
> vg             # Video Gif
> cs             # Claude Save
> cg             # Gemini Save
> cz             # Codex Save
```

#### 3. Verbose - Full Words
```
> start          # Start recording
> stop           # Stop recording
> gif            # Convert to GIF
> claude         # Save to claude.md
> gemini         # Save to gemini.md
> codex          # Save to codex.md
```

### Universal Commands (All Styles)

| Command | Action |
|---------|--------|
| `#sc` | Take screenshot instantly |
| `#sv` | Render recording to GIF |
| `help` | Show help menu |
| `exit` / `quit` / `q` | Exit FlashRecord |

## Usage Examples

### Example 1: Quick Screenshot
```
> #sc
[+] Screenshot: flashrecord-save/screenshot_20251020_143022.png
```

### Example 2: Record & Convert to GIF
```
> 1
[>] Recording started... (use '2' to stop)
[Do your work...]
> 2
[+] Recording stopped
> 3
[+] GIF: flashrecord-save/recording_20251020_143045.gif
```

### Example 3: Save Session to AI
```
> 4
[+] Saved to claude.md
```

## File Organization

All files save to **`flashrecord-save/`** (flat structure):

```
flashrecord-save/
├── screenshot_*.png        # Screenshots
├── record_*                # Terminal recordings
├── recording_*.gif         # GIF files
├── claude.md               # Claude sessions
├── gemini.md               # Gemini sessions
├── codex.md                # Codex sessions
└── general.md              # General sessions
```

## Configuration

Edit `config.json` to customize:

```json
{
  "command_style": "numbered",
  "auto_delete_hours": 24,
  "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
}
```

- **command_style**: `"numbered"`, `"vs_vc_vg"`, or `"verbose"`
- **auto_delete_hours**: Auto-delete files older than N hours (0 = disabled)
- **hcap_path**: Path to hcap screenshot tool

## Instruction Notes

Add workflow instructions to markdown files in `flashrecord-save/`:

**Option 1: HTML Comments**
```markdown
<!-- instructions:start -->
Your instructions here
<!-- instructions:end -->
```

**Option 2: Heading Section**
```markdown
## Instructions
Your instructions here
```

Instructions display at startup for quick reference.

## Troubleshooting

### Screenshot Failed
```
[-] Screenshot failed
```
**Fix**: Verify hcap path in `config.json`:
```bash
cd d:\Sanctum\hcap-1.5.0
python simple_capture.py test.png
```

### Terminalizer Not Found
```
Warning: terminalizer not found
```
**Fix**: Install globally:
```bash
npm install -g terminalizer
terminalizer --version
```

### Recording Won't Start
**Fix**: Check for other terminalizer instances:
```bash
tasklist | findstr terminalizer
```

## Performance

- Screenshot Capture: ~24.8ms
- GIF Conversion: ~2-5s
- Session Save: ~50ms
- File Cleanup: ~100ms

## Directory Structure

```
D:\Sanctum\flashrecord/
├── flashrecord/
│   ├── cli.py              # Main CLI interface
│   ├── screenshot.py       # Screenshot wrapper
│   ├── video_recorder.py   # Video recording
│   ├── config.py           # Configuration management
│   ├── ai_prompt.py        # AI session manager
│   ├── manager.py          # File lifecycle
│   ├── utils.py            # Utilities
│   └── api.py              # FastAPI REST interface
├── flashrecord-save/       # Auto-created output directory
├── tests/                  # Test suite
├── pyproject.toml          # Poetry configuration
├── config.json             # User configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## API Reference

### CLI Module
```python
from flashrecord import FlashRecordCLI

cli = FlashRecordCLI()
cli.run()
```

### Screenshot Function
```python
from flashrecord.screenshot import take_screenshot

path = take_screenshot()  # Saves to flashrecord-save/screenshot_*.png
```

### Video Recorder
```python
from flashrecord.video_recorder import VideoRecorder

recorder = VideoRecorder()
recorder.start_recording()
# ... do work ...
recorder.stop_recording()
gif = recorder.convert_to_gif("recording_path")
```

### Configuration
```python
from flashrecord.config import Config

config = Config()
print(config.save_dir)           # Output directory
print(config.command_style)      # Current command style
print(config.auto_delete_hours)  # Auto-cleanup threshold
```

### AI Session Manager
```python
from flashrecord.ai_prompt import AIPromptManager

manager = AIPromptManager()
manager.save_session("claude")   # Save session timestamp
notes = manager.get_instruction_notes()  # Load workflow notes
```

## License

MIT License - See LICENSE file

## Author

Flamehaven - AI Development Framework

## Support

Check troubleshooting section or review logs in `flashrecord-save/` directory.
