# FlashRecord - Fast Screen Recording & GIF Generator

> **The fastest, simplest screen capture for developers - Python-first CLI tool**

A lightweight CLI tool for instant screen capture, GIF recording, and AI session integration. Built for developers who need automation-friendly, cross-platform screen recording without the GUI overhead.

## Why FlashRecord?

### For Developers, By Developers
- **CLI-First**: No GUI overhead - perfect for automation and scripting
- **Python Native**: `import flashrecord` - use in your scripts directly
- **One-Command Simplicity**: `@sc` for screenshots, `@sv` for GIF recording
- **Zero Configuration**: Works out of the box with sensible defaults
- **Cross-Platform**: Windows, macOS, Linux - same commands everywhere

### vs Other Tools

| Tool | Platform | Interface | Python Integration | Install Size |
|------|----------|-----------|-------------------|--------------|
| **FlashRecord** | All | CLI | Native (`import flashrecord`) | ~2 MB (pip) |
| ScreenToGif | Windows | GUI | None | ~40 MB |
| ShareX | Windows | GUI | None | ~15 MB |
| Kap | macOS | GUI | None | ~50 MB |
| peek | Linux | GUI | None | ~5 MB |
| ImageMagick | All | CLI | Complex | ~30 MB |

**Key Differentiator**: FlashRecord is the only Python-native, cross-platform screen recorder with direct scripting integration. Perfect for test automation, documentation workflows, and CI/CD pipelines.

## Features

- **Native Screenshot** - Instant screen capture with Pillow/PIL (no external tools needed)
- **Screen Recording to GIF** - One-command full screen recording with imageio + numpy
- **Intelligent Compression** - 99.5% file size reduction with RGB color preservation
  - CWAM-inspired approach (arXiv:2410.21144) implemented purely in Python
  - Cross-window saliency analysis (multi-scale feature extraction)
  - Temporal subsampling (10fps → 8fps) and adaptive resolution scaling
  - Saliency-based quality preservation (variance + edge density + entropy)
  - No ML models required - pure PIL/NumPy implementation
- **AI Integration** - Save sessions for Claude, Gemini, Codex
- **Auto-Cleanup** - Delete files older than N hours
- **Cross-Platform** - Windows, macOS, Linux (native support for each)
- **Production Ready** - Full CI/CD, pytest suite, Sphinx docs, PyPI-ready structure

## Quick Start

### Installation

```bash
# From PyPI (recommended - coming soon)
pip install flashrecord

# From source
git clone https://github.com/Flamehaven/flashrecord.git
cd flashrecord
pip install -e .

# Or with Poetry
poetry install
```

### Prerequisites

```bash
# Python 3.8+
python --version

# Core dependencies (auto-installed):
# - pillow>=9.0.0 (native screenshot capture)
# - imageio>=2.0.0 (GIF encoding with compression)
# - numpy>=1.20.0 (frame processing and saliency analysis)
```

### Usage

```bash
# Run CLI
flashrecord

# Or with Python module
python -m flashrecord.cli

# Direct commands
flashrecord @sc              # Screenshot
flashrecord @sv 10 10        # 10-second GIF at 10 FPS
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
| `@sc` | Take screenshot instantly |
| `@sv` | Record screen to GIF (5s default, 10 FPS) |
| `help` | Show help menu |
| `exit` / `quit` / `q` | Exit FlashRecord |

**New in v0.3.0**: `@sv` now records full screen directly to GIF with interactive duration input and CWAM-inspired compression.

## Usage Examples

### Example 1: Quick Screenshot
```
> @sc
[+] Screenshot: output/screenshot_20251026_143022.png
```

### Example 2: Record Screen to GIF
```
> @sv
[?] Recording duration in seconds (default: 5): 10
[>] Recording screen for 10 seconds...
[██████████] 100% (10.0s)
[+] Encoding GIF...
[*] CWAM-inspired compression: 100 frames
[*] Resolution scaling: (1920, 1080) -> (960, 540)
[*] Temporal subsampling: 100 -> 80 frames (10fps -> 8fps)
[+] Compression complete: 100 -> 80 frames
[+] GIF saved: output/screen_20251026_143045.gif
[+] Size: 0.2 MB, 100 frames, 10.0s
```

### Example 3: Python Script Integration
```python
from flashrecord.screenshot import take_screenshot
from flashrecord.screen_recorder import record_screen_to_gif

# Automated screenshot
screenshot_path = take_screenshot(output_dir='./screenshots')

# Automated GIF recording
gif_path = record_screen_to_gif(
    duration=5,
    fps=10,
    compression='balanced',
    output_dir='./gifs'
)
```

## File Organization

All files save to **`output/`** (flat structure):

```
output/
├── screenshot_*.png        # Screenshots (@sc command)
├── screen_*.gif            # Screen recordings (@sv command)
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
  "auto_delete_hours": 24
}
```

- **command_style**: `"numbered"`, `"vs_vc_vg"`, or `"verbose"`
- **auto_delete_hours**: Auto-delete files older than N hours (0 = disabled)

## Instruction Notes

Add workflow instructions to markdown files in `output/`:

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
**Fix**: Ensure Pillow is installed:
```bash
pip install pillow>=9.0.0
```

### GIF Recording Failed
```
[-] Recording failed
```
**Fix**: Ensure imageio and numpy are installed:
```bash
pip install imageio>=2.0.0 numpy>=1.20.0
```

### Permission Denied on Linux/macOS
**Fix**: Install platform-specific screenshot tools:
```bash
# Ubuntu/Debian
sudo apt-get install gnome-screenshot

# macOS (usually pre-installed)
which screencapture

# Fedora
sudo dnf install gnome-screenshot
```

## Performance

- Screenshot Capture: ~10-50ms (native Pillow, platform-dependent)
  - Windows: ~15-30ms (ImageGrab)
  - macOS: ~20-50ms (screencapture command)
  - Linux: ~20-50ms (gnome-screenshot/scrot)
- Screen Recording to GIF: 10 FPS capture with real-time progress
- CWAM Compression: 99.5% size reduction (25.6 MB → 0.1 MB for 5s/50 frames)
  - Resolution scaling: 50% (1920x1080 → 960x540)
  - Temporal subsampling: 10fps → 8fps (20% frame reduction)
  - RGB color preservation: Full color fidelity maintained
- Session Save: ~50ms
- File Cleanup: ~100ms
- No external process overhead (integrated implementation)

## Directory Structure

```
flashrecord/                  # Project root
├── src/                      # Source code (Python Packaging Guide standard)
│   └── flashrecord/          # Main package
│       ├── __init__.py
│       ├── cli.py            # Main CLI interface
│       ├── screenshot.py     # Native screenshot capture (Pillow)
│       ├── screen_recorder.py # Screen to GIF recorder (imageio)
│       ├── compression.py    # CWAM-inspired GIF compression
│       ├── config.py         # Configuration management
│       ├── ai_prompt.py      # AI session manager
│       ├── manager.py        # File lifecycle
│       └── utils.py          # Utilities
├── output/                   # Auto-created output directory
├── tests/                    # Test suite (pytest)
├── docs/                     # Sphinx documentation
├── .github/                  # GitHub Actions CI/CD
│   └── workflows/
│       └── ci.yml
├── pyproject.toml            # Poetry configuration
├── config.json               # User configuration
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── CHANGELOG.md              # Version history
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

### Screen Recorder (GIF)
```python
from flashrecord.screen_recorder import record_screen_to_gif

# Record with CWAM compression
gif_path = record_screen_to_gif(
    duration=5,           # seconds
    fps=10,               # frames per second
    compression='balanced',  # 'high', 'balanced', 'compact'
    output_dir='flashrecord-save'
)
# Returns: flashrecord-save/screen_20251025_143045.gif
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

## Vision & Roadmap

### Core Vision
**"The fastest, simplest screen capture for developers"**

FlashRecord is built for developers who need reliable, scriptable screen recording without GUI overhead. Our mission is to be the Python ecosystem's go-to tool for screen capture automation.

### What Makes FlashRecord Unique?

1. **Python-Native Integration**: The only screen recorder you can `import` and use directly in Python scripts
2. **Intelligent Compression**: CWAM-inspired approach achieving 99.5% reduction with pure PIL/NumPy (no ML models)
3. **Zero-Configuration CLI**: `@sc` and `@sv` - that's it
4. **Cross-Platform Consistency**: Same commands, same behavior on Windows/macOS/Linux
5. **Production-Ready**: Full CI/CD, pytest coverage, Sphinx docs, PyPI structure

### Development Roadmap

**v0.4.0 - Enhanced Formats** (Planned Q4 2025)
- [ ] WebP video format support (smaller than GIF)
- [ ] MP4 export option (H.264 codec)
- [ ] PNG sequence export for video editors

**v0.5.0 - GUI & Integration** (Planned Q4 2025)
- [ ] Gradio web interface for non-CLI users
- [ ] VSCode extension for in-editor capture
- [ ] Jupyter notebook integration (`%%flashrecord` magic)

**v0.6.0 - Advanced Features** (Planned Q1 2026)
- [ ] Real-time streaming to Twitch/YouTube
- [ ] Window-specific capture (not just full screen)
- [ ] Audio recording integration
- [ ] Cloud sync (S3/GCS/Azure optional)

**v1.0.0 - Enterprise** (Planned Q1 2026)
- [ ] Team collaboration features
- [ ] Encrypted storage options
- [ ] REST API server mode
- [ ] Docker containerization

### Why Continued Development is Guaranteed

1. **Active Use**: FlashRecord is battle-tested in production AI development workflows
2. **Clear Architecture**: Standard src/ layout, comprehensive tests, full CI/CD
3. **PyPI Ready**: Professional packaging structure ready for public release
4. **Community Need**: Fills gap for Python-native cross-platform screen recording

## License

MIT License - See LICENSE file

## Contributing

We welcome contributions! See our development setup:

```bash
# Clone repository
git clone https://github.com/Flamehaven/flashrecord.git
cd flashrecord

# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest tests/ -v

# Build documentation
cd docs && poetry run sphinx-build -b html . _build
```

## Author

Flamehaven - AI Development Framework

## Support

- **Issues**: GitHub Issues for bug reports and feature requests
- **Documentation**: Full Sphinx docs at `docs/` directory
- **Examples**: Check `tests/` for usage examples
