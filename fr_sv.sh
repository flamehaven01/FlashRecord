#!/bin/bash
# FlashRecord Screen Recording Wrapper for Linux/macOS
# Usage: ./fr_sv.sh [duration] [fps]
# Examples:
#   ./fr_sv.sh           - Interactive mode
#   ./fr_sv.sh 5         - 5 seconds, 10 fps (default)
#   ./fr_sv.sh 10 20     - 10 seconds, 20 fps

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

# Parse arguments
DURATION="${1:-5}"
FPS="${2:-10}"

# Validate numeric arguments
if ! [[ "$DURATION" =~ ^[0-9]+$ ]] || ! [[ "$FPS" =~ ^[0-9]+$ ]]; then
    echo "[-] Error: Duration and FPS must be numeric"
    echo "[*] Usage: ./fr_sv.sh [duration] [fps]"
    exit 1
fi

# Run flashrecord with GIF recording command
echo "[*] Recording screen for ${DURATION}s at ${FPS}fps..."
python3 -c "
from flashrecord.screen_recorder import record_screen_to_gif
from flashrecord.config import Config
config = Config()
result = record_screen_to_gif(duration=$DURATION, fps=$FPS, output_dir=config.save_dir)
if result:
    print(f'[+] GIF saved: {result}')
else:
    print('[-] Recording failed')
"
