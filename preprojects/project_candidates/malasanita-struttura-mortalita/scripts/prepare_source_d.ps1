$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $PSScriptRoot
$tmpDir = Join-Path $projectDir ".tmp_source_d"
$inputsDir = Join-Path $projectDir "inputs"
$zipPath = Join-Path $tmpDir "Tavole.zip"
$extractDir = Join-Path $tmpDir "unzipped"
$targetFile = Join-Path $inputsDir "data_base_2022.xlsx"
$url = "https://www.istat.it/wp-content/uploads/2025/09/Tavole.zip"

New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
New-Item -ItemType Directory -Force -Path $inputsDir | Out-Null

if (Test-Path $extractDir) {
  Remove-Item -Recurse -Force $extractDir
}

Write-Host "Download ZIP ISTAT..."
Invoke-WebRequest -Uri $url -OutFile $zipPath

Write-Host "Estrazione ZIP..."
Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

$expected = Join-Path $extractDir "Tavole\\data_base_2022.xlsx"
if (-not (Test-Path $expected)) {
  throw "File atteso non trovato: $expected"
}

Copy-Item -Path $expected -Destination $targetFile -Force
Write-Host "OK -> $targetFile"
