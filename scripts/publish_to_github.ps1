param(
  [Parameter(Mandatory=$true)][string]$GithubUser,
  [string]$RepoName = "VETERINARIA-INTELIGENTE",
  [ValidateSet("public","private")][string]$Visibility = "public"
)

Write-Host "Publishing repo to GitHub: $GithubUser/$RepoName ($Visibility)" -ForegroundColor Cyan

# 1) Check token
$token = $env:GITHUB_TOKEN
if (-not $token) {
  Write-Error "Environment variable GITHUB_TOKEN not set. Create a GitHub Personal Access Token (scope: repo) and set it, e.g.:`n$env:GITHUB_TOKEN='ghp_xxx'"
  exit 1
}

# 2) Create repository via API (if not exists)
$body = @{ name = $RepoName; private = ($Visibility -eq 'private'); auto_init = $false } | ConvertTo-Json
$headers = @{ Authorization = "token $token"; 'User-Agent' = 'ps-github-client'; Accept = 'application/vnd.github+json' }

try {
  $resp = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method Post -Headers $headers -Body $body
  Write-Host ("Repository created: {0}" -f $resp.html_url) -ForegroundColor Green
} catch {
  Write-Warning ("Repo creation may have failed or already exists: {0}" -f $_.Exception.Message)
}

# 3) Ensure git is available
$gitOk = $true
try { git --version | Out-Null } catch { $gitOk = $false }
if (-not $gitOk) { Write-Error "Git is not installed or not in PATH. Install from https://git-scm.com/download/win"; exit 1 }

# 4) Initialize and push
if (-not (Test-Path ".git")) { git init }

# Avoid committing the script's output
try { git add . } catch {
  Write-Warning ("git add failed: {0}" -f $_.Exception.Message)
}

try { git commit -m "Initial commit: Veterinaria Inteligente" } catch {
  Write-Warning ("git commit skipped: {0}" -f $_.Exception.Message)
}

try { git branch -M main } catch { }

$remoteUrl = "https://github.com/$GithubUser/$RepoName.git"
$hasOrigin = $false
try { git remote get-url origin | Out-Null; $hasOrigin = $true } catch { $hasOrigin = $false }
if (-not $hasOrigin) { git remote add origin $remoteUrl } else { git remote set-url origin $remoteUrl }

try {
  git push -u origin main
  Write-Host "Done. URL: $remoteUrl" -ForegroundColor Green
} catch {
  Write-Error ("git push failed: {0}" -f $_.Exception.Message)
  exit 1
}
