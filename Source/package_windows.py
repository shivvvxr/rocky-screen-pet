"""Create a documented, runnable Windows release with the Windows source."""
from pathlib import Path
import zipfile


README = '''# Rocky — final Windows edition

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
`HKEY_CURRENT_USER\\Software\\AgentRocky\\RockyWindows`.
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
powershell -ExecutionPolicy Bypass -File .\\build_windows.ps1
python package_windows.py
```

The build produces `Source/dist/Rocky/Rocky.exe`. The packaging script produces
`Source/Rocky-Final-Windows.zip`, with the app, current source, and file guide.
Quit a running copy of the executable before rebuilding its folder.

## Troubleshooting and checks

- If chat reports a missing CLI, install it, sign in, and restart Rocky.
- If Settings has disabled fields, finish or stop the current task first.
- If the packaged app fails at startup, check
  `%LOCALAPPDATA%\\AgentRocky\\startup-error.log`.
- If Windows loses Rocky after a monitor change, use Bring Rocky back.
- Run `Rocky.exe --smoke-test` for a short offline startup and UI check.
- From `Source`, run `python -m unittest discover -s tests -v` for offline
  regression checks, or `python -m rocky_windows --smoke-test` for the UI check.

The final build was checked with the offline suite, a rendered parachute
preview, the executable startup check, and ZIP integrity verification.
Live AI responses depend on the installed CLI, its configuration, and sign-in.
'''

SOURCE_README = '''# Windows source

See `../README.md` for the complete user and developer guide, and
`../FILE-GUIDE.md` for every included file's role.

From this directory:

```powershell
python -m pip install -r requirements.txt
python -m rocky_windows
python -m unittest discover -s tests -v
powershell -ExecutionPolicy Bypass -File .\\build_windows.ps1
python package_windows.py
```

Edit `rocky_windows/app.py` for appearance and animation, `session.py` for CLI
communication, and `agentrocky/*.png` for character poses. Keep the six sprite
filenames unchanged. Qt and Python runtime binaries are generated by the build.
'''


def purpose(path):
    name = Path(path).name
    direct = {
        'README.md': 'User guide, setup, controls, customization, rebuild steps, and troubleshooting.',
        'FILE-GUIDE.md': 'Complete per-file inventory and purpose of every file in this release.',
        'Rocky.exe': 'Windows launcher containing the frozen Rocky application code.',
        'app.py': 'All Windows windows/widgets, Settings panel, character movement, antics, parachute, speech bubbles, and tray.',
        'session.py': 'Finds Codex/Claude, launches CLI processes, sends prompts, parses output, and stops process trees.',
        '__init__.py': 'Marks rocky_windows as an importable Python package.',
        '__main__.py': 'Allows launching with python -m rocky_windows.',
        'launch_windows.py': 'PyInstaller entry point; records startup failures in the user local app-data folder.',
        'requirements.txt': 'Declares the PySide6 dependency for running the source.',
        'Run Rocky.cmd': 'Checks Python/PySide6 and starts the app from source.',
        'build_windows.ps1': 'Installs build dependencies and bundles the Windows executable with a restricted build PATH.',
        'package_windows.py': 'Packages the built app, current Windows source, README, and complete per-file guide.',
        'test_windows.py': 'Offline regression checks for process output, failure/cancel behavior, movement, and responsive Settings.',
        '.gitignore': 'Excludes generated build output, distribution files, and Python caches from version control.',
        'stand.png': 'User-supplied transparent standing pose, also used by the terminal portrait and tray icon.',
        'walkleft1.png': 'User-supplied walking animation frame 1.',
        'walkleft2.png': 'User-supplied walking animation frame 2.',
        'jazz1.png': 'User-supplied jazz dance animation frame 1.',
        'jazz2.png': 'User-supplied jazz dance animation frame 2.',
        'jazz3.png': 'User-supplied jazz dance animation frame 3.',
        'base_library.zip': 'Frozen Python standard-library modules used by the bundled interpreter.',
        'python3.dll': 'Python stable-ABI loader used by native extension modules.',
        'python314.dll': 'Bundled Python 3.14 interpreter runtime; no separate Python installation is needed.',
        '_bz2.pyd': 'Python bzip2 compression support.',
        '_decimal.pyd': 'Python decimal arithmetic support.',
        '_hashlib.pyd': 'Python native hashing support.',
        '_lzma.pyd': 'Python LZMA compression support.',
        '_socket.pyd': 'Python operating-system socket support.',
        '_ssl.pyd': 'Python TLS support.',
        '_zstd.pyd': 'Python Zstandard compression support.',
        'select.pyd': 'Python socket/readiness polling support.',
        'unicodedata.pyd': 'Python Unicode character metadata.',
        'libcrypto-3.dll': 'OpenSSL cryptographic dependency for the bundled Python TLS/hash modules.',
        'libssl-3.dll': 'OpenSSL TLS protocol dependency for the bundled Python SSL module.',
        'opengl32sw.dll': 'Software OpenGL fallback shipped with Qt.',
        'pyside6.abi3.dll': 'Shared PySide6 binding runtime connecting Python and Qt.',
        'Shiboken.pyd': 'Python access to the Shiboken binding support library.',
        'shiboken6.abi3.dll': 'Native object/type conversion and ownership support for PySide6.',
    }
    if name in direct:
        return direct[name]
    if name.startswith(('VCRUNTIME', 'MSVCP')):
        return 'Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions.'
    if name.endswith('.qm'):
        locale = name[:-3]
        for prefix in ('qt_help_', 'qtbase_', 'qt_'):
            if locale.startswith(prefix):
                locale = locale[len(prefix):]
                break
        return 'Bundled Qt interface translation catalog for locale ' + locale + '.'
    if name.startswith('Qt6') and name.endswith('.dll'):
        module = name[3:-4]
        descriptions = {'Core': 'events, timers, settings, process handling, and shared Qt infrastructure',
                        'Gui': 'images, painting, fonts, and window integration',
                        'Widgets': 'desktop widgets and layouts', 'Network': 'Qt networking support',
                        'OpenGL': 'graphics backend support', 'Pdf': 'PDF image plugin support',
                        'Svg': 'SVG image/icon plugin support', 'Quick': 'Qt Quick graphics used by optional plugins',
                        'VirtualKeyboard': 'optional on-screen keyboard plugin support'}
        return f'Qt {module} library: ' + descriptions.get(module, 'indirect dependency support for the bundled Qt plugins') + '.'
    if name.startswith('Qt') and name.endswith('.pyd'):
        return 'Python bindings for the Qt ' + name[2:-4] + ' module.'
    if '/plugins/' in path:
        category = path.split('/plugins/', 1)[1].split('/')[0]
        categories = {'platforms': 'window-system backend', 'imageformats': 'image format loader',
                      'tls': 'TLS backend', 'styles': 'widget styling backend',
                      'iconengines': 'icon rendering backend', 'generic': 'optional input integration',
                      'platforminputcontexts': 'input-method/on-screen keyboard integration',
                      'networkinformation': 'operating-system network status integration'}
        return f'Qt {categories.get(category, category + " support plugin")}: {name}.'
    raise ValueError('Add a file description before packaging: ' + path)


def main():
    root = Path(__file__).resolve().parent
    app = root / 'dist' / 'Rocky'
    if not (app / 'Rocky.exe').is_file():
        raise SystemExit('Build the app with build_windows.ps1 first.')
    files = {p.relative_to(app).as_posix(): p for p in app.rglob('*')
             if p.is_file() and p.relative_to(app).parts[0] != 'READ ME.txt'}
    source = ['launch_windows.py', 'requirements.txt', 'Run Rocky.cmd', 'build_windows.ps1',
              'package_windows.py', '.gitignore', 'rocky_windows/__init__.py',
              'rocky_windows/__main__.py', 'rocky_windows/app.py', 'rocky_windows/session.py',
              'tests/test_windows.py']
    source += ['agentrocky/' + name + '.png' for name in
               ('stand', 'walkleft1', 'walkleft2', 'jazz1', 'jazz2', 'jazz3')]
    files.update({'Source/' + name: root / name for name in source})
    files['README.md'] = README.encode('utf-8')
    files['Source/README.md'] = SOURCE_README.encode('utf-8')
    guide_paths = sorted([*files, 'FILE-GUIDE.md'])
    guide = ['# Every included file and its work', '',
             'Paths are relative to the extracted `Rocky-Final` folder. Runtime modules',
             'include indirect dependencies collected by PyInstaller. Source files are',
             'editable; runtime binaries are generated dependencies. Keep `_internal` intact.', '',
             '| File | What it does |', '| --- | --- |']
    guide.extend(f'| `{path}` | {purpose(path)} |' for path in guide_paths)
    files['FILE-GUIDE.md'] = ('\n'.join(guide) + '\n').encode('utf-8')
    output = root / 'Rocky-Final-Windows.zip'
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, content in sorted(files.items()):
            target = 'Rocky-Final/' + name
            if isinstance(content, Path):
                archive.write(content, target)
            else:
                archive.writestr(target, content)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(guide_paths)
        assert set(archive.namelist()) == {'Rocky-Final/' + path for path in guide_paths}
    print(f'Final ZIP verified: {output}\n{len(files)} files, {output.stat().st_size / 1024 / 1024:.1f} MB')


if __name__ == '__main__':
    main()
