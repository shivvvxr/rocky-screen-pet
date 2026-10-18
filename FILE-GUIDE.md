# Every included file and its work

Paths are relative to the extracted `Rocky-Final` folder. Runtime modules
include indirect dependencies collected by PyInstaller. Source files are
editable; runtime binaries are generated dependencies. Keep `_internal` intact.

| File | What it does |
| --- | --- |
| `FILE-GUIDE.md` | Complete per-file inventory and purpose of every file in this release. |
| `README.md` | User guide, setup, controls, customization, rebuild steps, and troubleshooting. |
| `Rocky.exe` | Windows launcher containing the frozen Rocky application code. |
| `Source/.gitignore` | Excludes generated build output, distribution files, and Python caches from version control. |
| `Source/README.md` | User guide, setup, controls, customization, rebuild steps, and troubleshooting. |
| `Source/Run Rocky.cmd` | Checks Python/PySide6 and starts the app from source. |
| `Source/agentrocky/jazz1.png` | User-supplied jazz dance animation frame 1. |
| `Source/agentrocky/jazz2.png` | User-supplied jazz dance animation frame 2. |
| `Source/agentrocky/jazz3.png` | User-supplied jazz dance animation frame 3. |
| `Source/agentrocky/stand.png` | User-supplied transparent standing pose, also used by the terminal portrait and tray icon. |
| `Source/agentrocky/walkleft1.png` | User-supplied walking animation frame 1. |
| `Source/agentrocky/walkleft2.png` | User-supplied walking animation frame 2. |
| `Source/build_windows.ps1` | Installs build dependencies and bundles the Windows executable with a restricted build PATH. |
| `Source/launch_windows.py` | PyInstaller entry point; records startup failures in the user local app-data folder. |
| `Source/package_windows.py` | Packages the built app, current Windows source, README, and complete per-file guide. |
| `Source/requirements.txt` | Declares the PySide6 dependency for running the source. |
| `Source/rocky_windows/__init__.py` | Marks rocky_windows as an importable Python package. |
| `Source/rocky_windows/__main__.py` | Allows launching with python -m rocky_windows. |
| `Source/rocky_windows/app.py` | All Windows windows/widgets, Settings panel, character movement, antics, parachute, speech bubbles, and tray. |
| `Source/rocky_windows/session.py` | Finds Codex/Claude, launches CLI processes, sends prompts, parses output, and stops process trees. |
| `Source/tests/test_windows.py` | Offline regression checks for process output, failure/cancel behavior, movement, and responsive Settings. |
| `_internal/PySide6/MSVCP140.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/PySide6/MSVCP140_1.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/PySide6/MSVCP140_2.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/PySide6/Qt6Core.dll` | Qt Core library: events, timers, settings, process handling, and shared Qt infrastructure. |
| `_internal/PySide6/Qt6Gui.dll` | Qt Gui library: images, painting, fonts, and window integration. |
| `_internal/PySide6/Qt6Network.dll` | Qt Network library: Qt networking support. |
| `_internal/PySide6/Qt6OpenGL.dll` | Qt OpenGL library: graphics backend support. |
| `_internal/PySide6/Qt6Pdf.dll` | Qt Pdf library: PDF image plugin support. |
| `_internal/PySide6/Qt6Qml.dll` | Qt Qml library: indirect dependency support for the bundled Qt plugins. |
| `_internal/PySide6/Qt6QmlMeta.dll` | Qt QmlMeta library: indirect dependency support for the bundled Qt plugins. |
| `_internal/PySide6/Qt6QmlModels.dll` | Qt QmlModels library: indirect dependency support for the bundled Qt plugins. |
| `_internal/PySide6/Qt6QmlWorkerScript.dll` | Qt QmlWorkerScript library: indirect dependency support for the bundled Qt plugins. |
| `_internal/PySide6/Qt6Quick.dll` | Qt Quick library: Qt Quick graphics used by optional plugins. |
| `_internal/PySide6/Qt6Svg.dll` | Qt Svg library: SVG image/icon plugin support. |
| `_internal/PySide6/Qt6VirtualKeyboard.dll` | Qt VirtualKeyboard library: optional on-screen keyboard plugin support. |
| `_internal/PySide6/Qt6Widgets.dll` | Qt Widgets library: desktop widgets and layouts. |
| `_internal/PySide6/QtCore.pyd` | Python bindings for the Qt Core module. |
| `_internal/PySide6/QtGui.pyd` | Python bindings for the Qt Gui module. |
| `_internal/PySide6/QtNetwork.pyd` | Python bindings for the Qt Network module. |
| `_internal/PySide6/QtWidgets.pyd` | Python bindings for the Qt Widgets module. |
| `_internal/PySide6/VCRUNTIME140.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/PySide6/VCRUNTIME140_1.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/PySide6/opengl32sw.dll` | Software OpenGL fallback shipped with Qt. |
| `_internal/PySide6/plugins/generic/qtuiotouchplugin.dll` | Qt optional input integration: qtuiotouchplugin.dll. |
| `_internal/PySide6/plugins/iconengines/qsvgicon.dll` | Qt icon rendering backend: qsvgicon.dll. |
| `_internal/PySide6/plugins/imageformats/qgif.dll` | Qt image format loader: qgif.dll. |
| `_internal/PySide6/plugins/imageformats/qicns.dll` | Qt image format loader: qicns.dll. |
| `_internal/PySide6/plugins/imageformats/qico.dll` | Qt image format loader: qico.dll. |
| `_internal/PySide6/plugins/imageformats/qjpeg.dll` | Qt image format loader: qjpeg.dll. |
| `_internal/PySide6/plugins/imageformats/qpdf.dll` | Qt image format loader: qpdf.dll. |
| `_internal/PySide6/plugins/imageformats/qsvg.dll` | Qt image format loader: qsvg.dll. |
| `_internal/PySide6/plugins/imageformats/qtga.dll` | Qt image format loader: qtga.dll. |
| `_internal/PySide6/plugins/imageformats/qtiff.dll` | Qt image format loader: qtiff.dll. |
| `_internal/PySide6/plugins/imageformats/qwbmp.dll` | Qt image format loader: qwbmp.dll. |
| `_internal/PySide6/plugins/imageformats/qwebp.dll` | Qt image format loader: qwebp.dll. |
| `_internal/PySide6/plugins/networkinformation/qnetworklistmanager.dll` | Qt operating-system network status integration: qnetworklistmanager.dll. |
| `_internal/PySide6/plugins/platforminputcontexts/qtvirtualkeyboardplugin.dll` | Qt input-method/on-screen keyboard integration: qtvirtualkeyboardplugin.dll. |
| `_internal/PySide6/plugins/platforms/qdirect2d.dll` | Qt window-system backend: qdirect2d.dll. |
| `_internal/PySide6/plugins/platforms/qminimal.dll` | Qt window-system backend: qminimal.dll. |
| `_internal/PySide6/plugins/platforms/qoffscreen.dll` | Qt window-system backend: qoffscreen.dll. |
| `_internal/PySide6/plugins/platforms/qwindows.dll` | Qt window-system backend: qwindows.dll. |
| `_internal/PySide6/plugins/styles/qmodernwindowsstyle.dll` | Qt widget styling backend: qmodernwindowsstyle.dll. |
| `_internal/PySide6/plugins/tls/qcertonlybackend.dll` | Qt TLS backend: qcertonlybackend.dll. |
| `_internal/PySide6/plugins/tls/qopensslbackend.dll` | Qt TLS backend: qopensslbackend.dll. |
| `_internal/PySide6/plugins/tls/qschannelbackend.dll` | Qt TLS backend: qschannelbackend.dll. |
| `_internal/PySide6/pyside6.abi3.dll` | Shared PySide6 binding runtime connecting Python and Qt. |
| `_internal/PySide6/translations/qt_ar.qm` | Bundled Qt interface translation catalog for locale ar. |
| `_internal/PySide6/translations/qt_bg.qm` | Bundled Qt interface translation catalog for locale bg. |
| `_internal/PySide6/translations/qt_ca.qm` | Bundled Qt interface translation catalog for locale ca. |
| `_internal/PySide6/translations/qt_cs.qm` | Bundled Qt interface translation catalog for locale cs. |
| `_internal/PySide6/translations/qt_da.qm` | Bundled Qt interface translation catalog for locale da. |
| `_internal/PySide6/translations/qt_de.qm` | Bundled Qt interface translation catalog for locale de. |
| `_internal/PySide6/translations/qt_en.qm` | Bundled Qt interface translation catalog for locale en. |
| `_internal/PySide6/translations/qt_es.qm` | Bundled Qt interface translation catalog for locale es. |
| `_internal/PySide6/translations/qt_fa.qm` | Bundled Qt interface translation catalog for locale fa. |
| `_internal/PySide6/translations/qt_fi.qm` | Bundled Qt interface translation catalog for locale fi. |
| `_internal/PySide6/translations/qt_fr.qm` | Bundled Qt interface translation catalog for locale fr. |
| `_internal/PySide6/translations/qt_gd.qm` | Bundled Qt interface translation catalog for locale gd. |
| `_internal/PySide6/translations/qt_gl.qm` | Bundled Qt interface translation catalog for locale gl. |
| `_internal/PySide6/translations/qt_he.qm` | Bundled Qt interface translation catalog for locale he. |
| `_internal/PySide6/translations/qt_help_ar.qm` | Bundled Qt interface translation catalog for locale ar. |
| `_internal/PySide6/translations/qt_help_bg.qm` | Bundled Qt interface translation catalog for locale bg. |
| `_internal/PySide6/translations/qt_help_ca.qm` | Bundled Qt interface translation catalog for locale ca. |
| `_internal/PySide6/translations/qt_help_cs.qm` | Bundled Qt interface translation catalog for locale cs. |
| `_internal/PySide6/translations/qt_help_da.qm` | Bundled Qt interface translation catalog for locale da. |
| `_internal/PySide6/translations/qt_help_de.qm` | Bundled Qt interface translation catalog for locale de. |
| `_internal/PySide6/translations/qt_help_en.qm` | Bundled Qt interface translation catalog for locale en. |
| `_internal/PySide6/translations/qt_help_es.qm` | Bundled Qt interface translation catalog for locale es. |
| `_internal/PySide6/translations/qt_help_fr.qm` | Bundled Qt interface translation catalog for locale fr. |
| `_internal/PySide6/translations/qt_help_gl.qm` | Bundled Qt interface translation catalog for locale gl. |
| `_internal/PySide6/translations/qt_help_hr.qm` | Bundled Qt interface translation catalog for locale hr. |
| `_internal/PySide6/translations/qt_help_hu.qm` | Bundled Qt interface translation catalog for locale hu. |
| `_internal/PySide6/translations/qt_help_it.qm` | Bundled Qt interface translation catalog for locale it. |
| `_internal/PySide6/translations/qt_help_ja.qm` | Bundled Qt interface translation catalog for locale ja. |
| `_internal/PySide6/translations/qt_help_ka.qm` | Bundled Qt interface translation catalog for locale ka. |
| `_internal/PySide6/translations/qt_help_kk.qm` | Bundled Qt interface translation catalog for locale kk. |
| `_internal/PySide6/translations/qt_help_ko.qm` | Bundled Qt interface translation catalog for locale ko. |
| `_internal/PySide6/translations/qt_help_nl.qm` | Bundled Qt interface translation catalog for locale nl. |
| `_internal/PySide6/translations/qt_help_nn.qm` | Bundled Qt interface translation catalog for locale nn. |
| `_internal/PySide6/translations/qt_help_pl.qm` | Bundled Qt interface translation catalog for locale pl. |
| `_internal/PySide6/translations/qt_help_pt_BR.qm` | Bundled Qt interface translation catalog for locale pt_BR. |
| `_internal/PySide6/translations/qt_help_ru.qm` | Bundled Qt interface translation catalog for locale ru. |
| `_internal/PySide6/translations/qt_help_sk.qm` | Bundled Qt interface translation catalog for locale sk. |
| `_internal/PySide6/translations/qt_help_sl.qm` | Bundled Qt interface translation catalog for locale sl. |
| `_internal/PySide6/translations/qt_help_sv.qm` | Bundled Qt interface translation catalog for locale sv. |
| `_internal/PySide6/translations/qt_help_tr.qm` | Bundled Qt interface translation catalog for locale tr. |
| `_internal/PySide6/translations/qt_help_uk.qm` | Bundled Qt interface translation catalog for locale uk. |
| `_internal/PySide6/translations/qt_help_zh_CN.qm` | Bundled Qt interface translation catalog for locale zh_CN. |
| `_internal/PySide6/translations/qt_help_zh_TW.qm` | Bundled Qt interface translation catalog for locale zh_TW. |
| `_internal/PySide6/translations/qt_hr.qm` | Bundled Qt interface translation catalog for locale hr. |
| `_internal/PySide6/translations/qt_hu.qm` | Bundled Qt interface translation catalog for locale hu. |
| `_internal/PySide6/translations/qt_it.qm` | Bundled Qt interface translation catalog for locale it. |
| `_internal/PySide6/translations/qt_ja.qm` | Bundled Qt interface translation catalog for locale ja. |
| `_internal/PySide6/translations/qt_ka.qm` | Bundled Qt interface translation catalog for locale ka. |
| `_internal/PySide6/translations/qt_kk.qm` | Bundled Qt interface translation catalog for locale kk. |
| `_internal/PySide6/translations/qt_ko.qm` | Bundled Qt interface translation catalog for locale ko. |
| `_internal/PySide6/translations/qt_lg.qm` | Bundled Qt interface translation catalog for locale lg. |
| `_internal/PySide6/translations/qt_lt.qm` | Bundled Qt interface translation catalog for locale lt. |
| `_internal/PySide6/translations/qt_lv.qm` | Bundled Qt interface translation catalog for locale lv. |
| `_internal/PySide6/translations/qt_nl.qm` | Bundled Qt interface translation catalog for locale nl. |
| `_internal/PySide6/translations/qt_nn.qm` | Bundled Qt interface translation catalog for locale nn. |
| `_internal/PySide6/translations/qt_pl.qm` | Bundled Qt interface translation catalog for locale pl. |
| `_internal/PySide6/translations/qt_pt_BR.qm` | Bundled Qt interface translation catalog for locale pt_BR. |
| `_internal/PySide6/translations/qt_pt_PT.qm` | Bundled Qt interface translation catalog for locale pt_PT. |
| `_internal/PySide6/translations/qt_ru.qm` | Bundled Qt interface translation catalog for locale ru. |
| `_internal/PySide6/translations/qt_sk.qm` | Bundled Qt interface translation catalog for locale sk. |
| `_internal/PySide6/translations/qt_sl.qm` | Bundled Qt interface translation catalog for locale sl. |
| `_internal/PySide6/translations/qt_sv.qm` | Bundled Qt interface translation catalog for locale sv. |
| `_internal/PySide6/translations/qt_tr.qm` | Bundled Qt interface translation catalog for locale tr. |
| `_internal/PySide6/translations/qt_uk.qm` | Bundled Qt interface translation catalog for locale uk. |
| `_internal/PySide6/translations/qt_zh_CN.qm` | Bundled Qt interface translation catalog for locale zh_CN. |
| `_internal/PySide6/translations/qt_zh_TW.qm` | Bundled Qt interface translation catalog for locale zh_TW. |
| `_internal/PySide6/translations/qtbase_ar.qm` | Bundled Qt interface translation catalog for locale ar. |
| `_internal/PySide6/translations/qtbase_bg.qm` | Bundled Qt interface translation catalog for locale bg. |
| `_internal/PySide6/translations/qtbase_ca.qm` | Bundled Qt interface translation catalog for locale ca. |
| `_internal/PySide6/translations/qtbase_cs.qm` | Bundled Qt interface translation catalog for locale cs. |
| `_internal/PySide6/translations/qtbase_da.qm` | Bundled Qt interface translation catalog for locale da. |
| `_internal/PySide6/translations/qtbase_de.qm` | Bundled Qt interface translation catalog for locale de. |
| `_internal/PySide6/translations/qtbase_en.qm` | Bundled Qt interface translation catalog for locale en. |
| `_internal/PySide6/translations/qtbase_es.qm` | Bundled Qt interface translation catalog for locale es. |
| `_internal/PySide6/translations/qtbase_fa.qm` | Bundled Qt interface translation catalog for locale fa. |
| `_internal/PySide6/translations/qtbase_fi.qm` | Bundled Qt interface translation catalog for locale fi. |
| `_internal/PySide6/translations/qtbase_fr.qm` | Bundled Qt interface translation catalog for locale fr. |
| `_internal/PySide6/translations/qtbase_gd.qm` | Bundled Qt interface translation catalog for locale gd. |
| `_internal/PySide6/translations/qtbase_he.qm` | Bundled Qt interface translation catalog for locale he. |
| `_internal/PySide6/translations/qtbase_hr.qm` | Bundled Qt interface translation catalog for locale hr. |
| `_internal/PySide6/translations/qtbase_hu.qm` | Bundled Qt interface translation catalog for locale hu. |
| `_internal/PySide6/translations/qtbase_it.qm` | Bundled Qt interface translation catalog for locale it. |
| `_internal/PySide6/translations/qtbase_ja.qm` | Bundled Qt interface translation catalog for locale ja. |
| `_internal/PySide6/translations/qtbase_ka.qm` | Bundled Qt interface translation catalog for locale ka. |
| `_internal/PySide6/translations/qtbase_kk.qm` | Bundled Qt interface translation catalog for locale kk. |
| `_internal/PySide6/translations/qtbase_ko.qm` | Bundled Qt interface translation catalog for locale ko. |
| `_internal/PySide6/translations/qtbase_lg.qm` | Bundled Qt interface translation catalog for locale lg. |
| `_internal/PySide6/translations/qtbase_lv.qm` | Bundled Qt interface translation catalog for locale lv. |
| `_internal/PySide6/translations/qtbase_nl.qm` | Bundled Qt interface translation catalog for locale nl. |
| `_internal/PySide6/translations/qtbase_nn.qm` | Bundled Qt interface translation catalog for locale nn. |
| `_internal/PySide6/translations/qtbase_pl.qm` | Bundled Qt interface translation catalog for locale pl. |
| `_internal/PySide6/translations/qtbase_pt_BR.qm` | Bundled Qt interface translation catalog for locale pt_BR. |
| `_internal/PySide6/translations/qtbase_ru.qm` | Bundled Qt interface translation catalog for locale ru. |
| `_internal/PySide6/translations/qtbase_sk.qm` | Bundled Qt interface translation catalog for locale sk. |
| `_internal/PySide6/translations/qtbase_sv.qm` | Bundled Qt interface translation catalog for locale sv. |
| `_internal/PySide6/translations/qtbase_tr.qm` | Bundled Qt interface translation catalog for locale tr. |
| `_internal/PySide6/translations/qtbase_uk.qm` | Bundled Qt interface translation catalog for locale uk. |
| `_internal/PySide6/translations/qtbase_zh_CN.qm` | Bundled Qt interface translation catalog for locale zh_CN. |
| `_internal/PySide6/translations/qtbase_zh_TW.qm` | Bundled Qt interface translation catalog for locale zh_TW. |
| `_internal/VCRUNTIME140.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/VCRUNTIME140_1.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/_bz2.pyd` | Python bzip2 compression support. |
| `_internal/_decimal.pyd` | Python decimal arithmetic support. |
| `_internal/_hashlib.pyd` | Python native hashing support. |
| `_internal/_lzma.pyd` | Python LZMA compression support. |
| `_internal/_socket.pyd` | Python operating-system socket support. |
| `_internal/_ssl.pyd` | Python TLS support. |
| `_internal/_zstd.pyd` | Python Zstandard compression support. |
| `_internal/agentrocky/jazz1.png` | User-supplied jazz dance animation frame 1. |
| `_internal/agentrocky/jazz2.png` | User-supplied jazz dance animation frame 2. |
| `_internal/agentrocky/jazz3.png` | User-supplied jazz dance animation frame 3. |
| `_internal/agentrocky/stand.png` | User-supplied transparent standing pose, also used by the terminal portrait and tray icon. |
| `_internal/agentrocky/walkleft1.png` | User-supplied walking animation frame 1. |
| `_internal/agentrocky/walkleft2.png` | User-supplied walking animation frame 2. |
| `_internal/base_library.zip` | Frozen Python standard-library modules used by the bundled interpreter. |
| `_internal/libcrypto-3.dll` | OpenSSL cryptographic dependency for the bundled Python TLS/hash modules. |
| `_internal/libssl-3.dll` | OpenSSL TLS protocol dependency for the bundled Python SSL module. |
| `_internal/python3.dll` | Python stable-ABI loader used by native extension modules. |
| `_internal/python314.dll` | Bundled Python 3.14 interpreter runtime; no separate Python installation is needed. |
| `_internal/select.pyd` | Python socket/readiness polling support. |
| `_internal/shiboken6/MSVCP140.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/shiboken6/Shiboken.pyd` | Python access to the Shiboken binding support library. |
| `_internal/shiboken6/VCRUNTIME140.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/shiboken6/VCRUNTIME140_1.dll` | Microsoft Visual C++ runtime dependency for Python, Qt, or their native extensions. |
| `_internal/shiboken6/shiboken6.abi3.dll` | Native object/type conversion and ownership support for PySide6. |
| `_internal/unicodedata.pyd` | Python Unicode character metadata. |
