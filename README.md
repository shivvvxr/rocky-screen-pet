# Rocky — final Windows edition

## Start here

1. Extract this entire ZIP to a folder on your computer.
2. Open `Rocky-Final` and double-click `Rocky.exe`.
3. Keep `Rocky.exe` and `_internal` together.

Python is included in the executable's runtime. You do not need to install
Python to run this packaged app. The `Source` folder is for editing and rebuilding.

## What Rocky does

- Walks around screen edges, climbs walls, jumps, and parachutes on high jumps.
- Uses your six transparent character images for standing, walking, and dancing.
- Shows a translucent cyan-and-amber terminal, matching speech bubbles, and a
  matching parachute with cyan canopy seams and amber suspension details.
- Dances, bounces, spins, peeks, and wiggles in place while the terminal is open.
- Displays a phrase with each dance; assistant messages are named ROCKY.
- Opens Settings inside the terminal and hides routine system notices.

## Controls

| Action | Control |
| --- | --- |
| Open or hide terminal | Click Rocky or use the tray icon |
| Move Rocky | Drag him; he snaps to the nearest screen edge |
| Dance, jump, sleep, wake, quit | Right-click Rocky or the tray icon |
| Recover Rocky after a display change | Tray menu → Bring Rocky back |
| Move terminal | Drag its header |
| Resize terminal | Drag its bottom-right grip |
| Send prompt | Enter |
| Add a line to prompt | Shift+Enter |
| Clear visible transcript | Ctrl+L |
| Start a fresh conversation while idle | Ctrl+N |
| Copy selected output or whole transcript | Ctrl+Shift+C or Copy log |
| Close Settings or hide terminal | Escape |

Closing the terminal keeps Rocky running. Use Quit Rocky to exit the app.
Sleep and dragging pause new antics. Parachuting happens during qualifying high
jumps; the terminal-open bounces are small animations in place.

## Set up AI chat

Install and sign in to Codex CLI or Claude Code CLI on your own computer.
The CLI tools and account sign-ins are separate from this package.
Open Settings, select the backend, and choose the working folder. Leave Model
blank to use the CLI default, or enter a model available to your account.
The backend is selectable even though assistant replies are labeled ROCKY.

Codex uses workspace write access. Claude uses its dontAsk permission mode.
Full computer access enables the unrestricted execution option from the original
app. Settings can be viewed during a task; edit them after the task ends.
Use Stop to cancel a task and New chat to reset the conversation.

## Where settings and history live

Settings use the Windows user's Qt settings store at
`HKEY_CURRENT_USER\Software\AgentRocky\RockyWindows`.
Rocky's transcript is kept in memory until New chat or app exit. Claude resumes
its CLI session between prompts; Codex receives the last 12 conversation turns.
The CLI tools may keep their own records. Personal settings and CLI sign-ins
are not included in this release ZIP.

## What each file does

`FILE-GUIDE.md` has one row for **every file included in this ZIP**, including
each runtime DLL, Qt plugin, translation, sprite, and source file. Start with:

| File or folder | Purpose |
| --- | --- |
| `Rocky.exe` | Ready-to-run Windows app |
| `_internal/` | Python, Qt, image assets, and supporting runtime files |
| `Source/rocky_windows/app.py` | Windows UI, themed drawing, animation, movement, Settings, tray controls |
| `Source/rocky_windows/session.py` | CLI discovery, process lifecycle, prompts, streamed responses, cancellation |
| `Source/agentrocky/*.png` | Six editable character images |
| `Source/launch_windows.py` | Executable entry point and startup error logging |
| `Source/Run Rocky.cmd` | Source launcher that checks/installs PySide6 |
| `Source/build_windows.ps1` | Builds a new executable and its runtime folder |
| `Source/package_windows.py` | Creates this documented final release ZIP |
| `Source/tests/test_windows.py` | Offline session, movement, and Settings regression checks |

The runtime contains indirect Qt dependencies and compatibility plugins as well
as modules used directly by Rocky. Keep the supplied `_internal` folder intact.

## Edit the character or rebuild

For source development, install Python 3.11 or newer with pip. Open a terminal
in `Source` and run:

```powershell
python -m pip install -r requirements.txt
python -m rocky_windows
```

Replace `Source/agentrocky/stand.png`, `walkleft1.png`, `walkleft2.png`,
`jazz1.png`, `jazz2.png`, and `jazz3.png`. Keep the filenames, transparent
backgrounds, and consistent image sizes. The parachute and speech bubbles are
drawn in `app.py`; they do not need extra PNG files.

Build and package from the `Source` folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
python package_windows.py
```

The build produces `Source/dist/Rocky/Rocky.exe`. The packaging script produces
`Source/Rocky-Final-Windows.zip`, with the app, current source, and file guide.
Quit a running copy of the executable before rebuilding its folder.

## Troubleshooting and checks

- If chat reports a missing CLI, install it, sign in, and restart Rocky.
- If Settings has disabled fields, finish or stop the current task first.
- If the packaged app fails at startup, check
  `%LOCALAPPDATA%\AgentRocky\startup-error.log`.
- If Windows loses Rocky after a monitor change, use Bring Rocky back.
- Run `Rocky.exe --smoke-test` for a short offline startup and UI check.
- From `Source`, run `python -m unittest discover -s tests -v` for offline
  regression checks, or `python -m rocky_windows --smoke-test` for the UI check.

The final build was checked with the offline suite, a rendered parachute
preview, the executable startup check, and ZIP integrity verification.
Live AI responses depend on the installed CLI, its configuration, and sign-in.
