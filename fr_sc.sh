#!/bin/bash
# FlashRecord Screenshot Wrapper for Linux/macOS
# Usage: ./fr_sc.sh [options]
# Options:
#   (none)      - Take optimized screenshot
#   -c          - Balanced compression (50% scale)
#   -c high     - High quality (70% scale)
#   -c compact  - Maximum compression (30% scale)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLASHRECORD_DIR="$SCRIPT_DIR/src/flashrecord"

# Check if flashrecord module exists
if [ ! -d "$FLASHRECORD_DIR" ]; then
    echo "[-] Error: flashrecord module not found at $FLASHRECORD_DIR"
    echo "[*] Please run from flashrecord project directory"
    exit 1
fi

# Set PYTHONPATH to include src/
export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"

# Run flashrecord with screenshot command
if [ "$#" -eq 0 ]; then
    # No arguments - default screenshot
    python3 -c "from flashrecord.cli import FlashRecordCLI; cli = FlashRecordCLI(); cli.handle_screenshot()"
elif [ "$1" = "-c" ]; then
    # Compression mode
    QUALITY="${2:-balanced}"
    python3 -c "from flashrecord.cli import FlashRecordCLI; cli = FlashRecordCLI(); cli.handle_screenshot(compress=True, quality='$QUALITY')"
else
    echo "[-] Unknown option: $1"
    echo "[*] Usage: ./fr_sc.sh [-c [high|balanced|compact]]"
    exit 1
fi
