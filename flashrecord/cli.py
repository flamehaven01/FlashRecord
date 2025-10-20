"""
Minimal CLI - Clean, fast, simple
Iceberg: simple commands, powerful backend
"""

from .screenshot import take_screenshot
from .video_recorder import VideoRecorder
from .ai_prompt import AIPromptManager
from .config import Config
from .install import run_setup_if_needed


class FlashRecordCLI:
    """Minimal CLI interface"""

    def __init__(self):
        self.config = Config()
        self.ai_manager = AIPromptManager()
        self.video_recorder = VideoRecorder()
        self.recording = False
        self.recording_file = None

    def show_help(self):
        """Show minimal help"""
        style = self.config.command_style
        help_text = {
            "numbered": "[1]start [2]stop [3]gif [4-6]save",
            "vs_vc_vg": "[vs]start [vc]stop [vg]gif [cs/cg/cz]save",
            "verbose": "[start][stop][gif][claude/gemini/codex]"
        }
        print(f"\n[*] Commands: {help_text.get(style, 'unknown')}")
        print("[*] Universal: #sc/sc=screenshot sv=gif help exit\n")

    def _start_hint(self) -> str:
        """Return start command hint based on the active style."""
        style = self.config.command_style
        if style == "vs_vc_vg":
            return "'vs'"
        if style == "verbose":
            return "'start'"
        return "'1'"

    def _stop_hint(self) -> str:
        """Return stop command hint based on the active style."""
        style = self.config.command_style
        if style == "vs_vc_vg":
            return "'vc'"
        if style == "verbose":
            return "'stop'"
        return "'2'"

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

    def handle_command(self, action, param):
        """Handle single command"""
        if action == "screenshot":
            result = take_screenshot()
            if result:
                print(f"[+] Screenshot: {result}")
        elif action == "start":
            self.recording_file = self.video_recorder.start_recording()
            self.recording = True
            print(f"[>] Recording started... (use {self._stop_hint()} to stop)")
        elif action == "stop":
            if self.recording and self.recording_file:
                self.video_recorder.stop_recording()
                self.recording = False
                print("[+] Recording stopped")
        elif action == "gif":
            if self.recording_file:
                gif = self.video_recorder.convert_to_gif(self.recording_file)
                if gif:
                    print(f"[+] GIF: {gif}")
            else:
                print(f"[-] No recording found. Start with {self._start_hint()} first.")
        elif action == "save":
            self.ai_manager.save_session(param or "general")
            print(f"[+] Saved to {param or 'general'}.md")
        elif action == "help":
            self.show_help()
        elif action == "unknown":
            print(f"[-] Unknown: {param or 'command'}")

    def map_command(self, cmd):
        """Map user input to action"""
        cmd = cmd.strip().lower()

        # Universal commands
        if cmd in ["exit", "quit", "q"]:
            return ("exit", None)
        if cmd == "help":
            return ("help", None)
        if cmd in ["#sc", "sc"]:
            return ("screenshot", None)
        if cmd == "sv":
            return ("gif", None)

        # Style-specific
        style = self.config.command_style

        if style == "vs_vc_vg":
            mapping = {
                "vs": ("start", None), "vc": ("stop", None), "vg": ("gif", None),
                "cs": ("save", "claude"), "cg": ("save", "gemini"), "cz": ("save", "codex")
            }
        elif style == "verbose":
            mapping = {
                "start": ("start", None), "stop": ("stop", None), "gif": ("gif", None),
                "claude": ("save", "claude"), "gemini": ("save", "gemini"), "codex": ("save", "codex")
            }
        else:  # numbered
            mapping = {
                "1": ("start", None), "2": ("stop", None), "3": ("gif", None),
                "4": ("save", "claude"), "5": ("save", "gemini"), "6": ("save", "codex")
            }

        return mapping.get(cmd, ("unknown", cmd))

    def run(self):
        """Main loop"""
        run_setup_if_needed()
        self.show_help()
        self._display_instruction_notes()
        print(f"[*] Mode: {self.config.command_style} | Dir: {self.config.save_dir}\n")

        while True:
            try:
                cmd = input("> ").strip()
                if not cmd:
                    continue

                action, param = self.map_command(cmd)

                if action == "exit":
                    print("[*] Goodbye")
                    break
                else:
                    self.handle_command(action, param)

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
