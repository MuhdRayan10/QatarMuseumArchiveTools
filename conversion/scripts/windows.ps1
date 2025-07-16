<#  FFmpeg + REDCINE-X PRO bootstrapper (idempotent for FFmpeg)
    Run from an *elevated* PowerShell window.
#>

$ErrorActionPreference = 'Stop'
if (-not ( [Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()
      ).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Warning 'Re-run this script from an *elevated* PowerShell prompt.'
    exit 1
}

[Net.ServicePointManager]::SecurityProtocol = 3072  # TLS 1.2+

# -------- CONFIG --------
$ffmpegUrl      = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
$ffmpegZip      = "$env:TEMP\ffmpeg.zip"
$ffmpegRoot     = 'C:\Tools\ffmpeg'        # change if desired
$ffmpegBinGlob  = "$ffmpegRoot\ffmpeg-*\bin\ffmpeg.exe"   # wildcard for version folder

$redcineUrl     = 'https://downloads.red.com/rcx/release/64.0.25/REDCINE-X_PRO_Windows_64.0.25.zip'
$redZip         = "$env:TEMP\rcx.zip"
$redExtract     = "$env:TEMP\rcx"
$redProgramDir  = 'C:\Program Files\REDCINE-X PRO 64-bit' # default install location
# ------------------------

# ========== FFmpeg ==========
if (Test-Path $ffmpegBinGlob) {
    Write-Host "✓ FFmpeg already present — skipping download/extract."
    $ffmpegResolvedBin = (Get-Item $ffmpegBinGlob | Select-Object -First 1).DirectoryName
} else {
    Write-Host "`n◼ Downloading FFmpeg …"
    Invoke-WebRequest $ffmpegUrl -OutFile $ffmpegZip

    Write-Host "◼ Extracting to $ffmpegRoot"
    New-Item $ffmpegRoot -ItemType Directory -Force | Out-Null
    Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegRoot -Force
    Remove-Item $ffmpegZip

    $ffmpegResolvedBin = (Get-Item $ffmpegBinGlob | Select-Object -First 1).DirectoryName
}

# Add FFmpeg bin to machine PATH if needed
$machinePath = [Environment]::GetEnvironmentVariable('Path','Machine')
if (-not ($machinePath -split ';' | Where-Object { $_ -ieq $ffmpegResolvedBin })) {
    [Environment]::SetEnvironmentVariable('Path', "$machinePath;$ffmpegResolvedBin", 'Machine')
    Write-Host "✓ Added FFmpeg to PATH"
} else {
    Write-Host "✓ FFmpeg already on PATH"
}

Write-Host "`nAll done!  Open a *new* command prompt or PowerShell session for the updated PATH to take effect."
