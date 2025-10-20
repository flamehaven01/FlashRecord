# FlashRecord - Installation & Setup Wizard

## Initial Setup Flow

When you first run FlashRecord, an **Interactive Setup Wizard** automatically launches to configure your preferences.

```
┌─────────────────────────────────────┐
│  FlashRecord Setup Wizard           │
├─────────────────────────────────────┤
│ Step 1: Choose Command Style        │
│ Step 2: Screenshot Analysis         │
│ Step 3: GIF/Video Analysis          │
│ Step 4: Auto-Cleanup Settings       │
│ Step 5: AI Model Integration        │
│ Save Configuration                  │
│ Create Instruction Files            │
│ Done!                               │
└─────────────────────────────────────┘
```

## Setup Steps Explained

### Step 1: Command Style Selection

Choose how you want to interact with FlashRecord:

**Option 1: vs/vc/vg Style (Video Start/Stop/Gif)**
```
vs       - Start recording
vc       - Stop recording
vg       - Convert to GIF
cs       - Save to Claude
cg       - Save to Gemini
cz       - Save to Codex
```

**Option 2: Numbered Style (1/2/3)**
```
1        - Start recording
2        - Stop recording
3        - Convert to GIF
4        - Save to Claude
5        - Save to Gemini
6        - Save to Codex
```

**Option 3: Verbose Style (start/stop/gif)**
```
start    - Start recording
stop     - Stop recording
gif      - Convert to GIF
claude   - Save to Claude
gemini   - Save to Gemini
codex    - Save to Codex
```

### Step 2: Screenshot Analysis

**Do you want automatic screenshot analysis?**

- **Yes**: After taking a screenshot, you'll be prompted:
  ```
  [+] Screenshot saved: screenshot_20250115_143022.png
  Analyze this screenshot? (y/n)
  > y
  [*] Analyzing...
  [+] Analysis: This screenshot shows...
  ```

- **No**: Screenshots are saved without prompting for analysis

### Step 3: GIF/Video Analysis

**Enable analysis for generated GIFs?**

- **Yes**: After GIF conversion, offers frame-by-frame analysis
  ```
  [+] GIF created: recording_20250115_143045.gif
  Analyze this GIF? (y/n)
  > y
  [*] Analyzing frame sequence...
  [+] Analysis: This GIF shows...
  ```

- **No**: GIFs are saved without analysis

### Step 4: Auto-Cleanup Settings

**How often should old files be deleted?**

- **0** - Keep all files (no auto-cleanup)
- **24** - Delete files older than 1 day
- **72** - Delete files older than 3 days
- **168** - Delete files older than 1 week
- **Custom** - Enter custom hours

### Step 5: AI Model Integration

**Which AI models will you use?**

Select one or more:
- **Claude**
- **Gemini**
- **Codex (OpenAI)**

Wizard creates separate session files for each:
```
flashrecord-save/
├── claude.md    (Claude sessions)
├── gemini.md    (Gemini sessions)
└── codex.md     (Codex sessions)
```

## Generated Files

### After Setup Completion

**config.json** - Your preferences
```json
{
  "auto_delete_hours": 24,
  "hcap_path": "d:\\Sanctum\\hcap-1.5.0\\simple_capture.py",
  "command_style": "vs_vc_vg",
  "auto_analyze_screenshot": true,
  "auto_analyze_gif": true,
  "ai_models": ["claude", "gemini"]
}
```

**Instruction Files**
```
flashrecord-save/
└── instructions/
    ├── main.md              (Your personalized instructions)
    ├── commands.md          (Command reference)
    └── prompts/
        ├── screenshot_analysis.prompt
        └── gif_analysis.prompt     (if enabled)
```

## First Run Example

```bash
$ cd D:\Sanctum\flashrecord
$ python -m flashrecord.cli

[*] First-time setup detected...

╔═══════════════════════════════════╗
║ FlashRecord - Initial Setup Wizard║
╚═══════════════════════════════════╝

[*] Welcome to FlashRecord v0.1.0
[*] Fast Screen Recording & GIF Generator
[*] First-time setup and configuration

---------- Step 1: Choose Command Style ----------

[1] vs/vc/vg Style (Video Start/Stop/Gif)
[2] Numbered Style (1/2/3)
[3] Verbose Style (start/stop/gif)

Select style (1-3): 1
[+] Selected: vs_vc_vg style

---------- Step 2: Screenshot Analysis ----------

[*] After taking screenshots, analyze content?
[y] Yes - Analyze automatically
[n] No - Save only

Enable screenshot analysis? (y/n): y
[+] Screenshot analysis: Enabled

... (Steps 3-5) ...

======== Configuration Summary ========

[*] Your Settings:
    Command Style:          vs_vc_vg
    Screenshot Analysis:    Enabled
    GIF Analysis:           Enabled
    Auto-cleanup:           24h
    AI Models:              claude, gemini

Save this configuration? (y/n): y

[+] Configuration saved to config.json
[+] Instruction files created
[+] Setup Complete!

[*] FlashRecord is now configured and ready to use!

[*] Files created:
    - config.json (your settings)
    - flashrecord-save/instructions/main.md (instructions)
    - flashrecord-save/instructions/commands.md (reference)

[*] Next steps:
    1. Start FlashRecord: python -m flashrecord.cli
    2. Type 'help' for command list
    3. Use 'exit' to quit

[+] Happy recording!

========== FlashRecord Ready ==========

[*] FlashRecord ready
[*] Command style: vs_vc_vg
[*] Save directory: flashrecord-save
[*] Auto-delete: 24h

> vs
[>] Recording started... (press 'vc' to stop)
```

## Reconfiguring Later

### Option 1: Re-run Setup Wizard

```bash
python -c "from flashrecord.install import InstallWizard; wizard = InstallWizard(); wizard.run_wizard()"
```

### Option 2: Edit config.json Directly

```json
{
  "auto_delete_hours": 72,
  "command_style": "verbose",
  "auto_analyze_screenshot": false,
  "auto_analyze_gif": true,
  "ai_models": ["claude"]
}
```

## Generated Instruction Files

### main.md
Your personalized instruction guide with:
- Your selected command style
- Your configuration summary
- Basic workflow
- Tips and tricks
- Next steps

### commands.md
Command reference table with:
- All available commands (based on your style)
- Command descriptions
- File organization
- Navigation tips

### prompts/ (if analysis enabled)
AI analysis prompt templates:
- `screenshot_analysis.prompt` - How to analyze screenshots
- `gif_analysis.prompt` - How to analyze GIF sequences

## Command Mapping Examples

### If you chose "vs/vc/vg" style:
```
> vs          → Start recording
> vc          → Stop recording
> vg          → Convert to GIF
> cs          → Save to Claude
> help        → Show help
> exit        → Exit
```

### If you chose "numbered" style:
```
> 1           → Start recording
> 2           → Stop recording
> 3           → Convert to GIF
> 4           → Save to Claude
> help        → Show help
> exit        → Exit
```

### If you chose "verbose" style:
```
> start       → Start recording
> stop        → Stop recording
> gif         → Convert to GIF
> claude      → Save to Claude
> help        → Show help
> exit        → Exit
```

## First-Time Setup Checklist

- [x] Choose command style that matches your preference
- [x] Enable/disable screenshot analysis
- [x] Enable/disable GIF analysis
- [x] Set auto-cleanup frequency
- [x] Select AI models to use
- [x] Review configuration summary
- [x] Save configuration
- [x] Instruction files created
- [x] Ready to use!

## Tips

1. **Command Style**: Choose the one that feels natural to you
   - vs/vc/vg: Short, technical
   - 1/2/3: Numbered, simple
   - start/stop/gif: Verbose, descriptive

2. **Analysis**: Start with enabled and disable if you don't need it
   - Screenshot analysis is useful for documentation
   - GIF analysis can identify workflow patterns

3. **Auto-cleanup**: Start with 24h to test
   - Increase to 72h+ if you want to keep files longer
   - Set to 0 to disable cleanup

4. **AI Models**: Add all you might use
   - You can always add/remove later
   - Each gets its own session file

## Reinstalling Configuration

To reset all settings:

```bash
# Delete config and instructions
rm config.json
rm -rf flashrecord-save/instructions

# Restart - setup wizard runs again
python -m flashrecord.cli
```

---

**Setup Time**: ~2-3 minutes
**Questions**: Check README.md for more info
**Support**: Refer to flashrecord-save/instructions/ files
