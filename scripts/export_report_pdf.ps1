param(
  [string]$InputMd = "docs/Informe_Veterinaria_Inteligente.md",
  [string]$OutputPdf = "docs/Informe_Veterinaria_Inteligente.pdf",
  [string]$OutputHtml = "docs/Informe_Veterinaria_Inteligente.html",
  [string]$Css = "docs/pdf.css"
)

function Has-Command {
  param([string]$Name)
  try { Get-Command $Name -ErrorAction Stop | Out-Null; return $true } catch { return $false }
}

if (-not (Test-Path $InputMd)) {
  Write-Error "No se encontró el archivo Markdown: $InputMd"
  exit 1
}

$pandoc = Has-Command "pandoc"
$wkhtml = Has-Command "wkhtmltopdf"
$pdflatex = Has-Command "pdflatex"

if ($pandoc -and ($wkhtml -or $pdflatex)) {
  Write-Host "Exportando a PDF con pandoc..." -ForegroundColor Cyan
  $engineArg = @()
  if ($wkhtml) { $engineArg = @("--pdf-engine=wkhtmltopdf") }
  elseif ($pdflatex) { $engineArg = @("--pdf-engine=pdflatex") }

  $args = @(
    "-s", $InputMd,
    "-o", $OutputPdf,
    "--toc",
    "--metadata", "title=Informe - Veterinaria Inteligente"
  ) + $engineArg

  if (Test-Path $Css) { $args += @("-c", $Css) }

  & pandoc @args
  if ($LASTEXITCODE -eq 0) {
    Write-Host "PDF generado: $OutputPdf" -ForegroundColor Green
    exit 0
  } else {
    Write-Warning "Falló la exportación directa a PDF. Se generará HTML como alternativa."
  }
}

# Fallback: generar HTML autosuficiente
if ($pandoc) {
  Write-Host "Generando HTML con pandoc (fallback)..." -ForegroundColor Yellow
  $htmlArgs = @(
    "-s", $InputMd,
    "-o", $OutputHtml,
    "--toc",
    "--metadata", "title=Informe - Veterinaria Inteligente",
    "--self-contained"
  )
  if (Test-Path $Css) { $htmlArgs += @("-c", $Css) }
  & pandoc @htmlArgs
  if ($LASTEXITCODE -eq 0) {
    Write-Host "HTML generado: $OutputHtml" -ForegroundColor Green
    Write-Host "Abrir en navegador y 'Imprimir' -> 'Microsoft Print to PDF' para obtener el PDF." -ForegroundColor DarkGray
    try { Invoke-Item $OutputHtml } catch {}
    exit 0
  } else {
    Write-Error "No se pudo generar HTML. ¿Está pandoc instalado? https://pandoc.org/installing.html"
    exit 1
  }
} else {
  Write-Error "Pandoc no está instalado. Instalar desde: https://pandoc.org/installing.html. Luego reintente."
  exit 1
}
