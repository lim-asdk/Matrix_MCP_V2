param(
    [string]$PythonExe = ""
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$target = Join-Path $repoRoot "run_desktop_app.py"

function Resolve-ProjectPython {
    param(
        [string]$RepoRoot,
        [string]$PreferredPython
    )

    if ($PreferredPython -and (Test-Path $PreferredPython)) {
        return $PreferredPython
    }

    $sharedRoot = Split-Path -Parent (Split-Path -Parent $RepoRoot)
    $sharedPython = Join-Path $sharedRoot ".venv\Scripts\python.exe"
    if (Test-Path $sharedPython) {
        return $sharedPython
    }

    $systemPython = Get-Command python -ErrorAction SilentlyContinue
    if ($systemPython -and $systemPython.Path) {
        return $systemPython.Path
    }

    throw "No usable Python found. Checked shared venv and system python."
}

function Ensure-Pip {
    param([string]$Python)
    Write-Host "Verifying Python environment..." -ForegroundColor Cyan
    $hasPip = & $Python -m pip --version 2>$null
    if (-not $?) {
        Write-Host "Pip missing in venv. Attempting repair..." -ForegroundColor Yellow
        & $Python -m ensurepip --default-pip
        if (-not $?) {
            Write-Warning "Failed to restore Pip. WebView components may fail to load."
        } else {
            Write-Host "Pip restored successfully." -ForegroundColor Green
        }
    }
}

$python = Resolve-ProjectPython -RepoRoot $repoRoot -PreferredPython $PythonExe
Ensure-Pip -Python $python

Push-Location $repoRoot
try {
    & $python $target @args
} finally {
    Pop-Location
}
