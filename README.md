<p align="center">
  <img src="git-assets/ricewm_b_logo.png" width="150" alt="RiceWM logo">
</p>

A lightweight, customizable window management utility for Windows — fast keyboard-driven window switching, virtual desktop navigation with animated notifications, and global hotkey controls, all running quietly from the system tray.

-- screenshot

## Requirements

- **Windows 10 or Windows 11** (64-bit)
- Administrator privileges (required for global hotkey suppression to work reliably)

RiceWM relies on Windows-specific APIs (virtual desktops, low-level keyboard hooks) and is **not compatible with Linux or macOS**.

## Features

- **Global hotkeys** — control windows, virtual desktops, and app behavior from anywhere.
- **Window search & switch panel** — a fast, keyboard-navigable popup to find and jump to any open window.
- **Virtual desktop navigation** — move between desktops, create new ones, and delete the current one with automatic fallback handling, complete with a themeable animated on-screen notifier.
- **Window controls** — minimize, maximize, restore, and close the focused window via hotkey.
- **Tray-first design** — runs entirely from the system tray with no persistent main window, so it stays out of your way.
- **Fully themeable** — customize colors, sizing, and animations via a JSON theme file.
- **Configurable keymap** — remap every hotkey to your preference via a simple JSON config.

## Installation

1. Download the latest release from the [Releases] page.
2. Extract the `RiceWM` folder anywhere you like.
3. Run `RiceWM.exe`.

> **Note:** RiceWM requests administrator privileges on launch. This is required for global hotkey suppression to work reliably across all applications (similar to how AutoHotkey scripts operate).

> **Antivirus note:** Some antivirus software may flag RiceWM on first run due to its use of global keyboard hooks — this pattern is also used by keyloggers, so heuristic scanners sometimes react to it. RiceWM is not currently code-signed (see [Roadmap]), so Windows SmartScreen may also show an "unrecognized app" warning. This is expected for an early-stage, unsigned open-source tool — you're welcome to review the source yourself before running it.

On first launch, RiceWM automatically creates its config directory at `%USERPROFILE%\.config\riceWM` and populates it with default configuration, theme, and keymap files.

## Default Hotkeys

| Action                          | Hotkey                   |
| ------------------------------- | ------------------------ |
| Toggle window search panel      | `Ctrl + Alt + \`         |
| Close search panel              | `Esc`                    |
| Select previous window          | `Ctrl + W`               |
| Select next window              | `Ctrl + S`               |
| Virtual desktop: go left        | `Ctrl + Alt + A`         |
| Virtual desktop: go right       | `Ctrl + Alt + D`         |
| Virtual desktop: create new     | `Ctrl + Shift + Alt + N` |
| Virtual desktop: delete current | `Ctrl + Shift + Alt + Q` |
| Maximize focused window         | `Ctrl + Alt + W`         |
| Minimize focused window         | `Ctrl + Alt + X`         |
| Close focused window            | `Ctrl + Alt + Q`         |
| Restore focused window          | `Ctrl + Alt + S`         |
| Restart Application             | `Ctrl + Alt + F12`       |

All hotkeys are fully remappable — see [Configuration]() below.

## Commands

Typed into the window search panel, prefixed with '`:`':

| Command            | Description                        |
| ------------------ | ---------------------------------- |
| `:quit`            | Quits the application              |
| `:open-theme`      | Opens the active `theme.json` file |
| `:open-app-config` | Opens `app.toml`                   |
| `:open-config`     | Opens active `config.json`         |
| `:open-keymap`     | Opens the keymap file              |
| `:restart`         | Restarts the application           |
## Configuration

RiceWM stores its config at `%USERPROFILE%\.config\riceWM\`:

```
.config/riceWM/
├── app.toml                 # general app settings
├── key_map.json             # hotkey bindings
├── config/
│   └── default_config.json  # behavior and configs
└── themes/
    └── default_theme.json   # colors, animations, sizing
```

Edit these files directly, then restart the application with `Ctrl + Alt + F12` (or the key-bind given in your keymap) to apply changes.

## Building from Source

**Requirements:**

- Python 3.13+
- Windows 10/11

```bash
git clone https://github.com/darco-ctrl/riceWM.git
cd RiceWM
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Building an executable

```bash
pyinstaller --clean main.spec
```

The built application will be output to `dist/RiceWM/`.

## Uninstalling

RiceWM doesn't currently ship with an installer/uninstaller, so removal is manual. Two locations to clean up:

1. **Quit the app first** — right-click the tray icon and choose Quit, type `:quit` in the search panel, or end `RiceWM.exe` via Task Manager if it's unresponsive.
2. **Delete the application folder** — the entire folder you extracted/built RiceWM into, e.g. `dist\RiceWM\`. This includes `RiceWM.exe` and the `_internal\` folder PyInstaller generates alongside it (bundled dependencies, `assets/`, `default_config/`) — deleting the parent folder removes both in one go.
3. **Delete the config folder** — `%USERPROFILE%\.config\riceWM\`, which holds your keymap, themes, and app config. Skip this step if you plan to reinstall later and want to keep your settings.

## Tech Stack

- **Python 3.13**
- **PySide6** — UI, tray icon, and animations
- **keyboard** — global hotkey registration with input suppression
- **pynput** — scoped, panel-local hotkey handling
- **pyvda** — Windows virtual desktop control

## Tested On

- Windows 11
- Windows 10

## Roadmap / Future Plans

- Code-signing the executable to reduce antivirus/SmartScreen false positives and improve trust
- Proper `.msi` installer (and matching uninstaller) instead of a manual extract-and-run folder
- General stability and polish as the project moves toward a trusted, production-ready release

## Contributing

Issues and pull requests are welcome. This is an early-stage project (v1) under active development — expect breaking changes between versions.

## Acknowledgments

RiceWM is built on top of these excellent open-source projects:

- [PySide6](https://pypi.org/project/PySide6/) — Qt for Python, used for the UI, tray icon, and animations
- [keyboard](https://github.com/boppreh/keyboard) — global hotkey registration with input suppression
- [pynput](https://github.com/moses-palmer/pynput) — scoped, panel-local input handling
- [pyvda](https://github.com/mrob95/pyvda) — Windows virtual desktop control via COM
- [PyInstaller](https://pyinstaller.org/) — packaging RiceWM into a standalone executable

## License

RiceWM is licensed under the [MIT License]().

## Feedback & Support

Found a bug, have a feature idea, or just want to chat about the project? Reach out to me through either :D :

- **Discord:** [discord.gg/PLACEHOLDER]()
- **Email:** [ricewm]

You can also open an issue directly on GitHub for bugs or feature requests.

## About

This project was made because I hated `alt+tab` and used `.ahk` to customize hotkey to switch between virtual desktop and stuff and I had 5 virtual desktpp opened and wouldn't know where a window is that's how I got idea of making window search,

Btw , love `.ahk` when i said above don't take it as bad its amazing :D
