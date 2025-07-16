<#  FFmpeg + REDCINE-X PRO bootstrapper
    Tested on Windows 10/11 PowerShell 5/7
#>

# ---------------- safety & config -----------------
$ErrorActionPreference = 'Stop'
if (-not ( [Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()
      ).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Warning 'Re-run this script from an *elevated* PowerShell prompt.'
    exit 1
}

# Use TLS 1.2/1.3 for all web requests
[Net.ServicePointManager]::SecurityProtocol = 3072

$ffmpegUrl      = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
$ffmpegZip      = "$env:TEMP\ffmpeg.zip"
$ffmpegRoot     = 'C:\Tools\ffmpeg'        # adjust if you like
$ffmpegBinPath  = "$ffmpegRoot\ffmpeg-*\bin"  # wildcard matches version folder

# --------------- FFmpeg --------------------------
Write-Host "`n◼ Downloading FFmpeg …"
Invoke-WebRequest $ffmpegUrl -OutFile $ffmpegZip

Write-Host "◼ Extracting to $ffmpegRoot"
New-Item $ffmpegRoot -ItemType Directory -Force | Out-Null
Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegRoot -Force
Remove-Item $ffmpegZip

# Grab actual bin folder after wild-card expansion
$ffmpegResolvedBin = Get-Item $ffmpegBinPath | Select-Object -First 1 | ForEach-Object FullName

# Add FFmpeg to PATH (machine scope)
$machinePath = [Environment]::GetEnvironmentVariable('Path','Machine')
if (-not $machinePath.Split(';') -contains $ffmpegResolvedBin) {
    [Environment]::SetEnvironmentVariable('Path', "$machinePath;$ffmpegResolvedBin", 'Machine')
    Write-Host "✓ Added FFmpeg to PATH"
} else {
    Write-Host "✓ FFmpeg already on PATH"
}

Write-Host "`nAll done!  Open a *new* command prompt or PowerShell session for the updated PATH to take effect."
