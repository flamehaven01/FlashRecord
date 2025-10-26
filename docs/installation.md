# Installation

## From PyPI

```bash
pip install flashrecord
```

## From Source

```bash
git clone https://github.com/Flamehaven/flashrecord.git
cd flashrecord
poetry install
```

## Docker

```bash
docker pull flamehaven/flashrecord:latest
```

## Platform-Specific Notes

### Windows

No additional dependencies required. Screenshot capture uses PIL ImageGrab.

### macOS

Screenshot capture uses the built-in `screencapture` command.

### Linux

Install one of the following:

```bash
# Ubuntu/Debian
sudo apt-get install gnome-screenshot

# Or scrot
sudo apt-get install scrot

# Or ImageMagick
sudo apt-get install imagemagick
```

## Verification

```bash
flashrecord --version
```
