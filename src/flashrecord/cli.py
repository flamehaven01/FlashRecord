"""
FlashRecord CLI v0.3.4
Simple screen capture and animated GIF recording
v0.3.4: Added PNG compression support for @sc command
"""

from .ai_prompt import AIPromptManager
from .config import Config
from .install import run_setup_if_needed
from .screen_recorder import record_screen_to_gif
from .screenshot import take_screenshot


class FlashRecordCLI:
    """FlashRecord CLI interface"""

    def __init__(self):
        self.config = Config()
        self.ai_manager = AIPromptManager()

    def show_help(self):
        """Show help"""
        print("\n[*] FlashRecord v0.3.4 - Screen Capture & GIF Recording")
        print("[*] Commands:")
        print("    @sc           - Take screenshot (PNG, optimized)")
        print("    @sc -c        - Take screenshot (compressed, balanced)")
        print("    @sc -c high   - Take screenshot (70% scale, ~50% reduction)")
        print("    @sc -c compact- Take screenshot (30% scale, ~90% reduction)")
        print("    @sv           - Record screen to GIF (interactive)")
        print("    help          - Show this help")
        print("    exit          - Quit\n")

    def _display_instruction_notes(self):
        """Print instruction snippets loaded from markdown files."""
        notes = self.ai_manager.get_instruction_notes()
        if not notes:
            return

        print("[*] Instruction notes loaded from markdown:")
        order = ["codex", "gemini", "claude", "general"]
        for model in order:
            content = notes.get(model)
            if not content:
                continue
            title = model.capitalize()
            print(f"--- {title} ---")
            print(content.strip())
            print("")

    def handle_screenshot(self, compress=False, quality="balanced"):
        """
        Handle @sc command with optional compression

        Args:
            compress: Enable compression (default: False)
            quality: Compression quality - 'high', 'balanced', 'compact'
        """
        # Show compression info if enabled
        if compress:
            quality_info = {
                "high": "70% scale, ~50% size reduction",
                "balanced": "50% scale, ~75% size reduction",
                "compact": "30% scale, ~90% size reduction",
            }
            print(f"[*] Compression: {quality} ({quality_info.get(quality, 'balanced')})")

        result = take_screenshot(compress=compress, quality=quality)
        if result:
            print(f"[+] Screenshot: {result}")
        else:
            print("[-] Screenshot failed")

    def handle_screenshot_with_args(self, cmd):
        """
        Parse @sc command with compression arguments

        Examples:
            @sc -c         -> balanced compression
            @sc -c high    -> high quality compression
            @sc -c compact -> maximum compression
        """
        parts = cmd.strip().lower().split()

        compress = False
        quality = "balanced"

        if len(parts) >= 2 and parts[1] == "-c":
            compress = True
            if len(parts) >= 3 and parts[2] in ["high", "balanced", "compact"]:
                quality = parts[2]

        self.handle_screenshot(compress=compress, quality=quality)

    def handle_screen_record(self):
        """Handle @sv command - Auto/Manual mode with options"""
        try:
            # Ask if user wants to change defaults
            change = input("[?] Auto mode/5sec/10fps - Change settings? (y/n): ").strip().lower()

            if change != "y":
                # Quick mode: use defaults
                result = record_screen_to_gif(duration=5, fps=10, output_dir=self.config.save_dir)
                if not result:
                    print("[-] GIF recording failed")
                return

            # Mode selection
            print("\n[*] Recording Mode:")
            print("    1 - Auto mode (timer-based)")
            print("    2 - Manual mode (start/stop control)")
            mode = input("[?] Select (1-2): ").strip()

            if mode == "2":
                # Manual mode
                self._manual_recording_mode()
            else:
                # Auto mode with options
                self._auto_recording_mode()

        except KeyboardInterrupt:
            print("\n[-] Recording cancelled")
        except Exception as e:
            print(f"[-] Error: {str(e)}")

    def _auto_recording_mode(self):
        """Auto mode with duration and FPS selection"""
        # Duration selection
        print("\n[*] Recording Duration:")
        print("    1 - 5 seconds")
        print("    2 - 7 seconds")
        print("    3 - 10 seconds")
        duration_choice = input("[?] Select (1-3): ").strip()

        duration_map = {"1": 5, "2": 7, "3": 10}
        duration = duration_map.get(duration_choice, 5)

        # FPS selection
        print("\n[*] FPS (Frames Per Second):")
        print("    1 - 10 fps (smaller file)")
        print("    2 - 20 fps (balanced)")
        print("    3 - 30 fps (smoother)")
        fps_choice = input("[?] Select (1-3): ").strip()

        fps_map = {"1": 10, "2": 20, "3": 30}
        fps = fps_map.get(fps_choice, 10)

        # Record
        print(f"\n[>] Auto mode: {duration}sec, {fps}fps")
        result = record_screen_to_gif(duration=duration, fps=fps, output_dir=self.config.save_dir)

        if not result:
            print("[-] GIF recording failed")

    def _manual_recording_mode(self):
        """Manual mode with start/stop control"""
        import os

        from .screen_recorder import ScreenRecorder
        from .utils import get_timestamp

        print("\n[*] Manual Recording Mode")
        print("[*] Commands:")
        print("    1 - Start recording")
        print("    2 - Stop recording")
        print("    3 - Record again (discard previous)")
        print("    4 - Save and exit")

        recorder = ScreenRecorder(fps=10)

        while True:
            cmd = input("\n> ").strip()

            if cmd == "1":
                if recorder.is_recording:
                    print("[-] Already recording")
                else:
                    recorder.start_recording(duration=None)  # No auto-stop
                    print("[>] Recording started... (Press 2 to stop)")

            elif cmd == "2":
                if not recorder.is_recording:
                    print("[-] Not recording")
                else:
                    recorder.stop_recording()
                    stats = recorder.get_stats()
                    print(
                        f"[+] Recording stopped. {stats['frame_count']} frames captured ({stats['duration']:.1f}s)"
                    )
                    print("[*] Commands: 3-Record again, 4-Save and exit")

            elif cmd == "3":
                if recorder.is_recording:
                    recorder.stop_recording()
                recorder.frames = []
                print("[*] Ready to record again. Press 1 to start.")

            elif cmd == "4":
                if recorder.is_recording:
                    recorder.stop_recording()

                if not recorder.frames:
                    print("[-] No frames to save")
                    break

                # Save GIF
                timestamp = get_timestamp()
                filename = f"screen_{timestamp}.gif"
                filepath = os.path.join(self.config.save_dir, filename)

                print("[+] Encoding GIF...")
                if recorder.save_gif(filepath):
                    stats = recorder.get_stats()
                    file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                    print(f"[+] GIF saved: {filepath}")
                    print(
                        f"[+] Size: {file_size:.1f} MB, {stats['frame_count']} frames, {stats['duration']:.1f}s"
                    )
                else:
                    print("[-] Failed to save GIF")
                break

            else:
                print("[-] Invalid command. Use 1-4")

    def map_command(self, cmd):
        """Map user input to action"""
        cmd = cmd.strip().lower()

        # Universal commands
        if cmd in ["exit", "quit", "q"]:
            return "exit"
        if cmd == "help":
            return "help"
        if cmd == "@sc":
            return "screenshot"
        if cmd.startswith("@sc "):
            return "screenshot_compressed"
        if cmd == "@sv":
            return "gif_record"

        return "unknown"

    def run(self):
        """Main loop"""
        run_setup_if_needed()
        self.show_help()
        self._display_instruction_notes()
        print(f"[*] Save directory: {self.config.save_dir}\n")

        while True:
            try:
                cmd = input("> ").strip()
                if not cmd:
                    continue

                action = self.map_command(cmd)

                if action == "exit":
                    print("[*] Goodbye")
                    break
                elif action == "screenshot":
                    self.handle_screenshot()
                elif action == "screenshot_compressed":
                    self.handle_screenshot_with_args(cmd)
                elif action == "gif_record":
                    self.handle_screen_record()
                elif action == "help":
                    self.show_help()
                else:
                    print(f"[-] Unknown command: {cmd}")
                    print("[*] Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\n[*] Press 'exit' to quit")
            except Exception as e:
                print(f"[-] Error: {str(e)}")


def main():
    """Entry point"""
    cli = FlashRecordCLI()
    cli.run()


if __name__ == "__main__":
    main()
