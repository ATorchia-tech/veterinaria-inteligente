param(
  [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = 'Stop'

function Test-ApiUp {
  param([string]$Url)
  try {
    Invoke-WebRequest -Uri "$Url/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    return $true
  } catch { return $false }
}

function Invoke-JsonPost {
  param(
    [Parameter(Mandatory=$true)][string]$Url,
    [Parameter(Mandatory=$true)]$BodyObj
  )
  $json = $BodyObj | ConvertTo-Json -Depth 10 -Compress
  return Invoke-RestMethod -Method Post -Uri $Url -Body $json -ContentType 'application/json; charset=utf-8'
}

try {
  Write-Host "[0/5] Esperando API (hasta 20s)..." -ForegroundColor Cyan
  $ready = $false
  for ($i = 0; $i -lt 40; $i++) { # ~20s
    if (Test-ApiUp -Url $BaseUrl) { $ready = $true; break }
    Start-Sleep -Milliseconds 500
  }
  if (-not $ready) { throw "API no disponible en $BaseUrl" }

  Write-Host "[1/5] Health check..." -ForegroundColor Cyan
  $health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health"
  Write-Host ("  -> status: {0}" -f $health.status) -ForegroundColor Green

  Write-Host "[2/5] Crear owner..." -ForegroundColor Cyan
  $ownerBody = @{ name = "Juan Perez"; phone = "123456"; email = "juan@example.com" }
  $owner = Invoke-JsonPost -Url "$BaseUrl/owners" -BodyObj $ownerBody
  Write-Host ("  -> owner id: {0}" -f $owner.id) -ForegroundColor Green

  Write-Host "[3/5] Crear pet..." -ForegroundColor Cyan
  $petBody = @{ 
    name = "Firulais"; species = "perro"; breed = "mestizo"; birth_date = "2020-05-01"; 
    notes = "vacunas al dia"; owner_id = $owner.id 
  }
  $pet = Invoke-JsonPost -Url "$BaseUrl/pets" -BodyObj $petBody
  Write-Host ("  -> pet id: {0}" -f $pet.id) -ForegroundColor Green

  Write-Host "[4/5] Crear appointment..." -ForegroundColor Cyan
  $apptTime = (Get-Date).AddHours(2)
  $apptIso  = $apptTime.ToString('s')  # yyyy-MM-ddTHH:mm:ss
  $apBody = @{ date = $apptIso; reason = "control anual"; pet_id = $pet.id }
  $ap = Invoke-JsonPost -Url "$BaseUrl/appointments" -BodyObj $apBody
  Write-Host ("  -> appointment id: {0} at {1}" -f $ap.id, $ap.date) -ForegroundColor Green

  Write-Host "[5/5] Consultar agenda del dia..." -ForegroundColor Cyan
  $day = $apptTime.ToString('yyyy-MM-dd')
  $agenda = Invoke-RestMethod -Method Get -Uri "$BaseUrl/schedule/day?day=$day"
  $count = ($agenda | Measure-Object).Count
  Write-Host ("  -> turnos en {0}: {1}" -f $day, $count) -ForegroundColor Green

  Write-Host "\nOK: Smoke E2E completado." -ForegroundColor Green
  Write-Host ("Resumen: owner={0}, pet={1}, appointment={2}" -f $owner.id, $pet.id, $ap.id)
}
catch {
  Write-Host "ERROR durante el smoke test:" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  if ($_.Exception.Response -and $_.Exception.Response.Content) {
    try {
      $body = $_.Exception.Response.Content | ConvertFrom-Json -ErrorAction SilentlyContinue
      if ($body) { $body | ConvertTo-Json -Depth 10 | Write-Host }
    } catch {}
  }
  exit 1
}
