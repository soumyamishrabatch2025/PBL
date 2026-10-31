$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
New-Item -ItemType Directory -Force -Path tmp/pip | Out-Null
$env:TEMP = Join-Path $projectRoot 'tmp/pip'
$env:TMP = $env:TEMP

# Python 3.12 is recommended. This leaves any existing .venv untouched.
if (-not (Test-Path -LiteralPath '.venv-research/Scripts/python.exe')) {
    py -3.12 -m venv .venv-research
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 or create .venv-research with your Python 3.12 executable.' }
}
& ./.venv-research/Scripts/python.exe -m ensurepip --upgrade
if ($LASTEXITCODE -ne 0) { throw 'pip bootstrap failed' }
& ./.venv-research/Scripts/python.exe -m pip install 'torch==2.7.1' --index-url https://download.pytorch.org/whl/cu126
if ($LASTEXITCODE -ne 0) { throw 'PyTorch installation failed' }
& ./.venv-research/Scripts/python.exe -m pip install -e .
if ($LASTEXITCODE -ne 0) { throw 'Project installation failed' }
& ./.venv-research/Scripts/python.exe run_research.py doctor
