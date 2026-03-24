param(
    [string]$PythonExe = ""
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$target = Join-Path $repoRoot "run_web_server.py"

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

$python = Resolve-ProjectPython -RepoRoot $repoRoot -PreferredPython $PythonExe

Push-Location $repoRoot
try {
    & $python $target @args
} finally {
    Pop-Location
}
