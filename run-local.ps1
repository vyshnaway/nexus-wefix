param(
    [switch]$CreateDemoData
)

$ErrorActionPreference = 'Stop'

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    throw 'Python was not found. Install Python 3 and make sure "python" is available in PATH.'
}

$projectRoot = $PSScriptRoot
$sourceRoot = Join-Path $projectRoot 'src'
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    & $pythonCommand.Source -m venv (Join-Path $projectRoot '.venv')
    if ($LASTEXITCODE -ne 0) {
        throw 'Failed to create the virtual environment.'
    }
}

& $venvPython -m pip install -r (Join-Path $projectRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to install Python dependencies.'
}

$env:DATABASE_URL = 'sqlite:///db.sqlite3'
$env:DEBUG = 'True'
$env:SECRET_KEY = 'local-development-key'

Push-Location $sourceRoot
try {
    & $venvPython manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        throw 'Database migrations failed.'
    }

    if ($CreateDemoData) {
        & $venvPython manage.py create_demo_data
        if ($LASTEXITCODE -ne 0) {
            throw 'Creating demo data failed.'
        }
    }

    & $venvPython manage.py runserver 127.0.0.1:8000
    if ($LASTEXITCODE -ne 0) {
        throw 'The Django development server exited with an error.'
    }
}
finally {
    Pop-Location
}
