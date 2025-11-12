param(
    [int]$Count = 100
)

$ErrorActionPreference = 'Stop'

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $workspace
$venvPy = Join-Path $root '.venv\\Scripts\\python.exe'

function Initialize-Venv {
    if (-not (Test-Path $venvPy)) {
        Write-Host 'Creando entorno virtual (.venv) y instalando dependencias...'
        & py -m venv (Join-Path $root '.venv') | Out-Null
        & (Join-Path $root '.venv\Scripts\pip.exe') install -r (Join-Path $root 'requirements.txt') | Out-Null
    }
}

Initialize-Venv

Write-Host "Ejecutando seeder de internet: $Count registros"
& $venvPy -m app.db.seed --internet $Count
if ($LASTEXITCODE -ne 0) {
    throw "Fallo la siembra de internet"
}

Write-Host 'Listo: base de datos enriquecida con datos de Internet.'
