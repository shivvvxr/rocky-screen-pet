$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$rockyPython = if (Get-Command py -ErrorAction SilentlyContinue) { (Get-Command py).Source } else { (Get-Command python).Source }
& $rockyPython -m pip install -r requirements.txt pyinstaller
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
$rockyOriginalPath = $env:PATH
$rockyRuntime = & $rockyPython -c 'import sys; from pathlib import Path; print(Path(sys.executable).parent)'
try {
    # Prevent unrelated programs' ICU and CRT DLLs from entering the bundle.
    $env:PATH = "$env:SystemRoot\System32;$env:SystemRoot;$rockyRuntime;$(Split-Path -Parent $rockyPython)"
    & $rockyPython -m PyInstaller --noconfirm --clean --windowed --onedir --name Rocky --collect-submodules rocky_windows --add-data 'agentrocky/stand.png;agentrocky' --add-data 'agentrocky/walkleft1.png;agentrocky' --add-data 'agentrocky/walkleft2.png;agentrocky' --add-data 'agentrocky/jazz1.png;agentrocky' --add-data 'agentrocky/jazz2.png;agentrocky' --add-data 'agentrocky/jazz3.png;agentrocky' launch_windows.py
    if ($LASTEXITCODE -ne 0) { throw 'Executable build failed.' }
} finally {
    $env:PATH = $rockyOriginalPath
}
Write-Host 'Built dist\Rocky\Rocky.exe. Distribute the entire dist\Rocky folder.'
