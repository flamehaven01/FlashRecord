"""
Minimal Setup Wizard - Command style selection only
Iceberg design: simple surface, minimal code
"""

import os
import json


class InstallWizard:
    """Minimal installation - only command style selection"""

    def __init__(self):
        self.config_path = "config.json"
        self.config_data = {}

    def run_wizard(self):
        """Run minimal setup wizard"""
        self.show_welcome()
        style = self.show_command_selection()
        self.save_config(style)
        return True

    def show_welcome(self):
        """Display welcome"""
        print("\n" + "=" * 60)
        print("FlashRecord v0.1.0 - Setup".center(60))
        print("=" * 60 + "\n")

    def show_command_selection(self):
        """Choose command style"""
        print("[o] Choose Command Style:\n")
        print("[1] Speed   (1=start, 2=stop, 3=gif)")
        print("[2] Easy    (vs=start, vc=stop, vg=gif)")
        print("[3] Clear   (start, stop, gif)\n")

        while True:
            choice = input("Select (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                styles = {"1": "numbered", "2": "vs_vc_vg", "3": "verbose"}
                style = styles[choice]
                print(f"[+] Selected: {style}\n")
                return style
            print("[-] Invalid. Try again.\n")

    def save_config(self, style):
        """Save config with minimal defaults"""
        config = {
            "command_style": style,
            "auto_delete_hours": 24,
            "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py"
        }
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"[+] Config saved to {self.config_path}")


def run_setup_if_needed():
    """Run wizard if config doesn't exist"""
    if not os.path.exists("config.json"):
        wizard = InstallWizard()
        return wizard.run_wizard()
    return True
