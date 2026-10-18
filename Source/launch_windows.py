"""Entry point for Python and PyInstaller."""
if __name__ == '__main__':
    try:
        from rocky_windows.app import main
        raise SystemExit(main())
    except Exception:
        import os
        from pathlib import Path
        import traceback
        log = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'AgentRocky'
        log.mkdir(parents=True, exist_ok=True)
        (log / 'startup-error.log').write_text(traceback.format_exc(), encoding='utf-8')
        raise
