"""
FlashRecord CLI v0.3.0
Simple screen capture and animated GIF recording
"""

from .screenshot import take_screenshot
from .screen_recorder import record_screen_to_gif
from .ai_prompt import AIPromptManager
from .config import Config
from .install import run_setup_if_needed


class FlashRecordCLI:
    """FlashRecord CLI interface"""

    def __init__(self):
        self.config = Config()
        self.ai_manager = AIPromptManager()

    def show_help(self):
        """Show help"""
        print("\n[*] FlashRecord v0.3.0 - Screen Capture & GIF Recording")
        print("[*] Commands:")
        print("    @sc - Take screenshot (PNG)")
        print("    @sv - Record screen to GIF (interactive)")
        print("    help - Show this help")
        print("    exit - Quit\n")

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

    def handle_screenshot(self):
        """Handle @sc command"""
        result = take_screenshot()
        if result:
            print(f"[+] Screenshot: {result}")
        else:
            print("[-] Screenshot failed")

    def handle_screen_record(self):
        """Handle @sv command - Interactive GIF recording"""
        try:
            # Ask for duration
            duration_input = input("[?] Recording duration in seconds (default: 5): ").strip()

            if duration_input:
                try:
                    duration = int(duration_input)
                    if duration < 1 or duration > 60:
                        print("[-] Duration must be between 1-60 seconds. Using default: 5")
                        duration = 5
                except ValueError:
                    print("[-] Invalid input. Using default: 5 seconds")
                    duration = 5
            else:
                duration = 5

            # Record screen to GIF
            result = record_screen_to_gif(
                duration=duration,
                fps=10,
                output_dir=self.config.save_dir
            )

            if not result:
                print("[-] GIF recording failed")

        except KeyboardInterrupt:
            print("\n[-] Recording cancelled")
        except Exception as e:
            print(f"[-] Error: {str(e)}")

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
